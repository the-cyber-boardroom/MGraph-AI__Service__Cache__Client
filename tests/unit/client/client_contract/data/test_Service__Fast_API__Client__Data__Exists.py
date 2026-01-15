# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Service__Fast_API__Client__Data__Exists
# Verify data file existence checking operations
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from osbot_utils.utils.Objects                                                                              import base_classes
from mgraph_ai_service_cache_client.client.client_contract.data.Service__Fast_API__Client__Data__Exists     import Service__Fast_API__Client__Data__Exists
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Exists__Response                import Schema__Cache__Data__Exists__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                              import Enum__Cache__Data_Type
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                           import client_cache_service


class test_Service__Fast_API__Client__Data__Exists(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                            # Setup in-memory client
        cls.client_cache_service, cls.cache_service = client_cache_service()
        cls.data_exists                             = cls.client_cache_service.data().exists()
        cls.data_store                              = cls.client_cache_service.data_store()
        cls.store_client                            = cls.client_cache_service.store()
        cls.test_namespace                          = Safe_Str__Id("test-data-exists")

        # Create a cache entry with data files for testing
        cls.test_string_data                        = "test string content"
        cls.test_json_data                          = {"key": "value", "number": 42}
        cls.test_binary_data                        = bytes(range(50))

        # Create main cache entry
        cls.store_result = cls.store_client.store__string(strategy  = "direct"           ,
                                                          namespace = cls.test_namespace ,
                                                          body      = "main entry"       )
        cls.cache_id     = cls.store_result.cache_id

        # Store data files under the cache entry
        cls.string_file_id = "test-string-file"
        cls.json_file_id   = "test-json-file"
        cls.binary_file_id = "test-binary-file"
        cls.data_key       = "subfolder/nested"

        cls.data_store.data__store_string__with__id(cache_id     = cls.cache_id       ,
                                                    namespace    = cls.test_namespace ,
                                                    data_file_id = cls.string_file_id ,
                                                    body         = cls.test_string_data)

        cls.data_store.data__store_json__with__id(cache_id     = cls.cache_id     ,
                                                  namespace    = cls.test_namespace,
                                                  data_file_id = cls.json_file_id ,
                                                  body         = cls.test_json_data)

        cls.data_store.data__store_binary__with__id(cache_id     = cls.cache_id       ,
                                                    namespace    = cls.test_namespace ,
                                                    data_file_id = cls.binary_file_id ,
                                                    body         = cls.test_binary_data)

        # Store data file with key path
        cls.keyed_file_id = "keyed-data-file"
        cls.data_store.data__store_string__with__id_and_key(cache_id     = cls.cache_id       ,
                                                            namespace    = cls.test_namespace ,
                                                            data_key     = cls.data_key       ,
                                                            data_file_id = cls.keyed_file_id  ,
                                                            body         = "keyed content"    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__setUpClass(self):                                                                             # Verify test setup
        with self.data_exists as _:
            assert type(_)         is Service__Fast_API__Client__Data__Exists
            assert base_classes(_) == [Type_Safe, object]

    def test__init__(self):                                                                                 # Test initialization
        with self.data_exists as _:
            assert _._client is self.client_cache_service
            assert _.obj()   == __(_client = __SKIP__)

    def test_requests(self):                                                                                # Test requests property
        with self.data_exists as _:
            requests = _.requests
            assert requests is not None
            assert callable(requests.execute)

    # ═══════════════════════════════════════════════════════════════════════════
    # data__exists__with__id - Existing Files
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__exists__with__id__string_file_exists(self):                                             # Test existing string file
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = self.test_namespace        ,
                                              data_type    = Enum__Cache__Data_Type.STRING,
                                              data_file_id = self.string_file_id        )

            assert type(result)      is Schema__Cache__Data__Exists__Response
            assert result.exists     is True
            assert result.cache_id   == self.cache_id
            assert result.namespace  == self.test_namespace
            assert result.data_type  == Enum__Cache__Data_Type.STRING
            assert result.data_file_id == self.string_file_id

    def test__data__exists__with__id__json_file_exists(self):                                               # Test existing JSON file
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id            ,
                                              namespace    = self.test_namespace      ,
                                              data_type    = Enum__Cache__Data_Type.JSON,
                                              data_file_id = self.json_file_id        )

            assert type(result)  is Schema__Cache__Data__Exists__Response
            assert result.exists is True

    def test__data__exists__with__id__binary_file_exists(self):                                             # Test existing binary file
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = self.test_namespace        ,
                                              data_type    = Enum__Cache__Data_Type.BINARY,
                                              data_file_id = self.binary_file_id        )

            assert type(result)  is Schema__Cache__Data__Exists__Response
            assert result.exists is True

    # ═══════════════════════════════════════════════════════════════════════════
    # data__exists__with__id - Non-Existing Files
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__exists__with__id__non_existent_file(self):                                              # Test non-existent file
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = self.test_namespace        ,
                                              data_type    = Enum__Cache__Data_Type.STRING,
                                              data_file_id = "non-existent-file"        )

            assert type(result)  is Schema__Cache__Data__Exists__Response
            assert result.exists is False

    def test__data__exists__with__id__wrong_data_type(self):                                                # Test wrong data type for existing file
        with self.data_exists as _:
            # String file exists, but checking with JSON type
            result = _.data__exists__with__id(cache_id     = self.cache_id            ,
                                              namespace    = self.test_namespace      ,
                                              data_type    = Enum__Cache__Data_Type.JSON,
                                              data_file_id = self.string_file_id      )

            assert result.exists is False                                                                   # Wrong type returns false

    def test__data__exists__with__id__wrong_namespace(self):                                                # Test namespace isolation
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = "different-namespace"      ,
                                              data_type    = Enum__Cache__Data_Type.STRING,
                                              data_file_id = self.string_file_id        )

            assert result.exists is False                                                                   # Different namespace

    # ═══════════════════════════════════════════════════════════════════════════
    # data__exists__with__id_and_key - With Key Path
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__exists__with__id_and_key__existing_file(self):                                          # Test file with key path exists
        with self.data_exists as _:
            result = _.data__exists__with__id_and_key(cache_id     = self.cache_id              ,
                                                      namespace    = self.test_namespace        ,
                                                      data_type    = Enum__Cache__Data_Type.STRING,
                                                      data_key     = self.data_key              ,
                                                      data_file_id = self.keyed_file_id         )

            assert type(result)  is Schema__Cache__Data__Exists__Response
            assert result.exists is True
            assert result.data_key == self.data_key
            assert result.data_file_id == self.keyed_file_id

    def test__data__exists__with__id_and_key__wrong_key_path(self):                                         # Test wrong key path
        with self.data_exists as _:
            result = _.data__exists__with__id_and_key(cache_id     = self.cache_id              ,
                                                      namespace    = self.test_namespace        ,
                                                      data_type    = Enum__Cache__Data_Type.STRING,
                                                      data_key     = "wrong/path"               ,
                                                      data_file_id = self.keyed_file_id         )

            assert result.exists is False                                                                   # Wrong key path

    def test__data__exists__with__id_and_key__file_without_key(self):                                       # Test file stored without key
        with self.data_exists as _:
            # String file was stored without key path
            result = _.data__exists__with__id_and_key(cache_id     = self.cache_id              ,
                                                      namespace    = self.test_namespace        ,
                                                      data_type    = Enum__Cache__Data_Type.STRING,
                                                      data_key     = "some/path"                ,
                                                      data_file_id = self.string_file_id        )

            assert result.exists is False                                                                   # File exists but not at this key

    # ═══════════════════════════════════════════════════════════════════════════
    # Response Structure Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__response_structure__all_fields_present(self):                                                 # Verify response has all fields
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = self.test_namespace        ,
                                              data_type    = Enum__Cache__Data_Type.STRING,
                                              data_file_id = self.string_file_id        )

            assert hasattr(result, 'exists')
            assert hasattr(result, 'cache_id')
            assert hasattr(result, 'namespace')
            assert hasattr(result, 'data_type')
            assert hasattr(result, 'data_key')
            assert hasattr(result, 'data_file_id')

    def test__response_structure__field_types(self):                                                        # Verify response field types
        with self.data_exists as _:
            result = _.data__exists__with__id(cache_id     = self.cache_id              ,
                                              namespace    = self.test_namespace        ,
                                              data_type    = Enum__Cache__Data_Type.JSON,
                                              data_file_id = self.json_file_id          )

            assert type(result.exists)       is bool
            assert type(result.data_type)    is Enum__Cache__Data_Type