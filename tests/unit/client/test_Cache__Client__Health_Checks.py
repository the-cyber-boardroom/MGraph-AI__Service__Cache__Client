from unittest                                                                                         import TestCase

import pytest
from osbot_utils.testing.__                                                                           import __, __SKIP__
from osbot_utils.utils.Env                                                                            import load_dotenv
from mgraph_ai_service_cache_client.client.Cache__Client__Config                                      import Cache__Client__Config
from mgraph_ai_service_cache_client.client.Cache__Client__Health_Checks                               import Cache__Client__Health_Checks
from mgraph_ai_service_cache_client.schemas.client.health_checks.Client__Check__Target_Server__Auth   import Client__Check__Target_Server__Auth
from mgraph_ai_service_cache_client.schemas.client.health_checks.Client__Check__Target_Server__Status import Client__Check__Target_Server__Status


class test_Cache__Client__Health_Checks(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pytest.skip("test requires live server which is current in a crashed state (due to missing schema dependency")
        load_dotenv()                                               # todo: remove once we have main test class for the non-fastapi client api
        cls.client_health_checks = Cache__Client__Health_Checks()

    def test__setUpClass(self):
        with self.client_health_checks as _:
            assert type(_      ) is Cache__Client__Health_Checks
            assert type(_.config) is Cache__Client__Config

    def test_check__target_server__status(self):
        with self.client_health_checks as _:
            result = _.check__target_server__status()
            assert type(result) is Client__Check__Target_Server__Status
            assert result.obj() == __(duration      = __SKIP__                     ,
                                      success       = True                         ,
                                      target_server = 'https://cache.dev.mgraph.ai',
                                      timestamp     = __SKIP__                     )

    def test_check__target_server__auth(self):
        with self.client_health_checks as _:
            result = _.check__target_server__auth()
            assert type(result) is Client__Check__Target_Server__Auth
            assert result.obj() == __(found_key_name             = True  ,
                                      found_key_value            = True  ,
                                      key_valid_in_target_server = True )