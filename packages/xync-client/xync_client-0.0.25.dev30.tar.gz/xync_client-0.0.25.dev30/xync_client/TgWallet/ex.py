from asyncio import run

from x_model import init_db
from xync_schema.pydantic import PmPyd, PmexBankPyd, CurEpyd, CoinEpyd, BaseAdPydIn, AdBuyPydIn

from xync_schema import models
from xync_schema.models import Ex, Direction, Pair, Coin, Cur, Pm, Actor, PairEx

from xync_client.TgWallet.pyd import (
    PmEpydRoot,
    OneAdTakerMakerSale,
    OneAdTakerBuy,
    AdTakerSaleBuy,
    _TakerOne,
    _PmsTrait,
    _BaseAd,
)
from xync_client.loader import PG_DSN
from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.Base import MapOfIdsList
from xync_client.TgWallet.auth import AuthClient


class ExClient(BaseExClient, AuthClient):
    def __init__(self, ex: Ex):
        super().__init__(ex)  # BaseExClient

    def pm_type_map(self, pm: Pm) -> str:
        return "V2" if pm.name.startswith("SBP") else "V1"

    # 00: todo: min-max for cur and coin ad amount, order, fee ..
    async def _settings(self) -> dict:
        settings = await self._post("/p2p/public-api/v2/offer/settings/get")
        return settings["data"]

    # 19: Список поддерживаемых валют тейкера
    async def curs(self) -> list[CurEpyd]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        stg = await self._settings()
        roundings: dict[str, int] = stg["offerSettings"]["roundingScaleByFiatCurrency"]
        minimums: dict[str, str] = stg["offerSettings"]["minOrderAmountByCurrencyCode"]
        return [
            CurEpyd(
                exid=c["code"], ticker=c["code"], rounding_scale=roundings.get(c["code"]), minimum=minimums[c["code"]]
            )
            for c in coins_curs["data"]["fiat"]
        ]

    async def _pms(self, cur: str) -> dict[str, PmEpydRoot]:
        pms = await self._post("/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur})
        return {pm["code"]: PmEpydRoot(**pm) for pm in pms["data"]}

    # 20: Список платежных методов. todo: refact to pmexs?
    async def pms(self, cur: str = None) -> dict[str, PmPyd]:
        pms: dict[str:PmEpydRoot] = {}
        if cur:
            pms = await self._pms(cur)
        else:
            for cur in await self.curs():
                pms |= await self._pms(cur.exid)
        return {
            k: PmPyd(name=pm.nameEng, banks=[PmexBankPyd(exid=b.code, name=b.name) for b in pm.banks or []])
            for k, pm in pms.items()
        }

    # 21: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:
        return {cur.exid: list(await self._pms(cur.exid)) for cur in await self.curs()}

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    async def coins(self) -> list[CoinEpyd]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        stg = await self._settings()
        lims = list(stg["offerSettings"]["offerVolumeLimitsPerMarket"].values())
        coins = {k: max(float(v[k]["minInclusive"]) for v in lims) for k, v in lims[0].items()}
        return [
            CoinEpyd(exid=c["code"], ticker=c["code"], minimum=coins[c["code"]]) for c in coins_curs["data"]["crypto"]
        ]

    # 23: Список пар валюта/монет
    async def pairs(self) -> MapOfIdsList:
        coins = await self.coins()
        curs = await self.curs()
        pairs = {cur.exid: set(c.exid for c in coins) for cur in curs}
        return pairs

    # 42: Чужая объява по id
    async def ad(self, ad_id: int) -> _TakerOne:
        ad = await self._post("/p2p/public-api/v2/offer/get", {"offerId": ad_id})
        ad: dict = ad["data"]
        model = OneAdTakerMakerSale if ad["type"] == "SALE" else OneAdTakerBuy
        return model(**ad)

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[AdTakerSaleBuy]:
        params = {
            "baseCurrencyCode": coin_exid,
            "quoteCurrencyCode": cur_exid,
            "offerType": "SALE" if is_sell else "PURCHASE",
            "offset": 0,
            "limit": 100,
            # "merchantVerified": "TRUSTED"
        }
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params, "data")
        return [AdTakerSaleBuy(**ad) for ad in ads]

    async def ad_common_epyd2pydin(self, ad: _BaseAd) -> BaseAdPydIn:
        coin = await Coin.get_or_create_by_name(ad.price.baseCurrencyCode)
        cur = await Cur.get_or_create_by_name(ad.price.quoteCurrencyCode)
        pair, _ = await Pair.get_or_create(coin=coin, cur=cur)
        pairex, _ = await PairEx.get_or_create(pair=pair, ex=self.ex)
        dr, _ = await Direction.get_or_create(pairex=pairex, sell=ad.is_sell)
        return BaseAdPydIn(
            exid=ad.id,
            price=ad.price.value,
            min_fiat=ad.orderAmountLimits.min,
            max_fiat=ad.orderAmountLimits.max,
            direction=dr,
            detail=getattr(ad, "comment", None),
        )

    async def ad_taker_epyd2pydin(self, ad: _TakerOne) -> AdBuyPydIn:
        adx: BaseAdPydIn = await self.ad_common_epyd2pydin(ad)
        adx.maker = (await Actor.update_or_create({"name": ad.user.nickname}, ex=self.ex, exid=ad.user.userId))[0]
        pms = ad.paymentMethods if isinstance(ad, _PmsTrait) else [pd.paymentMethod for pd in ad.paymentDetails]
        return AdBuyPydIn(
            **adx.model_dump(), pms_=await Pm.filter(pmexs__ex=self.ex, pmexs__exid__in=[p.code for p in pms])
        )


async def _test():
    await init_db(PG_DSN, models, True)
    tgex = await Ex.get(name="TgWallet")
    cl: ExClient = tgex.client()

    # await cl.set_pmcurexs()
    # await cl.set_coinexs()

    # # # SALE # # #
    # get ads list
    ads: list[AdTakerSaleBuy] = await cl.ads("TON", "RUB", True)
    # prepare ad list items for saving
    ads_pydin: list[BaseAdPydIn] = [await cl.ad_taker_epyd2pydin(adp) for adp in ads]
    # list items save
    _ads_db = [await cl.ad_pydin2db(adi) for adi in ads_pydin]

    # # get ad fulls
    # ads_pyd: list[_TakerOne] = [await cl.ad(ad.id) for ad in ads]
    # # prepare ad fulls for saving
    # ads_pydin: list[AdBuyPydIn] = [await cl.ad_taker_epyd2pydin(adp) for adp in ads_pyd]
    # # full ones save
    # _ads_db = [await cl.ad_pydin2db(adi) for adi in ads_pydin]

    # # # BUY # # #
    # get ads list
    ads: list[AdTakerSaleBuy] = await cl.ads("TON", "RUB", False)
    # prepare ad list items for saving
    ads_pydin: list[BaseAdPydIn] = [await cl.ad_taker_epyd2pydin(adp) for adp in ads]
    # list items save
    _ads_db = [await cl.ad_pydin2db(adi) for adi in ads_pydin]

    # # get ad fulls
    # ads_pyd = [await cl.ad(ad.id) for ad in ads]
    # # prepare ad fulls for saving
    # ads_pydin: list[AdBuyPydIn] = [await cl.ad_taker_epyd2pydin(adp) for adp in ads_pyd]
    # # full ones save
    # _ads_db = [await cl.ad_pydin2db(adi) for adi in ads_pydin]

    await cl.close()


if __name__ == "__main__":
    run(_test())
