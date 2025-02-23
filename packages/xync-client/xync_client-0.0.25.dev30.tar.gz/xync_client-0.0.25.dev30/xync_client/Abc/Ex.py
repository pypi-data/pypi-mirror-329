import logging
import re
from abc import abstractmethod

from xync_schema.pydantic import BaseAdPydIn, PmPyd, BaseAd, CurEpyd, CoinEpyd
from xync_schema.models import Ex, Coin, Cur, Pm, Pmex, Curex, Pmcur, Coinex, PmexBank, Ad

from xync_client.Abc.Base import BaseClient, DictOfDicts, MapOfIdsList


class BaseExClient(BaseClient):
    pm_map: dict[str, str] = {
        "Юmoney": "YooMoney",
        "Local Bank (R-Green)": "Sberbank",
        "Local Bank (S-Green)": "Sberbank",
        "Local Card (Red)": "Alfa-Bank",
        "Local Card (Yellow)": "Tinkoff",
        "Local Card M-redTS": "MTS-bank",
        "Local Card-Green": "Sberbank",
        "Local Card-Yellow": "Tinkoff",
        "GTB Bank (Guarantee Trust Bank)": "GTBank",
    }

    def __init__(self, ex: Ex):
        self.acronyms: dict[str, str] = {}  # for pm norm
        super().__init__(ex)  # , "host_p2p"

    @abstractmethod
    def pm_type_map(self, type_: Pmex) -> str: ...

    # 19: Список поддерживаемых валют тейкера
    @abstractmethod
    async def curs(self) -> list[CurEpyd]:  # {cur.exid: cur.ticker}
        ...

    # 20: Список платежных методов
    @abstractmethod
    async def pms(self, cur: Cur = None) -> dict[int | str, PmPyd]:  # {pm.exid: pm}
        ...

    # 21: Список платежных методов по каждой валюте
    @abstractmethod
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        ...

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    @abstractmethod
    async def coins(self) -> list[CoinEpyd]:  # {coin.exid: coin.ticker}
        ...

    # 23: Список пар валюта/монет
    @abstractmethod
    async def pairs(self) -> MapOfIdsList: ...

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    @abstractmethod
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[BaseAd]:  # {ad.id: ad}
        ...

    # 42: Чужая объява по id
    @abstractmethod
    async def ad(self, ad_id: int) -> BaseAd: ...

    # Преобразрование объекта объявления из формата биржи в формат xync
    @abstractmethod
    async def ad_epyd2pydin(self, ad: BaseAd) -> BaseAdPydIn: ...  # my_uid: for MyAd

    def _pmnorm(self, s: str) -> str:
        def get_and_remove_acro(title: str) -> str:
            acr = "".join(word[0] for word in title.split(" ") if len(word) > 1 and word.istitle())
            if len(acr) > 2:
                title = title.replace(acr, "", 1)
                self.acronyms[acr] = title  # заполняем словарь аббревиатур
            return title

        def find_and_replace_only_acro(title: str) -> str:
            if " " not in title and title.isupper() and title in self.acronyms:
                title = self.acronyms[title]
            return title

        def remove(rms: str | list[str], st: str, regexp: bool = False) -> str:
            for rm in rms:
                st = re.sub(rm, "", st) if regexp else st.replace(rm, "")
            return st

        s = get_and_remove_acro(s)
        s = find_and_replace_only_acro(s)
        s = self.pm_map.get(s, s)
        s = s.lower().strip()
        s = remove("-:`'’′", s)
        common_map = {
            "nationale": "national",
            "а": "a",
            "á": "a",
            "â": "a",
            "о": "o",
            "ó": "o",
            "ō": "o",
            "ú": "u",
            "ü": "u",
            "ų": "u",
            "с": "c",
            "č": "c",
            "ç": "c",
            "é": "e",
            "è": "e",
            "ş": "s",
            "š": "s",
            "ř": "r",
            "í": "i",
        }
        for src, trgt in common_map.items():
            s = s.replace(src, trgt)
        rm_rgxps = [
            r"\(card\)$|\(russia\)$",
            r"^bank\s|bank$",
            r"^banka\s|\sbanka$",
            r"^bankas\s|\sbankas$",
            r"^bankası\s|\sbankası$",
            r"^banca\s|\sbanca$",
            r"^banco\s|\sbanco$",
            r"\.io$|\.com$",
            r"s\.a$",
        ]
        s = remove(rm_rgxps, s, True)
        return s.replace(" ", "")

    # Импорт Pm-ов (с Pmcur-, Pmex- и Pmcurex-ами) и валют (с Curex-ами) с биржи в бд
    async def set_pmcurexs(self):
        # Pms
        pms_epyds: dict[int | str, PmPyd] = {
            k: v for k, v in sorted((await self.pms()).items(), key=lambda x: x[1].name)
        }  # sort by name
        pms: dict[int | str, Pm] = dict({})
        prev = 0, "", ""  # id, normd-name, orig-name
        for k, pm in pms_epyds.items():
            norm = self._pmnorm(pm.name)
            if prev[1:] == (norm, pm.name):
                logging.warning(f"Pm: '{pm.name}' duplicated with ids {prev[0]}: {k} on {self.ex.name}")
                pm_ = pms.get(prev[0], (await Pm.get_or_none(name=prev[2])) or await Pm.get_or_none(identifier=prev[1]))
                await Pmex.update_or_create({"pm": pm_, "name": pm.name}, ex=self.ex, exid=k)
            elif prev[1] == norm:
                logging.error(f"Pm: {pm.name}&{prev[2]} overnormd as {norm} with ids {prev[0]}: {k} on {self.ex.name}")
                await Pmex.update_or_create(
                    {"pm": pms.get(prev[0], await Pm.get(name=prev[2]))}, ex=self.ex, exid=k, name=pm.name
                )
            else:
                pms[k], _ = await Pm.update_or_create(pm.model_dump(exclude_none=True), identifier=norm)
            prev = k, norm, pm.name
        # Pmexs
        pmexs = [Pmex(exid=k, ex=self.ex, pm=pm, name=pm.name) for k, pm in pms.items()]
        await Pmex.bulk_create(pmexs, ignore_conflicts=True)
        # Pmex banks
        for k, pm in pms_epyds.items():
            if banks := pm.banks:
                pmex = await Pmex.get(ex=self.ex, exid=k)  # pm=pms[k],
                for b in banks:
                    await PmexBank.update_or_create({"name": b.name}, exid=b.exid, pmex=pmex)

        # Curs
        cur_pyds: list[CurEpyd] = await self.curs()
        curs: dict[int | str, Cur] = {
            cur_pyd.exid: (await Cur.update_or_create({"rate": cur_pyd.rate}, ticker=cur_pyd.ticker))[0]
            for cur_pyd in cur_pyds
        }
        curexs: list[Curex] = [Curex(**c.model_dump(), cur=curs[c.exid], ex=self.ex) for c in cur_pyds]
        # Curex
        await Curex.bulk_create(curexs, update_fields=["minimum", "rounding_scale"], on_conflict=["cur_id", "ex_id"])

        cur2pms = await self.cur_pms_map()
        # # Link PayMethods with currencies
        pmcurs = set()
        for cur_id, exids in cur2pms.items():
            for exid in exids:
                pmcurs.add(
                    (
                        await Pmcur.update_or_create(
                            cur=curs[cur_id],
                            pm=pms.get(exid) or (await Pmex.get(ex=self.ex, exid=exid).prefetch_related("pm")).pm,
                        )
                    )[0]
                )
        # pmcurexs = [Pmcurex(pmcur=pmcur, ex=self.ex) for pmcur in pmcurs]
        # await Pmcurex.bulk_create(pmcurexs)

    # Импорт монет (с Coinex-ами) с биржи в бд
    async def set_coinexs(self):
        coins: list[CoinEpyd] = await self.coins()
        coins_db: dict[int, Coin] = {c.exid: (await Coin.update_or_create(ticker=c.ticker))[0] for c in coins}
        coinexs: list[Coinex] = [
            Coinex(coin=coins_db[c.exid], ex=self.ex, exid=c.exid, minimum=c.minimum) for c in coins
        ]
        await Coinex.bulk_create(coinexs, update_fields=["minimum"], on_conflict=["coin_id", "ex_id"])

    # Сохранение чужого объявления (с Pm-ами) в бд
    async def ad_pydin2db(self, ad_pydin: BaseAdPydIn) -> Ad:
        df, unq = ad_pydin.args()
        ad_db, _ = await Ad.update_or_create(df, **unq)
        if getattr(ad_pydin, "pms_", None):  # if it ListItem, not Full One # todo: remove?
            await ad_db.pms.add(*ad_pydin.pms_)
        return ad_db
