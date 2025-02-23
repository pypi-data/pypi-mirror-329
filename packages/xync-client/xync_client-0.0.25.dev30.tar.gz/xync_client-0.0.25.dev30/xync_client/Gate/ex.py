import re
from asyncio import run, sleep
from json import JSONDecoder

from bs4 import BeautifulSoup, Script
from x_model import init_db
from xync_schema import models
from xync_schema.models import Coin, Cur, Pm, Ex

from xync_client.Abc.Base import MapOfIdsList, DictOfDicts, FlatDict, ListOfDicts
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN


class ExClient(BaseExClient):
    # 20: Список всех платежных методов на бирже
    async def pms(self, cur: Cur = None) -> DictOfDicts:
        await sleep(1)
        doc = await self._get("/p2p")
        await sleep(1)
        soup = BeautifulSoup(doc, "html.parser")
        script: Script = soup.body.find_all("script")[17]  # 17-th not stable
        strng = (
            script.get_text(strip=True)
            .replace("\n", "")
            .replace("  ", "")
            .replace(
                ',\'bank\': {image: "/images/payment/bank.png",index: "2",pay_name: lang_string("银行卡"),pay_type: "bank",rgb: "#FF860D",}',
                "",
            )
        )
        # pattern = r'var c2cData = (\{.*?\})\s+var transLang'
        # pattern = r'payment_settings:\s{1}(\{.*?\}),\s?// 用户放开的支付方式'
        pattern = r"payment_settings:\s{1}(\{.*?\}),paymentIdMap:"
        match = re.search(pattern, strng.replace(",}", "}").replace(",]", "]"), re.DOTALL)
        res = match.group(1)
        pms = JSONDecoder(strict=False).decode(res)
        return {
            pm["index"]: {"name": pm["pay_name"], "logo": pm["image"], "identifier": idf, "type_": pm["base_type"]}
            for idf, pm in pms.items()
        }

    # 21: Список поддерживаемых валют
    async def coins(self, cur: Cur = None) -> FlatDict: ...

    # 22: Списки поддерживаемых платежек по каждой валюте
    async def cur_pms_map(self) -> MapOfIdsList:
        pass

    # 23: Монеты на Gate
    async def curs(self) -> FlatDict:
        curs = await self._post("/json_svr/buy_crypto_fiat_setting")
        curs = {cur["fiat"]: cur["fiat"] for cur in curs["datas"] if cur["p2p"]}
        return curs

    # 24: ads
    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> ListOfDicts:
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="Gate")
    cl = ExClient(bg)
    await cl.curs()
    # await cl.coins()
    pms = await cl.pms()
    print(pms)


if __name__ == "__main__":
    run(main())
