from types                                                                                              import NoneType
from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                          import Cache__Service__Client
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Exists    import Cache__Service__Client__File__Exists
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                       import fast_api__service__registry
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                         import register_cache_service__in_memory
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__Exists__Response                  import Schema__Cache__Exists__Response
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__File__Cache_Hash            import Safe_Str__Cache__File__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                      import Cache_Id


class test_Service__Fast_API__Client__File__Exists(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                    # Setup in-memory FastAPI client for testing
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.client__exists        = cls.cache_service_client.exists()
        cls.client__delete        = cls.cache_service_client.delete()
        cls.service_config        = fast_api__service__registry.config(Cache__Service__Client)
        cls.cache_service         = cls.service_config.fast_api.cache_service

        # Test data - create entries in test namespace
        cls.test_namespace     = "test-exists"
        cls.test_data_json     = {"test": "data", "number": 42}
        cls.test_data_string   = "test string content"

        # Store JSON entry
        cls.cache_hash_json    = cls.cache_service.hash_from_json(cls.test_data_json)
        cls.store_result_json  = cls.cache_service.store_with_strategy(storage_data = cls.test_data_json  ,
                                                                       cache_hash   = cls.cache_hash_json ,
                                                                       strategy     = "direct"            ,
                                                                       namespace    = cls.test_namespace  )
        cls.cache_id_json      = cls.store_result_json.cache_id

        # Store String entry
        cls.cache_hash_string  = cls.cache_service.hash_from_string(cls.test_data_string)
        cls.store_result_string = cls.cache_service.store_with_strategy(storage_data = cls.test_data_string  ,
                                                                        cache_hash   = cls.cache_hash_string ,
                                                                        strategy     = "direct"              ,
                                                                        namespace    = cls.test_namespace    )
        cls.cache_id_string    = cls.store_result_string.cache_id

        # Non-existent test data
        cls.non_existent_cache_id = Cache_Id()
        cls.non_existent_hash     = Safe_Str__Cache__File__Cache_Hash("0000000000000000")

    def test__setUpClass(self):
        with self.client__exists as _:
            assert type(_) is Cache__Service__Client__File__Exists

    # ═══════════════════════════════════════════════════════════════════════════
    # exists__cache_id tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__exists__cache_id__existing_json(self):                                # Test existing JSON entry
        with self.client__exists as _:
            result = _.exists__cache_id(cache_id  = self.cache_id_json  ,
                                        namespace = self.test_namespace)

            assert type(result)      is Schema__Cache__Exists__Response
            assert result.exists     is True
            assert result.cache_id   == self.cache_id_json
            assert result.namespace  == self.test_namespace
            assert result.cache_hash is None                                        # Not set for id-based check

    def test__exists__cache_id__existing_string(self):                              # Test existing String entry
        with self.client__exists as _:
            result = _.exists__cache_id(cache_id  = self.cache_id_string,
                                        namespace = self.test_namespace )

            assert type(result)    is Schema__Cache__Exists__Response
            assert result.exists   is True
            assert result.cache_id == self.cache_id_string
            assert result.namespace == self.test_namespace

    def test__exists__cache_id__non_existent(self):                                 # Test non-existent cache_id
        with self.client__exists as _:
            result = _.exists__cache_id(cache_id  = self.non_existent_cache_id,
                                        namespace = self.test_namespace       )

            assert type(result)    is NoneType

    def test__exists__cache_id__wrong_namespace(self):                              # Test namespace isolation
        with self.client__exists as _:
            result = _.exists__cache_id(cache_id  = self.cache_id_json    ,
                                        namespace = "different-namespace")

            assert type(result)    is Schema__Cache__Exists__Response
            assert result.exists   is False                                         # Exists in test_namespace, not here

    # ═══════════════════════════════════════════════════════════════════════════
    # exists__hash__cache_hash tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__exists__hash__cache_hash__existing_json(self):                        # Test existing JSON hash
        with self.client__exists as _:
            result = _.exists__hash__cache_hash(cache_hash = self.cache_hash_json ,
                                                namespace  = self.test_namespace  )

            assert type(result)      is Schema__Cache__Exists__Response
            assert result.exists     is True
            assert result.cache_hash == self.cache_hash_json
            assert result.namespace  == self.test_namespace
            assert result.cache_id   is None                                        # Not set for hash-based check

    def test__exists__hash__cache_hash__existing_string(self):                      # Test existing String hash
        with self.client__exists as _:
            result = _.exists__hash__cache_hash(cache_hash = self.cache_hash_string,
                                                namespace  = self.test_namespace   )

            assert type(result)      is Schema__Cache__Exists__Response
            assert result.exists     is True
            assert result.cache_hash == self.cache_hash_string
            assert result.namespace  == self.test_namespace

    def test__exists__hash__cache_hash__non_existent(self):                         # Test non-existent hash
        with self.client__exists as _:
            result = _.exists__hash__cache_hash(cache_hash = self.non_existent_hash,
                                                namespace  = self.test_namespace   )

            assert type(result)      is Schema__Cache__Exists__Response
            assert result.exists     is False
            assert result.cache_hash == self.non_existent_hash
            assert result.namespace  == self.test_namespace

    def test__exists__hash__cache_hash__wrong_namespace(self):                      # Test namespace isolation
        with self.client__exists as _:
            result = _.exists__hash__cache_hash(cache_hash = self.cache_hash_json   ,
                                                namespace  = "different-namespace"  )

            assert type(result)      is Schema__Cache__Exists__Response
            assert result.exists     is False                                       # Exists in test_namespace, not here

    # ═══════════════════════════════════════════════════════════════════════════
    # Combined and edge case tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__exists__both_methods_consistent(self):                                # Both methods should agree for same entry
        with self.client__exists as _:
            result_by_id   = _.exists__cache_id(cache_id  = self.cache_id_json ,
                                                namespace = self.test_namespace)
            result_by_hash = _.exists__hash__cache_hash(cache_hash = self.cache_hash_json,
                                                        namespace  = self.test_namespace )

            assert result_by_id.exists   is True
            assert result_by_hash.exists is True

    def test__exists__after_delete(self):                                           # Test existence after deletion
        # Create a temporary entry
        temp_data      = {"temp": "entry"}
        temp_hash      = self.cache_service.hash_from_json(temp_data)
        temp_namespace = "test-exists-delete"
        store_result   = self.cache_service.store_with_strategy(storage_data = temp_data     ,
                                                                cache_hash   = temp_hash     ,
                                                                strategy     = "direct"      ,
                                                                namespace    = temp_namespace)
        temp_cache_id  = store_result.cache_id

        with self.client__exists as _:
            # Verify it exists
            assert _.exists__cache_id(cache_id=temp_cache_id, namespace=temp_namespace).exists is True
            assert _.exists__hash__cache_hash(cache_hash=temp_hash, namespace=temp_namespace).exists is True

            # Delete it
            self.client__delete.delete__cache_id(cache_id=temp_cache_id, namespace=temp_namespace)

            # Verify it no longer exists
            assert _.exists__cache_id(cache_id=temp_cache_id, namespace=temp_namespace).exists is False
            assert _.exists__hash__cache_hash(cache_hash=temp_hash, namespace=temp_namespace).exists is False

    def test__exists__multiple_entries_same_namespace(self):                        # Test multiple entries in same namespace
        with self.client__exists as _:
            # Both entries from setUpClass should exist
            assert _.exists__cache_id(cache_id=self.cache_id_json,   namespace=self.test_namespace).exists is True
            assert _.exists__cache_id(cache_id=self.cache_id_string, namespace=self.test_namespace).exists is True

            # Their hashes should also exist
            assert _.exists__hash__cache_hash(cache_hash=self.cache_hash_json,   namespace=self.test_namespace).exists is True
            assert _.exists__hash__cache_hash(cache_hash=self.cache_hash_string, namespace=self.test_namespace).exists is True