from unittest                                                                                   import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                  import Cache__Service__Client
from mgraph_ai_service_cache_client.client.client_contract.namespace.Cache__Service__Client__Namespace import Cache__Service__Client__Namespace
from osbot_fast_api.services.registry.Fast_API__Service__Registry                               import fast_api__service__registry
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                 import register_cache_service__in_memory
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__File__Cache_Hash    import Safe_Str__Cache__File__Cache_Hash


class test_Service__Fast_API__Client__Namespace(TestCase):
    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing

        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.client__namespace     = cls.cache_service_client.namespace()
        cls.client__delete        = cls.cache_service_client.delete()
        cls.service_config        = fast_api__service__registry.config(Cache__Service__Client)
        cls.cache_service         = cls.service_config.fast_api.cache_service

        cls.test_data             = {"test": "data", "number": 42}
        cls.namespace             = "test-namespace"
        cls.cache_hash            = cls.cache_service.hash_from_json(cls.test_data)
        cls.store_result          = cls.cache_service.store_with_strategy(storage_data = cls.test_data  ,
                                                                          cache_hash   = cls.cache_hash ,
                                                                          strategy     = "direct"       ,
                                                                          namespace    = cls.namespace  )
        cls.cache_id               = cls.store_result.cache_id

    def test__setUpClass(self):
        with self.client__namespace as _:
            assert type(_) is Cache__Service__Client__Namespace

    def test_cache_hashes(self):
        with self.client__namespace as _:
            assert type(self.cache_hash) is Safe_Str__Cache__File__Cache_Hash
            assert _.cache_hashes(namespace = self.namespace) == [self.cache_hash]

    def test_cache_ids(self):
        with self.client__namespace as _:
            assert _.cache_ids(namespace = self.namespace) == [self.cache_id]

            self.client__delete.delete__cache_id(cache_id = self.cache_id, namespace = self.namespace)

            assert _.cache_ids   (namespace = self.namespace) == []
            assert _.cache_hashes(namespace = self.namespace) == []



