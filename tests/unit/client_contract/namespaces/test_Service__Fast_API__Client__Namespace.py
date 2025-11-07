from unittest                                                                                           import TestCase
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                    import Serverless__Fast_API__Config
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                           import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client                           import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config                   import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Requests                 import Service__Fast_API__Client__Requests
from mgraph_ai_service_cache_client.client_contract.namespaces.Service__Fast_API__Client__Namespace     import Service__Fast_API__Client__Namespaces


class test_Service__Fast_API__Client__Namespace(TestCase):
    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing

        cls.serverless_config       = Serverless__Fast_API__Config       (enable_api_key = False                            )
        cls.cache_service__fast_api = Cache_Service__Fast_API            (config         = cls.serverless_config            ).setup()
        cls.server_config           = Service__Fast_API__Client__Config  ()
        cls.requests                = Service__Fast_API__Client__Requests(config         = cls.server_config                ,
                                                                          _app           = cls.cache_service__fast_api.app())
        cls.fast_api_client         = Service__Fast_API__Client          (config         = cls.server_config                ,
                                                                          _requests      = cls.requests                     )
        cls.cache_service           = cls.cache_service__fast_api.cache_service
        cls.namespaces              = cls.fast_api_client.namespaces()

    def test__setUpClass(self):
        with self.namespaces as _:
            assert type(_) is Service__Fast_API__Client__Namespaces

    def test_list(self):
        with self.namespaces as _:
            assert _.list() == []

            # add an entry with an entry
            test_data     = {"test": "data", "number": 42}
            namespace     = "test-namespaces"
            cache_hash    = self.cache_service.hash_from_json(test_data)
            store_result  = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                                  cache_hash   = cache_hash ,
                                                                  strategy     = "direct"   ,
                                                                  namespace    = namespace  )
            assert namespace in _.list()