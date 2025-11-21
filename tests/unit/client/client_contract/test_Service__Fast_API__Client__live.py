import pytest
from unittest                                                                                   import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.utils.Env                                                                      import get_env
from mgraph_ai_service_cache.utils.Version                                                      import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client     import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_contract.info.Service__Fast_API__Client__Info import Service__Fast_API__Client__Info
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                         import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE, ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME, ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE
from mgraph_ai_service_cache_client.utils.Version import version__mgraph_ai_service_cache_client


# todo: add tests that hit a local ephemeral server (started using Fast_API__Server)
# todo: move this tests to integration tests (since it is going to be hitting a live server

# todo: add integration tests that hit the live cache.dev.mgraph.ai server

class test_Service__Fast_API__Client__live(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pytest.skip("test needs refactoring once the new Cache_Service__Client is setup")
        if get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE) is None:
            pytest.skip("Test needs URL__TARGET_SERVER__CACHE_SERVICE env var set")

        cls.fast_api_client         = Cache__Service__Fast_API__Client()
        #cls.fast_api_client_builder = Fast_API__Client__Builder()
        #cls.server_details          = cls.fast_api_client_builder.server_details()
        #assert cls.server_details.configured is True, "Server details need to be configured for this test to run"

        #cls.fast_api_client_builder.configure_client(cls.fast_api_client)


    def test__init__(self):
        api_key        = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE)
        api_key_header = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME )
        base_url       = get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            )

        with self.fast_api_client as _:
            assert type(_) == Cache__Service__Fast_API__Client
            assert _.config.obj()  == __(base_url        = base_url                               ,
                                         api_key         = api_key                                ,     # todo: name field to: key_name
                                         api_key_header  = api_key_header                         ,     # todo: name field to: key_value
                                         timeout         = 30                                     ,
                                         service_name    = 'Cache__Service__Fast_API'             ,
                                         service_version = version__mgraph_ai_service_cache_client)
            assert type(_.info()) == Service__Fast_API__Client__Info

    def test__make_request(self):

        with self.fast_api_client.info() as _:
            assert _.health () == { 'status': 'ok'}
            assert _.status () == { 'environment': 'aws-lambda'                            ,
                                    'name'       : 'mgraph_ai_service_cache'               ,
                                    'status'     : 'operational'                           ,
                                    'version'    : version__mgraph_ai_service_cache_client }