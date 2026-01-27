from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                          import Cache__Service__Client
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                       import fast_api__service__registry
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                         import register_cache_service__in_memory
from mgraph_ai_service_cache_client.client.client_contract.namespace.Cache__Service__Client__Namespaces import Cache__Service__Client__Namespaces


class test_Service__Fast_API__Client__Namespaces(TestCase):
    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.namespaces            = cls.cache_service_client.namespaces()
        cls.service_config        = fast_api__service__registry.config(Cache__Service__Client)
        cls.cache_service         = cls.service_config.fast_api.cache_service

    def test__setUpClass(self):
        with self.namespaces as _:
            assert type(_) is Cache__Service__Client__Namespaces

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