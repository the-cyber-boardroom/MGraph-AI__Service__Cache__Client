from unittest                                                                 import TestCase
from osbot_fast_api.utils.Fast_API_Server                                     import Fast_API_Server
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config          import Serverless__Fast_API__Config
from osbot_utils.helpers.duration.decorators.capture_duration                 import capture_duration
from osbot_utils.testing.__ import __
from osbot_utils.utils.Http                                                   import GET_json
from mgraph_ai_service_cache.fast_api.Service__Fast_API                       import Service__Fast_API
from mgraph_ai_service_cache.utils.Version                                    import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config import Service__Fast_API__Client__Config


class test_Service__Fast_API__Client__local(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with capture_duration() as duration:
            cls.serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)
            cls.cache_service__fast_api = Service__Fast_API(config=cls.serverless_config).setup()
            cls.fast_api_server         = Fast_API_Server(app=cls.cache_service__fast_api.app())
            cls.server_url              = cls.fast_api_server.url()

            cls.server_config           = Service__Fast_API__Client__Config(base_url=cls.server_url, verify_ssl=False)
            cls.fast_api_client         = Service__Fast_API__Client        (config=cls.server_config)

            cls.fast_api_server.start()

        assert duration.seconds < 0.5               # server setup and start should not take more than 0.5 (locally takes about 0.25)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fast_api_server.stop()

    def test__local_server(self):
        assert self.fast_api_server.running is True
        assert GET_json(self.server_url + 'info/health' ) == { 'status'     : 'ok'                            }
        assert GET_json(self.server_url + 'info/status' ) == { 'environment': 'local'                         ,
                                                               'name'       : 'mgraph_ai_service_cache'       ,
                                                               'status'     : 'operational'                   ,
                                                               'version'    : version__mgraph_ai_service_cache}
    def test__init__(self):
        with self.fast_api_client as _:
            assert _.config.obj() == __(base_url       = self.server_url    ,
                                       api_key         = None               ,
                                       api_key_header  = 'X-API-Key'        ,
                                       timeout         = 30                 ,
                                       verify_ssl      = False              ,
                                       service_name    ='Service__Fast_API' ,
                                       service_version = 'v0.5.67'          )

    def test_info(self):
        with self.fast_api_client.info() as _:
            assert _.health() == { 'status'     : 'ok'                             }
            assert _.status() == { 'environment': 'local'                          ,
                                   'name'       : 'mgraph_ai_service_cache'        ,
                                   'status'     : 'operational'                    ,
                                   'version'    : version__mgraph_ai_service_cache }