import json
import os
import subprocess
from asyncio import run

from x_model import init_db
from xync_client.Abc.Base import DictOfDicts
from xync_schema import models
from xync_schema.models import Cur, Ex

from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN


class ExClient(BaseExClient):
    headers = {
        "accept-language": "ru,en;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "deviceid": "883e1394d8a2278418b6f02804df16c4",
    }

    async def curs(self) -> dict[str, str]:
        curs = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["fiatInfoRespList"]
        return {cur["fiatCode"]: cur["fiatCode"] for cur in curs}

    async def coins(self, cur: Cur = None) -> dict[str, str]:
        coins = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["coinInfoRespList"]
        return {coin["coinCode"]: coin["coinCode"] for coin in coins}

    async def pms(self) -> DictOfDicts:  # {pm.exid: pm}
        for id_, cur in (await self.curs()).items():
            pref = "../xync_client/BitGet/" if os.getcwd().split("/")[-1] == "tests" else ""
            data = {"fiatCode": cur, "languageType": 6}
            p = subprocess.Popen(
                [
                    "node",
                    pref + "req.mjs",
                    "pub/currency/query-popular-paymethod",
                    json.dumps(data, separators=(",", ":")),
                    json.dumps(self.headers, separators=(",", ":")),
                ],
                stdout=subprocess.PIPE,
            )
            out = p.stdout.read().decode()
            pms: list[dict] = json.loads(out)

        pmcurs = {pm["fiatCode"]: pm["paymethodInfo"] for pm in pms}
        pp = {}
        [
            [pp.update({int(p["paymethodId"]): {"name": p["paymethodName"], "logo": p.get("iconUrl")}}) for p in ps]
            for ps in pmcurs.values()
        ]
        return pp

    async def ads(self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[int] = None) -> list[dict]:
        slots = (
            await self._post(
                "/v1/p2p/pub/adv/queryAdvList",
                data={
                    "side": 2 if is_sell else 1,
                    "pageNo": 1,
                    "pageSize": 3,
                    "coinCode": coin_exid,
                    "fiatCode": cur_exid,
                    "languageType": 6,
                    "paymethodId": pm_exids[0] if pm_exids else None,
                },
            )
        )["data"]["dataList"]
        result = []
        for slot in slots:
            result.append(
                {
                    "price": float(slot["priceValue"]),
                    "min_fiat": float(slot["minAmount"]),
                    "max_fiat": float(min(slot["maxAmount"], slot["amount"])),
                    "user": int(slot["userId"]) if slot["userId"] else None,
                    "pms": [int(pay_method["paymethodId"]) for pay_method in slot["paymethodInfo"]],
                }
            )
        return result

    async def cur_pms_map(self) -> dict[str, list[int]]:
        curs = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["fiatInfoRespList"]
        return {
            cur["fiatCode"]: [int(pay_method["paymethodId"]) for pay_method in cur["paymethodInfo"]] for cur in curs
        }


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="BitGet")
    cl = ExClient(bg)
    # await cl.curs()
    # await cl.coins()
    # await cl.ads("BTC", "RUB", True, [1, 289, 375])
    await cl.pms()
    # await cl.cur_pms_map()
    await cl.set_pmcurexs()
    await cl.set_coinexs()
    await cl.close()


if __name__ == "__main__":
    run(main())
