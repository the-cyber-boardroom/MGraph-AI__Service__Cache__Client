# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Service__Fast_API__Client__Data__List
# Verify data file listing operations under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                               import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client__Requests                    import Cache__Service__Client__Requests
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                             import register_cache_service__in_memory
from mgraph_ai_service_cache_client.client.client_contract.data.Cache__Service__Client__Data__List          import Cache__Service__Client__Data__List
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from osbot_utils.utils.Objects                                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__List__Response                  import Schema__Cache__Data__List__Response
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__File__Info                      import Schema__Cache__Data__File__Info
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                              import Enum__Cache__Data_Type


class test_Service__Fast_API__Client__Data__List(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                            # Setup in-memory client
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.data_list                               = cls.cache_service_client.data().list()
        cls.data_store                              = cls.cache_service_client.data_store()
        cls.store_client                            = cls.cache_service_client.store()
        cls.test_namespace                          = Safe_Str__Id("test-data-list")

        # Create cache entry with multiple data files
        cls.store_result = cls.store_client.store__string(strategy  = "direct"           ,
                                                          namespace = cls.test_namespace ,
                                                          body      = "main entry"       )
        cls.cache_id     = cls.store_result.cache_id

        # Store various data files at root level
        cls.string_file_id = "root-string-file"
        cls.json_file_id   = "root-json-file"
        cls.binary_file_id = "root-binary-file"

        cls.data_store.data__store_string__with__id(cache_id     = cls.cache_id       ,
                                                    namespace    = cls.test_namespace ,
                                                    data_file_id = cls.string_file_id ,
                                                    body         = "string content"   )

        cls.data_store.data__store_json__with__id(cache_id     = cls.cache_id         ,
                                                  namespace    = cls.test_namespace   ,
                                                  data_file_id = cls.json_file_id     ,
                                                  body         = {"key": "value"}     )

        cls.data_store.data__store_binary__with__id(cache_id     = cls.cache_id       ,
                                                    namespace    = cls.test_namespace ,
                                                    data_file_id = cls.binary_file_id ,
                                                    body         = bytes(range(20))   )

        # Store data files in nested key paths
        cls.nested_key_1 = "level1"
        cls.nested_key_2 = "level1/level2"

        cls.data_store.data__store_string__with__id_and_key(cache_id     = cls.cache_id       ,
                                                            namespace    = cls.test_namespace ,
                                                            data_key     = cls.nested_key_1   ,
                                                            data_file_id = "nested-file-1"    ,
                                                            body         = "nested content 1" )

        cls.data_store.data__store_string__with__id_and_key(cache_id     = cls.cache_id       ,
                                                            namespace    = cls.test_namespace ,
                                                            data_key     = cls.nested_key_2   ,
                                                            data_file_id = "nested-file-2"    ,
                                                            body         = "nested content 2" )

        # Create empty cache entry for testing empty results
        cls.empty_store_result = cls.store_client.store__string(strategy  = "direct"                   ,
                                                                namespace = cls.test_namespace         ,
                                                                body      = "entry with no data files" )
        cls.empty_cache_id     = cls.empty_store_result.cache_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__setUpClass(self):                                                                             # Verify test setup
        with self.data_list as _:
            assert type(_) is Cache__Service__Client__Data__List
            assert base_classes(_) == [Type_Safe, object]

    def test__init__(self):                                                                                 # Test initialization
        with self.data_list as _:
            assert type(_.requests) is Cache__Service__Client__Requests


    def test_requests(self):                                                                                # Test requests property
        with self.data_list as _:
            requests = _.requests
            assert requests is not None
            assert callable(requests.execute)

    # ═══════════════════════════════════════════════════════════════════════════
    # data__list - Basic Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__list__all_files_recursive(self):                                                        # Test listing all files recursively
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            assert type(result)       is Schema__Cache__Data__List__Response
            assert result.cache_id    == self.cache_id
            assert result.namespace   == self.test_namespace
            assert result.file_count  >= 5                                                                  # At least 5 files created
            assert len(result.files)  == result.file_count
            assert result.total_size  >  0

    def test__data__list__response_contains_file_info(self):                                                # Test file info structure in response
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            assert len(result.files) > 0

            # Check first file has proper structure
            file_info = result.files[0]
            assert type(file_info) is Schema__Cache__Data__File__Info
            assert hasattr(file_info, 'data_file_id')
            assert hasattr(file_info, 'data_key')
            assert hasattr(file_info, 'data_type')
            assert hasattr(file_info, 'file_path')
            assert hasattr(file_info, 'file_size')
            assert hasattr(file_info, 'extension')

    def test__data__list__non_recursive(self):                                                              # Test non-recursive listing
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = False              )

            assert type(result) is Schema__Cache__Data__List__Response

            # Non-recursive should only include root-level files
            for file_info in result.files:
                # data_key should be empty for root level files
                assert '/' not in file_info.data_key or file_info.data_key == ''

    def test__data__list__empty_cache_entry(self):                                                          # Test listing empty cache entry
        with self.data_list as _:
            result = _.data__list(cache_id  = self.empty_cache_id,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            assert type(result)      is Schema__Cache__Data__List__Response
            assert result.file_count == 0
            assert result.files      == []
            assert result.total_size == 0

    def test__data__list__non_existent_cache_entry(self):                                                   # Test listing non-existent cache entry
        with self.data_list as _:
            non_existent_id = Cache_Id()
            result = _.data__list(cache_id  = non_existent_id    ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            assert result is None                                                                           # Returns None for non-existent

    # ═══════════════════════════════════════════════════════════════════════════
    # data__list__with__key - Filtered by Key Path
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__list__with__key__existing_path(self):                                                   # Test listing with key filter
        with self.data_list as _:
            result = _.data__list__with__key(cache_id  = self.cache_id      ,
                                             namespace = self.test_namespace,
                                             data_key  = self.nested_key_1  ,
                                             recursive = True               )

            assert type(result)      is Schema__Cache__Data__List__Response
            assert result.data_key   == self.nested_key_1
            assert result.file_count >= 1                                                                   # At least files in level1 path

    def test__data__list__with__key__nested_path(self):                                                     # Test listing deeper nested path
        with self.data_list as _:
            result = _.data__list__with__key(cache_id  = self.cache_id      ,
                                             namespace = self.test_namespace,
                                             data_key  = self.nested_key_2  ,
                                             recursive = True               )

            assert type(result)      is Schema__Cache__Data__List__Response
            assert result.file_count >= 1                                                                   # File at level1/level2

    def test__data__list__with__key__non_existent_path(self):                                               # Test listing non-existent key path
        with self.data_list as _:
            result = _.data__list__with__key(cache_id  = self.cache_id      ,
                                             namespace = self.test_namespace,
                                             data_key  = "nonexistent/path" ,
                                             recursive = True               )

            assert type(result)      is Schema__Cache__Data__List__Response
            assert result.file_count == 0
            assert result.files      == []

    def test__data__list__with__key__non_recursive(self):                                                   # Test non-recursive with key
        with self.data_list as _:
            result = _.data__list__with__key(cache_id  = self.cache_id      ,
                                             namespace = self.test_namespace,
                                             data_key  = self.nested_key_1  ,
                                             recursive = False              )

            assert type(result) is Schema__Cache__Data__List__Response
            # Should only return files directly in level1, not level1/level2

    # ═══════════════════════════════════════════════════════════════════════════
    # Response Structure Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__response_structure__all_fields_present(self):                                                 # Verify response has all fields
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            assert hasattr(result, 'cache_id')
            assert hasattr(result, 'namespace')
            assert hasattr(result, 'data_key')
            assert hasattr(result, 'file_count')
            assert hasattr(result, 'files')
            assert hasattr(result, 'total_size')

    def test__response_structure__file_info_data_types(self):                                               # Verify file info contains different data types
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            data_types_found = set()
            for file_info in result.files:
                data_types_found.add(file_info.data_type)

            # Should have string, json, and binary files
            assert Enum__Cache__Data_Type.STRING in data_types_found
            assert Enum__Cache__Data_Type.JSON   in data_types_found
            assert Enum__Cache__Data_Type.BINARY in data_types_found

    def test__response_structure__file_extensions_match_types(self):                                        # Verify extensions match data types
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            for file_info in result.files:
                if file_info.data_type == Enum__Cache__Data_Type.STRING:
                    assert file_info.extension == 'txt'
                elif file_info.data_type == Enum__Cache__Data_Type.JSON:
                    assert file_info.extension == 'json'
                elif file_info.data_type == Enum__Cache__Data_Type.BINARY:
                    assert file_info.extension == 'bin'

    # ═══════════════════════════════════════════════════════════════════════════
    # Namespace Isolation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__list__wrong_namespace(self):                                                            # Test namespace isolation
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id       ,
                                  namespace = "different-ns"      ,
                                  recursive = True                )

            assert result is None                                                                           # Cache entry not found in different namespace

    # ═══════════════════════════════════════════════════════════════════════════
    # Total Size Calculation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__total_size__matches_individual_files(self):                                                   # Test total size calculation
        with self.data_list as _:
            result = _.data__list(cache_id  = self.cache_id      ,
                                  namespace = self.test_namespace,
                                  recursive = True               )

            calculated_total = sum(f.file_size for f in result.files)
            assert result.total_size == calculated_total