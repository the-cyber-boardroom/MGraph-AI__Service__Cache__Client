from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                         import __
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                   import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client         import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.utils.Version                                                   import version__mgraph_ai_service_cache_client


class test_Cache__Service__Client(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cache_client = Client__Cache__Service()

    def test__init__(self):
        with self.cache_client as _:
            assert type(_       ) is Client__Cache__Service
            assert type(_.config) is Cache__Service__Fast_API__Client__Config

    def test_config(self):
        with Client__Cache__Service() as _:
            assert _.config.obj() == __(base_url        = None                                   ,
                                        api_key         = None                                   ,
                                        api_key_header  = None                                   ,
                                        fast_api_app    = None                                   ,
                                        mode            = 'in_memory'                            ,
                                        timeout         = 30                                     ,
                                        service_name    = 'Cache__Service__Fast_API'             ,
                                        service_version = version__mgraph_ai_service_cache_client)


    def test_client(self):
        with self.cache_client.client() as _:
            assert type(_) is Cache__Service__Fast_API__Client



