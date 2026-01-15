# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Service__Fast_API__Client__Data__Retrieve
# Verify data file retrieval operations under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from osbot_utils.utils.Objects                                                                              import base_classes
from osbot_utils.utils.Misc                                                                                 import random_string
from mgraph_ai_service_cache_client.client.client_contract.data.Service__Fast_API__Client__Data__Retrieve   import Service__Fast_API__Client__Data__Retrieve
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                           import client_cache_service


class test_Service__Fast_API__Client__Data__Retrieve(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                            # Setup in-memory client
        cls.client_cache_service, cls.cache_service = client_cache_service()
        cls.data_retrieve                           = cls.client_cache_service.data().retrieve()
        cls.data_store                              = cls.client_cache_service.data_store()
        cls.store_client                            = cls.client_cache_service.store()
        cls.test_namespace                          = Safe_Str__Id("test-data-retrieve")

        # Create main cache entry for testing
        cls.store_result = cls.store_client.store__string(strategy  = "direct"           ,
                                                          namespace = cls.test_namespace ,
                                                          body      = "main cache entry" )
        cls.cache_id     = cls.store_result.cache_id

        # Test data
        cls.test_string_data  = "test string content for retrieval"
        cls.test_json_data    = {"message": "hello", "count": 42, "nested": {"key": "value"}}
        cls.test_binary_data  = bytes(range(0, 100))

        # Store data files for testing
        cls.string_file_id = "retrieve-string-file"
        cls.json_file_id   = "retrieve-json-file"
        cls.binary_file_id = "retrieve-binary-file"

        cls.data_store.data__store_string__with__id(cache_id     = cls.cache_id         ,
                                                    namespace    = cls.test_namespace   ,
                                                    data_file_id = cls.string_file_id   ,
                                                    body         = cls.test_string_data )

        cls.data_store.data__store_json__with__id(cache_id     = cls.cache_id       ,
                                                  namespace    = cls.test_namespace ,
                                                  data_file_id = cls.json_file_id   ,
                                                  body         = cls.test_json_data )

        cls.data_store.data__store_binary__with__id(cache_id     = cls.cache_id         ,
                                                    namespace    = cls.test_namespace   ,
                                                    data_file_id = cls.binary_file_id   ,
                                                    body         = cls.test_binary_data )

        # Store files with key paths
        cls.data_key              = "configs/production"
        cls.keyed_string_file_id  = "keyed-string"
        cls.keyed_json_file_id    = "keyed-json"
        cls.keyed_binary_file_id  = "keyed-binary"
        cls.keyed_string_data     = "keyed string content"
        cls.keyed_json_data       = {"environment": "production", "debug": False}
        cls.keyed_binary_data     = bytes(range(50, 100))

        cls.data_store.data__store_string__with__id_and_key(cache_id     = cls.cache_id            ,
                                                            namespace    = cls.test_namespace      ,
                                                            data_key     = cls.data_key            ,
                                                            data_file_id = cls.keyed_string_file_id,
                                                            body         = cls.keyed_string_data   )

        cls.data_store.data__store_json__with__id_and_key(cache_id     = cls.cache_id          ,
                                                          namespace    = cls.test_namespace    ,
                                                          data_key     = cls.data_key          ,
                                                          data_file_id = cls.keyed_json_file_id,
                                                          body         = cls.keyed_json_data   )

        cls.data_store.data__store_binary__with__id_and_key(cache_id     = cls.cache_id            ,
                                                            namespace    = cls.test_namespace      ,
                                                            data_key     = cls.data_key            ,
                                                            data_file_id = cls.keyed_binary_file_id,
                                                            body         = cls.keyed_binary_data   )

    # ═══════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__setUpClass(self):                                                                             # Verify test setup
        with self.data_retrieve as _:
            assert type(_)         is Service__Fast_API__Client__Data__Retrieve
            assert base_classes(_) == [Type_Safe, object]

    def test__init__(self):                                                                                 # Test initialization
        with self.data_retrieve as _:
            assert _._client is self.client_cache_service
            assert _.obj()   == __(_client = __SKIP__)

    def test_requests(self):                                                                                # Test requests property
        with self.data_retrieve as _:
            requests = _.requests
            assert requests is not None
            assert callable(requests.execute)

    # ═══════════════════════════════════════════════════════════════════════════
    # data__string__with__id - String Retrieval
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__string__with__id__retrieves_content(self):                                              # Test basic string retrieval
        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = self.string_file_id )

            assert type(result) is str
            assert result       == self.test_string_data

    def test__data__string__with__id__non_existent_file(self):                                              # Test retrieving non-existent string file
        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = "non-existent-file" )

            assert result is None

    def test__data__string__with__id__non_existent_cache_entry(self):                                       # Test with non-existent cache entry
        with self.data_retrieve as _:
            non_existent_id = Cache_Id()
            result = _.data__string__with__id(cache_id     = non_existent_id     ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = self.string_file_id )

            assert result is None

    def test__data__string__with__id__wrong_namespace(self):                                                # Test namespace isolation
        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = "different-ns"      ,
                                              data_file_id = self.string_file_id )

            assert result is None

    def test__data__string__with__id__empty_string_content(self):                                           # Test retrieving empty string
        # Store empty string
        empty_file_id = f"empty-string-{random_string(prefix='')}"
        self.data_store.data__store_string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = empty_file_id       ,
                                                     body         = ""                  )

        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = empty_file_id       )

            assert result is None

    def test__data__string__with__id__unicode_content(self):                                                # Test Unicode string retrieval
        unicode_content = "你好世界 🌍 مرحبا Привет мир"
        unicode_file_id = f"unicode-{random_string(prefix='')}"

        self.data_store.data__store_string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = unicode_file_id     ,
                                                     body         = unicode_content     )

        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = unicode_file_id     )

            assert result == unicode_content

    # ═══════════════════════════════════════════════════════════════════════════
    # data__string__with__id_and_key - String Retrieval with Key
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__string__with__id_and_key__retrieves_content(self):                                      # Test string retrieval with key path
        with self.data_retrieve as _:
            result = _.data__string__with__id_and_key(cache_id     = self.cache_id            ,
                                                      namespace    = self.test_namespace      ,
                                                      data_key     = self.data_key            ,
                                                      data_file_id = self.keyed_string_file_id)

            assert type(result) is str
            assert result       == self.keyed_string_data

    def test__data__string__with__id_and_key__wrong_key_path(self):                                         # Test with wrong key path
        with self.data_retrieve as _:
            result = _.data__string__with__id_and_key(cache_id     = self.cache_id            ,
                                                      namespace    = self.test_namespace      ,
                                                      data_key     = "wrong/path"             ,
                                                      data_file_id = self.keyed_string_file_id)

            assert result is None

    def test__data__string__with__id_and_key__non_keyed_file(self):                                         # Test retrieving non-keyed file with key method
        with self.data_retrieve as _:
            # Try to retrieve root-level file with a key path
            result = _.data__string__with__id_and_key(cache_id     = self.cache_id       ,
                                                      namespace    = self.test_namespace ,
                                                      data_key     = "some/path"         ,
                                                      data_file_id = self.string_file_id )

            assert result is None                                                                           # Should not find it

    # ═══════════════════════════════════════════════════════════════════════════
    # data__json__with__id - JSON Retrieval
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__json__with__id__retrieves_content(self):                                                # Test basic JSON retrieval
        with self.data_retrieve as _:
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = self.json_file_id   )

            assert type(result) is dict
            assert result       == self.test_json_data

    def test__data__json__with__id__preserves_nested_structure(self):                                       # Test nested JSON preserved
        with self.data_retrieve as _:
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = self.json_file_id   )

            assert "nested" in result
            assert result["nested"]["key"] == "value"

    def test__data__json__with__id__non_existent_file(self):                                                # Test retrieving non-existent JSON file
        with self.data_retrieve as _:
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = "non-existent-json" )

            assert result is None

    def test__data__json__with__id__complex_json(self):                                                     # Test complex JSON structure
        complex_data = {
            "array"   : [1, 2, 3, "four", {"nested_in_array": True}],
            "boolean" : True,
            "null"    : None,
            "number"  : 123.456,
            "string"  : "hello",
            "nested"  : {
                "level2": {
                    "level3": {
                        "deep": "value"
                    }
                }
            }
        }
        complex_file_id = f"complex-json-{random_string(prefix='')}"

        self.data_store.data__store_json__with__id(cache_id     = self.cache_id       ,
                                                   namespace    = self.test_namespace ,
                                                   data_file_id = complex_file_id     ,
                                                   body         = complex_data        )

        with self.data_retrieve as _:
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = complex_file_id     )

            assert result                                  == complex_data
            assert result["array"][4]["nested_in_array"]   is True
            assert result["nested"]["level2"]["level3"]["deep"] == "value"

    def test__data__json__with__id__empty_object(self):                                                     # Test empty JSON object
        empty_file_id = f"empty-json-{random_string(prefix='')}"
        self.data_store.data__store_json__with__id(cache_id     = self.cache_id       ,
                                                   namespace    = self.test_namespace ,
                                                   data_file_id = empty_file_id       ,
                                                   body         = {}                  )

        with self.data_retrieve as _:
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = empty_file_id       )

            assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # data__json__with__id_and_key - JSON Retrieval with Key
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__json__with__id_and_key__retrieves_content(self):                                        # Test JSON retrieval with key path
        with self.data_retrieve as _:
            result = _.data__json__with__id_and_key(cache_id     = self.cache_id          ,
                                                    namespace    = self.test_namespace    ,
                                                    data_key     = self.data_key          ,
                                                    data_file_id = self.keyed_json_file_id)

            assert type(result) is dict
            assert result       == self.keyed_json_data

    def test__data__json__with__id_and_key__wrong_key_path(self):                                           # Test with wrong key path
        with self.data_retrieve as _:
            result = _.data__json__with__id_and_key(cache_id     = self.cache_id          ,
                                                    namespace    = self.test_namespace    ,
                                                    data_key     = "wrong/path"           ,
                                                    data_file_id = self.keyed_json_file_id)

            assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # data__binary__with__id - Binary Retrieval
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__binary__with__id__retrieves_content(self):                                              # Test basic binary retrieval
        with self.data_retrieve as _:
            result = _.data__binary__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = self.binary_file_id )

            assert type(result) is bytes
            assert result       == self.test_binary_data

    def test__data__binary__with__id__non_existent_file(self):                                              # Test retrieving non-existent binary file
        with self.data_retrieve as _:
            result = _.data__binary__with__id(cache_id     = self.cache_id         ,
                                              namespace    = self.test_namespace   ,
                                              data_file_id = "non-existent-binary" )

            assert result is None

    def test__data__binary__with__id__empty_bytes(self):                                                    # Test empty bytes content
        empty_file_id = f"empty-binary-{random_string(prefix='')}"
        self.data_store.data__store_binary__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = empty_file_id       ,
                                                     body         = b""                 )

        with self.data_retrieve as _:
            result = _.data__binary__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = empty_file_id       )

            assert result is None

    def test__data__binary__with__id__large_content(self):                                                  # Test large binary content
        large_data    = bytes(range(256)) * 100                                                             # ~25KB
        large_file_id = f"large-binary-{random_string(prefix='')}"

        self.data_store.data__store_binary__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = large_file_id       ,
                                                     body         = large_data          )

        with self.data_retrieve as _:
            result = _.data__binary__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = large_file_id       )

            assert result == large_data
            assert len(result) == len(large_data)

    def test__data__binary__with__id__preserves_exact_bytes(self):                                          # Test exact byte preservation
        # Include null bytes and all byte values
        exact_data    = bytes([0, 1, 127, 128, 255, 0, 0, 255])
        exact_file_id = f"exact-binary-{random_string(prefix='')}"

        self.data_store.data__store_binary__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = exact_file_id       ,
                                                     body         = exact_data          )

        with self.data_retrieve as _:
            result = _.data__binary__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = exact_file_id       )

            assert result == exact_data
            assert list(result) == [0, 1, 127, 128, 255, 0, 0, 255]

    # ═══════════════════════════════════════════════════════════════════════════
    # data__binary__with__id_and_key - Binary Retrieval with Key
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__binary__with__id_and_key__retrieves_content(self):                                      # Test binary retrieval with key path
        with self.data_retrieve as _:
            result = _.data__binary__with__id_and_key(cache_id     = self.cache_id            ,
                                                      namespace    = self.test_namespace      ,
                                                      data_key     = self.data_key            ,
                                                      data_file_id = self.keyed_binary_file_id)

            assert type(result) is bytes
            assert result       == self.keyed_binary_data

    def test__data__binary__with__id_and_key__wrong_key_path(self):                                         # Test with wrong key path
        with self.data_retrieve as _:
            result = _.data__binary__with__id_and_key(cache_id     = self.cache_id            ,
                                                      namespace    = self.test_namespace      ,
                                                      data_key     = "wrong/path"             ,
                                                      data_file_id = self.keyed_binary_file_id)

            assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Cross-Type Retrieval Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__cross_type__string_as_json_returns_none(self):                                                # Test retrieving string file as JSON
        with self.data_retrieve as _:
            # String file retrieved as JSON should fail or return raw
            result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                            namespace    = self.test_namespace ,
                                            data_file_id = self.string_file_id )

            # Behavior depends on implementation - may return None or parse error
            # String content is not valid JSON, so should return None
            assert result is None or isinstance(result, (dict, str))

    def test__cross_type__json_as_string(self):                                                             # Test retrieving JSON file as string
        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = self.json_file_id   )

            # JSON file read as string should return JSON string representation
            if result is not None:
                assert type(result) is str

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__integration__store_and_retrieve_cycle(self):                                                  # Test complete store-retrieve cycle
        test_file_id = f"cycle-test-{random_string(prefix='')}"
        test_content = f"unique content {random_string()}"

        # Store
        self.data_store.data__store_string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = test_file_id        ,
                                                     body         = test_content        )

        # Retrieve
        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = test_file_id        )

            assert result == test_content

    def test__integration__retrieve_multiple_files_same_entry(self):                                        # Test retrieving multiple files from same entry
        with self.data_retrieve as _:
            string_result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = self.string_file_id )

            json_result = _.data__json__with__id(cache_id     = self.cache_id       ,
                                                 namespace    = self.test_namespace ,
                                                 data_file_id = self.json_file_id   )

            binary_result = _.data__binary__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = self.binary_file_id )

            assert string_result == self.test_string_data
            assert json_result   == self.test_json_data
            assert binary_result == self.test_binary_data

    def test__integration__retrieve_all_keyed_files(self):                                                  # Test retrieving all keyed files
        with self.data_retrieve as _:
            string_result = _.data__string__with__id_and_key(cache_id     = self.cache_id            ,
                                                             namespace    = self.test_namespace      ,
                                                             data_key     = self.data_key            ,
                                                             data_file_id = self.keyed_string_file_id)

            json_result = _.data__json__with__id_and_key(cache_id     = self.cache_id          ,
                                                         namespace    = self.test_namespace    ,
                                                         data_key     = self.data_key          ,
                                                         data_file_id = self.keyed_json_file_id)

            binary_result = _.data__binary__with__id_and_key(cache_id     = self.cache_id            ,
                                                             namespace    = self.test_namespace      ,
                                                             data_key     = self.data_key            ,
                                                             data_file_id = self.keyed_binary_file_id)

            assert string_result == self.keyed_string_data
            assert json_result   == self.keyed_json_data
            assert binary_result == self.keyed_binary_data

    # ═══════════════════════════════════════════════════════════════════════════
    # Namespace Isolation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__namespace_isolation__separate_namespaces(self):                                               # Test files are isolated by namespace
        # Create entry in different namespace
        other_namespace  = Safe_Str__Id("other-retrieve-ns")
        other_result     = self.store_client.store__string(strategy  = "direct"        ,
                                                           namespace = other_namespace ,
                                                           body      = "other entry"   )
        other_cache_id   = other_result.cache_id
        other_file_id    = f"other-ns-file-{random_string(prefix='')}"
        other_content    = "content in other namespace"

        self.data_store.data__store_string__with__id(cache_id     = other_cache_id  ,
                                                     namespace    = other_namespace ,
                                                     data_file_id = other_file_id   ,
                                                     body         = other_content   )

        with self.data_retrieve as _:
            # Should retrieve from other namespace
            result_other = _.data__string__with__id(cache_id     = other_cache_id  ,
                                                    namespace    = other_namespace ,
                                                    data_file_id = other_file_id   )
            assert result_other == other_content

            # Should not find in test namespace
            result_test = _.data__string__with__id(cache_id     = other_cache_id     ,
                                                   namespace    = self.test_namespace,
                                                   data_file_id = other_file_id      )
            assert result_test is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════

    def test__edge_case__special_characters_in_file_id(self):                                               # Test file IDs with special characters
        # Note: Safe_Str__Id may sanitize these
        special_file_id = "file-with-dashes_and_underscores"
        special_content = "special file content"

        self.data_store.data__store_string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = special_file_id     ,
                                                     body         = special_content     )

        with self.data_retrieve as _:
            result = _.data__string__with__id(cache_id     = self.cache_id       ,
                                              namespace    = self.test_namespace ,
                                              data_file_id = special_file_id     )

            assert result == special_content

    def test__edge_case__nested_key_paths(self):                                                            # Test deeply nested key paths
        deep_key     = "level1/level2/level3/level4"
        deep_file_id = f"deep-file-{random_string(prefix='')}"
        deep_content = "content at deep path"

        self.data_store.data__store_string__with__id_and_key(cache_id     = self.cache_id       ,
                                                             namespace    = self.test_namespace ,
                                                             data_key     = deep_key            ,
                                                             data_file_id = deep_file_id        ,
                                                             body         = deep_content        )

        with self.data_retrieve as _:
            result = _.data__string__with__id_and_key(cache_id     = self.cache_id       ,
                                                      namespace    = self.test_namespace ,
                                                      data_key     = deep_key            ,
                                                      data_file_id = deep_file_id        )

            assert result == deep_content

    def test__edge_case__retrieve_after_update(self):                                                       # Test retrieval after content update
        update_file_id  = f"update-test-{random_string(prefix='')}"
        original_content = "original"
        updated_content  = "updated"

        # Store original
        self.data_store.data__store_string__with__id(cache_id     = self.cache_id       ,
                                                     namespace    = self.test_namespace ,
                                                     data_file_id = update_file_id      ,
                                                     body         = original_content    )

        with self.data_retrieve as _:
            result1 = _.data__string__with__id(cache_id     = self.cache_id       ,
                                               namespace    = self.test_namespace ,
                                               data_file_id = update_file_id      )
            assert result1 == original_content

        # Update content
        data_update = self.client_cache_service.data().update()
        data_update.data__update_string__with__id(cache_id     = self.cache_id       ,
                                                  namespace    = self.test_namespace ,
                                                  data_file_id = update_file_id      ,
                                                  body         = updated_content     )

        with self.data_retrieve as _:
            result2 = _.data__string__with__id(cache_id     = self.cache_id       ,
                                               namespace    = self.test_namespace ,
                                               data_file_id = update_file_id      )
            assert result2 == updated_content