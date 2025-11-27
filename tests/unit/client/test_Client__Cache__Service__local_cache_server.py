from unittest                                                                                  import TestCase
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                  import Cache_Service__Fast_API
from osbot_utils.utils.Misc                                                                    import random_text
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client    import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Retrieve__Success             import Schema__Cache__Retrieve__Success
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy           import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.utils.Version                                              import version__mgraph_ai_service_cache_client
from osbot_utils.testing.__                                                                    import __, __SKIP__
from mgraph_ai_service_cache_client.client.Client__Cache__Service                              import Client__Cache__Service
from osbot_fast_api.utils.Fast_API_Server                                                      import Fast_API_Server
from osbot_utils.testing.Temp_Env_Vars                                                         import Temp_Env_Vars


class test_Client__Cache__Service__local_cache_server(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key_name            = random_text("api_key_name" , lowercase=True)
        cls.api_key_value           = random_text("api_key_value", lowercase=True)
        cls.env_vars__cache_service = dict(FAST_API__AUTH__API_KEY__NAME                 =  cls.api_key_name    ,
                                           FAST_API__AUTH__API_KEY__VALUE                =  cls.api_key_value   )
        cls.auth_headers            = { cls.api_key_name: cls.api_key_value }

        # setup temp cache service running on ephemeral Fast_API
        with Temp_Env_Vars(env_vars=cls.env_vars__cache_service):
            cls.cache_service__fast_api = Cache_Service__Fast_API().setup()
            cls.cache_service__app      = cls.cache_service__fast_api.app()
            cls.fast_api_server         = Fast_API_Server(app=cls.cache_service__app)
            cls.cache_server_url        = cls.fast_api_server.url()
            cls.fast_api_server.start()

        cls.env_vars__cache_client = dict(AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME  =  cls.api_key_name    ,
                                          AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE = cls.api_key_value    ,
                                          URL__TARGET_SERVER__CACHE_SERVICE             = cls.cache_server_url )

        # setup client cache service
        with Temp_Env_Vars(env_vars=cls.env_vars__cache_client ):
            cls.client_cache_service = Client__Cache__Service()
            cls.requests             = cls.client_cache_service.client().requests()                # the .requests() will call .setup_config_from_env() which will wire up the env_vars tested below (which is a singleton)

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()

    def test__cache_server(self):
        assert self.fast_api_server.running is True
        assert self.fast_api_server.requests_get(path    = '/info/health'   ,
                                                 headers = self.auth_headers).status_code == 200

    def test__client_cache_service__cache_server_setup(self):
        with self.client_cache_service as _:
            assert type(_         )       is Client__Cache__Service
            assert type(_.client())       is Cache__Service__Fast_API__Client
            assert _.client().requests()  == self.requests                              # confirm we get the same object
            assert _.obj()                == __(config=__(base_url         = self.cache_server_url     ,
                                                          api_key          = self.api_key_value        ,
                                                          api_key_header   = self.api_key_name         ,
                                                          mode             = 'remote'                  ,
                                                          fast_api_app     = None                      ,
                                                          timeout          = 30                        ,
                                                          service_name     = 'Cache__Service__Fast_API',
                                                          service_version  = version__mgraph_ai_service_cache_client))

    def test__client_workflow(self):

        with self.client_cache_service.client() as _:
            assert _.namespaces().list() == []

            namespace        = 'local-cache-server'
            store_response   = _.store().store__string(strategy  = Enum__Cache__Store__Strategy.DIRECT ,
                                                       namespace = namespace                           ,
                                                       body      = 'the answer is 43-1'                )
            cache_id         = store_response.cache_id
            cache_hash       = store_response.cache_hash

            path             = f"/{namespace}/retrieve/{cache_id}"
            result           = self.fast_api_server.requests_get(path    = path            ,
                                                                 headers = self.auth_headers).json()
            retrieve_success = Schema__Cache__Retrieve__Success.from_json(result)

            assert _.namespaces().list()  == [namespace]
            assert cache_hash             == '47108d2fe2a1e063'
            assert retrieve_success.obj() == __(data     =  'the answer is 43-1'                   ,
                                                metadata = __(cache_id         = cache_id          ,
                                                              cache_hash       = '47108d2fe2a1e063',
                                                              cache_key        = ''                ,
                                                              file_id          = cache_id          ,
                                                              namespace        = namespace         ,
                                                              strategy         = 'direct'          ,
                                                              stored_at        = __SKIP__          ,
                                                              file_type        = 'json'            ,
                                                              content_encoding = None              ,
                                                              content_size     = 0                 ),
                                                data_type ='string')
