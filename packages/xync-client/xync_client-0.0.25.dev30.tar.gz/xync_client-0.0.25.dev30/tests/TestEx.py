import logging

import pytest
from xync_schema.pydantic import PmPyd, BaseAd, CurEpyd, CoinEpyd

from xync_client.Abc.BaseTest import BaseTest
from xync_schema.enums import ExStatus, ExType, ExAction
from xync_schema.models import Ex, TestEx as ExTest

from xync_client.Abc.Base import BaseClient, FlatDict, MapOfIdsList
from xync_client.Abc.Ex import BaseExClient


@pytest.mark.asyncio(loop_scope="session")
class TestEx(BaseTest):
    ad: dict[str, BaseAd] = {}

    @pytest.fixture
    async def clients(self) -> list[BaseClient]:
        exs = await Ex.filter(status__gt=ExStatus.plan)
        [await ex.fetch_related("actors__agent") for ex in exs if ex.type_ == ExType.tg]
        clients: list[BaseExClient] = [ex.client() for ex in exs]
        yield clients
        [await cl.close() for cl in clients]

    # 19
    async def test_curs(self, clients: list[BaseExClient]):
        for client in clients:
            curs: list[CurEpyd] = await client.curs()
            ok = self.is_list_of_objects(curs, CurEpyd)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.curs)
            assert t.ok, "No curs"
            logging.info(f"{client.ex.name}: {ExAction.curs.name} - ok")

    # 20
    async def test_pms(self, clients: list[BaseExClient]):
        for client in clients:
            pms: dict[int | str, PmPyd] = await client.pms()
            ok = self.is_dict_of_objects(pms, PmPyd)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.pms)
            assert t.ok, "No pms"
            logging.info(f"{client.ex.name}: {ExAction.pms.name} - ok")

    # 21
    async def test_cur_pms_map(self, clients: list[BaseExClient]):
        for client in clients:
            cur_pms: MapOfIdsList = await client.cur_pms_map()
            ok = self.is_map_of_ids(cur_pms)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.cur_pms_map)
            assert t.ok, "No pms for cur"
            logging.info(f"{client.ex.name}: {ExAction.cur_pms_map.name} - ok")

    # 22
    async def test_coins(self, clients: list[BaseExClient]):
        for client in clients:
            coins: FlatDict = await client.coins()
            ok = self.is_list_of_objects(coins, CoinEpyd)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.coins)
            assert t.ok, "No coins"
            logging.info(f"{client.ex.name}: {ExAction.coins.name} - ok")

    # 23
    async def test_pairs(self, clients: list[BaseExClient]):
        for client in clients:
            pairs: MapOfIdsList = await client.pairs()
            ok = self.is_map_of_ids(pairs)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.pairs)
            assert t.ok, "No coins"
            logging.info(f"{client.ex.name}: {ExAction.pairs.name} - ok")

    # 24
    async def test_ads(self, clients: list[BaseExClient]):
        for client in clients:
            ads: list[BaseAd] = await client.ads("USDT", "RUB", False)
            ok = self.is_list_of_objects(ads, BaseAd)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.ads)
            assert t.ok, "No ads"
            self.ad[client.ex.name] = ads[0]  # for further use in test_ad
            logging.info(f"{client.ex.name}: {ExAction.ads.name} - ok")

    # 42
    async def test_ad(self, clients: list[BaseExClient]):
        for client in clients:
            ad: BaseAd = await client.ad(self.ad.get(client.ex.name, (await client.ads("USDT", "RUB", False))[0]).id)
            ok = isinstance(ad, BaseAd)
            t, _ = await ExTest.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.ad)
            assert t.ok, "No ad"
            logging.info(f"{client.ex.name}: {ExAction.ad.name} - ok")
