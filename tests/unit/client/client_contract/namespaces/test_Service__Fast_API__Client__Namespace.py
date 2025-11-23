from unittest                                                                                              import TestCase
from mgraph_ai_service_cache_client.client.client_contract.namespaces.Service__Fast_API__Client__Namespace import Service__Fast_API__Client__Namespaces
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                          import client_cache_service


class test_Service__Fast_API__Client__Namespace(TestCase):
    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing

        # cls.serverless_config       = Serverless__Fast_API__Config              (enable_api_key = False                            )
        # cls.cache_service__fast_api = Cache_Service__Fast_API                   (config         = cls.serverless_config            ).setup()
        # cls.server_config           = Cache__Service__Fast_API__Client__Config  ()
        # cls.requests                = Cache__Service__Fast_API__Client__Requests(config    = cls.server_config                ,
        #                                                                          _app      = cls.cache_service__fast_api.app())
        # cls.fast_api_client         = Cache__Service__Fast_API__Client          (config    = cls.server_config,
        #                                                                          _requests = cls.requests)
        # cls.cache_service           = cls.cache_service__fast_api.cache_service

        cls.client_cache_service, cls.cache_service    = client_cache_service()
        cls.namespaces                                 = cls.client_cache_service.namespaces()

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