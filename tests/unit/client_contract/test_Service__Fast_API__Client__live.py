from unittest                                                                            import TestCase

import pytest
from osbot_utils.testing.__                                                              import __
from osbot_utils.utils.Env                                                               import get_env
from mgraph_ai_service_cache.utils.Version                                               import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.client_builder.Fast_API__Client__Builder             import Fast_API__Client__Builder
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client            import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.info.Service__Fast_API__Client__Info import Service__Fast_API__Client__Info
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                  import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE, ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME, ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE


# todo: add tests that hit a local ephemeral server (started using Fast_API__Server)
# todo: move this tests to integration tests (since it is going to be hitting a live server
class test_Service__Fast_API__Client__live(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        #pytest.skip("test requires live server which is current in a crashed state (due to missing schema dependency")
        cls.fast_api_client         = Service__Fast_API__Client()
        cls.fast_api_client_builder = Fast_API__Client__Builder()
        cls.server_details          = cls.fast_api_client_builder.server_details()
        assert cls.server_details.configured is True, "Server details need to be configured for this test to run"

        cls.fast_api_client_builder.configure_client(cls.fast_api_client)


    def test__init__(self):
        api_key        = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE)
        api_key_header = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME )
        base_url       = get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            )
        with self.fast_api_client as _:
            assert type(_)         == Service__Fast_API__Client
            assert _.config.obj()  == __(base_url        = base_url               ,
                                         api_key         = api_key                ,     # todo: name field to: key_name
                                         api_key_header  = api_key_header         ,     # todo: name field to: key_value
                                         timeout         = 30                     ,
                                         verify_ssl      = True                   ,
                                         service_name    = 'Service__Fast_API'    ,
                                         service_version = 'v0.5.67'              )
            assert type(_.info()) == Service__Fast_API__Client__Info

    def test__make_request(self):

        with self.fast_api_client.info() as _:
            assert _.health () == { 'status': 'ok'}
            assert _.status () == { 'environment': 'aws-lambda'                     ,
                                    'name'       : 'mgraph_ai_service_cache'        ,
                                    'status'     : 'operational'                    ,
                                    'version'    : version__mgraph_ai_service_cache }