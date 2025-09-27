from unittest                                                                                         import TestCase
from osbot_utils.testing.__                                                                           import __, __SKIP__
from mgraph_ai_service_cache_client.client.Cache__Client__Config                                      import Cache__Client__Config
from mgraph_ai_service_cache_client.client.Cache__Client__Health_Checks                               import Cache__Client__Health_Checks
from mgraph_ai_service_cache_client.schemas.client.health_checks.Cache__Client__Health_Checks__Status import Cache__Client__Health_Checks__Status


class test_Cache__Client__Health_Checks(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client_health_checks = Cache__Client__Health_Checks()

    def test__setUpClass(self):
        with self.client_health_checks as _:
            assert type(_      ) is Cache__Client__Health_Checks
            assert type(_.config) is Cache__Client__Config

    def test_check__target_server__status(self):
        with self.client_health_checks as _:
            result = _.check__target_server__status()
            assert type(result) is Cache__Client__Health_Checks__Status
            assert result.obj() == __(duration      = __SKIP__                     ,
                                      success       = True                         ,
                                      target_server = 'https://cache.dev.mgraph.ai',
                                      timestamp     = __SKIP__                     )