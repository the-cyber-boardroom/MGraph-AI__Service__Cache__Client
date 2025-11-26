from unittest                                                                                              import TestCase
from mgraph_ai_service_cache_client.client.client_contract.namespace.Service__Fast_API__Client__Namespace  import Service__Fast_API__Client__Namespace
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                          import client_cache_service


class test_Service__Fast_API__Client__Namespace(TestCase):
    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing

        cls.client_cache_service, cls.cache_service    = client_cache_service()
        cls.client__namespace                          = cls.client_cache_service.namespace()
        cls.test_data      = {"test": "data", "number": 42}
        cls.namespace      = "test-namespace"
        cls.cache_hash     = cls.cache_service.hash_from_json(cls.test_data)
        cls.store_result   = cls.cache_service.store_with_strategy(storage_data = cls.test_data  ,
                                                                   cache_hash   = cls.cache_hash ,
                                                                   strategy     = "direct"       ,
                                                                   namespace    = cls.namespace  )
        cls.cache_id        = cls.store_result.cache_id

    def test__setUpClass(self):
        with self.client__namespace as _:
            assert type(_) is Service__Fast_API__Client__Namespace

    # todo: BUG: rename file_hashes to cache_hashes     (after client refactor)
    def test_file_hashes(self):
        with self.client__namespace as _:
            assert _.file_hashes(namespace = self.namespace) == [self.cache_hash]

    # todo: BUG: rename file_ids to cache_ids     (after client refactor)
    def test_file_ids(self):
        with self.client__namespace as _:
            assert _.file_ids(namespace = self.namespace) == [self.cache_id]

            # add an entry with an entry


