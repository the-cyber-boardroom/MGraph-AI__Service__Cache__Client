from unittest                                                                 import TestCase
from osbot_utils.testing.__                                                   import __
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client import Service__Fast_API__Client


class test_Service__Fast_API__Client(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fast_api_client = Service__Fast_API__Client()

    def test__init__(self):
        with self.fast_api_client as _:
            assert type(_)         == Service__Fast_API__Client
            assert _.config.obj()  == __(base_url       = 'http://localhost:8000',
                                        api_key         = None                   ,
                                        api_key_header  = 'X-API-Key'            ,
                                        timeout         = 30                     ,
                                        verify_ssl      = True                   ,
                                        service_name    = 'Service__Fast_API'    ,
                                        service_version = 'v0.5.67'              )