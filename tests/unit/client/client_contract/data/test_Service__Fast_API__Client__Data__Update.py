# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Service__Fast_API__Client__Data__Update
# Verify data file update operations under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                               import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client__Requests                    import Cache__Service__Client__Requests
from mgraph_ai_service_cache_client.client.client_contract.data.Cache__Service__Client__Data__Update        import Cache__Service__Client__Data__Update
from osbot_utils.utils.Objects                                                                              import base_classes
from osbot_utils.utils.Misc                                                                                 import random_string
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                             import register_cache_service__in_memory
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                          import Cache_Id
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Update__Response                import Schema__Cache__Data__Update__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                              import Enum__Cache__Data_Type



class test_Service__Fast_API__Client__Data__Update(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                            # Setup in-memory client
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.data_update           = cls.cache_service_client.data().update()
        cls.data_store            = cls.cache_service_client.data_store()
        cls.data_retrieve         = cls.cache_service_client.data().retrieve()
        cls.store_client          = cls.cache_service_client.store()
        cls.test_namespace        = "test-data-update"

        # Test data versions
        cls.string_v1      = "original string content"
        cls.string_v2      = "updated string content"
        cls.json_v1        = {"version": 1, "status": "original", "data": "initial"}
        cls.json_v2        = {"version": 2, "status": "updated" , "data": "modified"}
        cls.binary_v1      = bytes(range(0, 50))
        cls.binary_v2      = bytes(range(50, 100))

    def _create_entry_with_data_file(self, data_type: str, data_file_id: str, data_key: str = None):       # Helper to create cache entry with data file
        # Create main cache entry
        store_result = self.store_client.store__string(strategy  = "direct"           ,
                                                       namespace = self.test_namespace,
                                                       body      = f"main entry for {data_file_id}")
        cache_id     = store_result.cache_id

        # Store initial data file
        if data_type == "string":
            if data_key:
                self.data_store.data__store_string__with__id_and_key(cache_id     = cache_id           ,
                                                                     namespace    = self.test_namespace,
                                                                     data_key     = data_key           ,
                                                                     data_file_id = data_file_id       ,
                                                                     body         = self.string_v1     )
            else:
                self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_file_id = data_file_id       ,
                                                             body         = self.string_v1     )
        elif data_type == "json":
            if data_key:
                self.data_store.data__store_json__with__id_and_key(cache_id     = cache_id           ,
                                                                   namespace    = self.test_namespace,
                                                                   data_key     = data_key           ,
                                                                   data_file_id = data_file_id       ,
                                                                   body         = self.json_v1       )
            else:
                self.data_store.data__store_json__with__id(cache_id     = cache_id           ,
                                                           namespace    = self.test_namespace,
                                                           data_file_id = data_file_id       ,
                                                           body         = self.json_v1       )
        elif data_type == "binary":
            if data_key:
                self.data_store.data__store_binary__with__id_and_key(cache_id     = cache_id           ,
                                                                     namespace    = self.test_namespace,
                                                                     data_key     = data_key           ,
                                                                     data_file_id = data_file_id       ,
                                                                     body         = self.binary_v1     )
            else:
                self.data_store.data__store_binary__with__id(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_file_id = data_file_id       ,
                                                             body         = self.binary_v1     )

        return cache_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__setUpClass(self):                                                                             # Verify test setup
        with self.data_update as _:
            assert type(_) is Cache__Service__Client__Data__Update
            assert base_classes(_) == [Type_Safe, object]

    def test__init__(self):                                                                                 # Test initialization
        with self.data_update as _:
            assert type(_.requests) is Cache__Service__Client__Requests

    def test_requests(self):                                                                                # Test requests property
        with self.data_update as _:
            requests = _.requests
            assert requests is not None
            assert callable(requests.execute)

    # ═══════════════════════════════════════════════════════════════════════════
    # String Update Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__update_string__with__id(self):                                                          # Test string update by ID
        data_file_id = f"string-update-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("string", data_file_id)

        with self.data_update as _:
            result = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = data_file_id       ,
                                                     body         = self.string_v2     )

            assert type(result)        is Schema__Cache__Data__Update__Response
            assert result.success      is True
            assert result.cache_id     == cache_id
            assert result.namespace    == self.test_namespace
            assert result.data_type    == Enum__Cache__Data_Type.STRING
            assert result.data_file_id == data_file_id
            assert result.file_size    >  0

        # Verify content actually updated
        retrieved = self.data_retrieve.data__string__with__id(cache_id     = cache_id           ,
                                                              namespace    = self.test_namespace,
                                                              data_file_id = data_file_id       )
        assert retrieved == self.string_v2

    def test__data__update_string__with__id_and_key(self):                                                  # Test string update with key path
        data_file_id = f"string-key-update-{random_string(prefix='')}"
        data_key     = "configs/app"
        cache_id     = self._create_entry_with_data_file("string", data_file_id, data_key)

        with self.data_update as _:
            result = _.data__update_string__with__id_and_key(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_key     = data_key           ,
                                                             data_file_id = data_file_id       ,
                                                             body         = self.string_v2     )

            assert type(result)     is Schema__Cache__Data__Update__Response
            assert result.success   is True
            assert result.data_key  == data_key

        # Verify content updated
        retrieved = self.data_retrieve.data__string__with__id_and_key(cache_id     = cache_id           ,
                                                                      namespace    = self.test_namespace,
                                                                      data_key     = data_key           ,
                                                                      data_file_id = data_file_id       )
        assert retrieved == self.string_v2

    # ═══════════════════════════════════════════════════════════════════════════
    # JSON Update Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__update_json__with__id(self):                                                            # Test JSON update by ID
        data_file_id = f"json-update-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("json", data_file_id)

        with self.data_update as _:
            result = _.data__update_json__with__id(cache_id     = cache_id           ,
                                                   namespace    = self.test_namespace,
                                                   data_file_id = data_file_id       ,
                                                   body         = self.json_v2       )

            assert type(result)     is Schema__Cache__Data__Update__Response
            assert result.success   is True
            assert result.data_type == Enum__Cache__Data_Type.JSON

        # Verify content updated
        retrieved = self.data_retrieve.data__json__with__id(cache_id     = cache_id           ,
                                                            namespace    = self.test_namespace,
                                                            data_file_id = data_file_id       )
        assert retrieved == self.json_v2

    def test__data__update_json__with__id_and_key(self):                                                    # Test JSON update with key path
        data_file_id = f"json-key-update-{random_string(prefix='')}"
        data_key     = "data/metrics"
        cache_id     = self._create_entry_with_data_file("json", data_file_id, data_key)

        with self.data_update as _:
            result = _.data__update_json__with__id_and_key(cache_id     = cache_id           ,
                                                           namespace    = self.test_namespace,
                                                           data_key     = data_key           ,
                                                           data_file_id = data_file_id       ,
                                                           body         = self.json_v2       )

            assert type(result)    is Schema__Cache__Data__Update__Response
            assert result.success  is True
            assert result.data_key == data_key

        # Verify content updated
        retrieved = self.data_retrieve.data__json__with__id_and_key(cache_id     = cache_id           ,
                                                                    namespace    = self.test_namespace,
                                                                    data_key     = data_key           ,
                                                                    data_file_id = data_file_id       )
        assert retrieved == self.json_v2

    # ═══════════════════════════════════════════════════════════════════════════
    # Binary Update Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__update_binary__with__id(self):                                                          # Test binary update by ID
        data_file_id = f"binary-update-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("binary", data_file_id)

        with self.data_update as _:
            result = _.data__update_binary__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = data_file_id       ,
                                                     body         = self.binary_v2     )

            assert type(result)     is Schema__Cache__Data__Update__Response
            assert result.success   is True
            assert result.data_type == Enum__Cache__Data_Type.BINARY

        # Verify content updated
        retrieved = self.data_retrieve.data__binary__with__id(cache_id     = cache_id           ,
                                                              namespace    = self.test_namespace,
                                                              data_file_id = data_file_id       )
        assert retrieved == self.binary_v2

    def test__data__update_binary__with__id_and_key(self):                                                  # Test binary update with key path
        data_file_id = f"binary-key-update-{random_string(prefix='')}"
        data_key     = "assets/images"
        cache_id     = self._create_entry_with_data_file("binary", data_file_id, data_key)

        with self.data_update as _:
            result = _.data__update_binary__with__id_and_key(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_key     = data_key           ,
                                                             data_file_id = data_file_id       ,
                                                             body         = self.binary_v2     )

            assert type(result)    is Schema__Cache__Data__Update__Response
            assert result.success  is True
            assert result.data_key == data_key

        # Verify content updated
        retrieved = self.data_retrieve.data__binary__with__id_and_key(cache_id     = cache_id           ,
                                                                      namespace    = self.test_namespace,
                                                                      data_key     = data_key           ,
                                                                      data_file_id = data_file_id       )
        assert retrieved == self.binary_v2

    # ═══════════════════════════════════════════════════════════════════════════
    # Error Cases
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__update_string__non_existent_file(self):                                                 # Test updating non-existent file
        # Create cache entry but no data file
        store_result = self.store_client.store__string(strategy  = "direct"           ,
                                                       namespace = self.test_namespace,
                                                       body      = "entry only"       )
        cache_id = store_result.cache_id

        with self.data_update as _:
            result = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = "non-existent-file",
                                                     body         = "new content"      )

            assert result is None                                                                           # Returns None for non-existent

    def test__data__update_string__non_existent_cache_entry(self):                                          # Test updating with non-existent cache entry
        non_existent_id = Cache_Id()

        with self.data_update as _:
            result = _.data__update_string__with__id(cache_id     = non_existent_id    ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = "some-file"        ,
                                                     body         = "content"          )

            assert result is None                                                                           # Returns None for non-existent cache

    def test__data__update_string__wrong_namespace(self):                                                   # Test namespace isolation
        data_file_id = f"ns-test-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("string", data_file_id)

        with self.data_update as _:
            result = _.data__update_string__with__id(cache_id     = cache_id        ,
                                                     namespace    = "different-ns"  ,
                                                     data_file_id = data_file_id    ,
                                                     body         = "new content"   )

            assert result is None                                                                           # Cache entry not in this namespace

    # ═══════════════════════════════════════════════════════════════════════════
    # Multiple Updates Test
    # ═══════════════════════════════════════════════════════════════════════════

    def test__data__update__multiple_sequential_updates(self):                                              # Test multiple updates on same file
        data_file_id = f"multi-update-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("string", data_file_id)

        with self.data_update as _:
            # First update
            result_1 = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                       namespace    = self.test_namespace,
                                                       data_file_id = data_file_id       ,
                                                       body         = "version 2"        )
            assert result_1.success is True

            # Second update
            result_2 = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                       namespace    = self.test_namespace,
                                                       data_file_id = data_file_id       ,
                                                       body         = "version 3"        )
            assert result_2.success is True

            # Third update
            result_3 = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                       namespace    = self.test_namespace,
                                                       data_file_id = data_file_id       ,
                                                       body         = "version 4"        )
            assert result_3.success is True

        # Verify final content
        retrieved = self.data_retrieve.data__string__with__id(cache_id     = cache_id           ,
                                                              namespace    = self.test_namespace,
                                                              data_file_id = data_file_id       )
        assert retrieved == "version 4"

    # ═══════════════════════════════════════════════════════════════════════════
    # Response Structure Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__response_structure__all_fields_present(self):                                                 # Verify response has all fields
        data_file_id = f"struct-test-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("string", data_file_id)

        with self.data_update as _:
            result = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = data_file_id       ,
                                                     body         = self.string_v2     )

            assert hasattr(result, 'success')
            assert hasattr(result, 'cache_id')
            assert hasattr(result, 'namespace')
            assert hasattr(result, 'data_type')
            assert hasattr(result, 'data_key')
            assert hasattr(result, 'data_file_id')
            assert hasattr(result, 'file_path')
            assert hasattr(result, 'file_size')

    def test__response_structure__file_size_reflects_content(self):                                         # Verify file size updates with content
        data_file_id = f"size-test-{random_string(prefix='')}"
        cache_id     = self._create_entry_with_data_file("string", data_file_id)

        short_content = "short"
        long_content  = "this is a much longer string content for testing file size"

        with self.data_update as _:
            # Update with short content
            result_short = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                           namespace    = self.test_namespace,
                                                           data_file_id = data_file_id       ,
                                                           body         = short_content      )

            # Update with long content
            result_long = _.data__update_string__with__id(cache_id     = cache_id           ,
                                                          namespace    = self.test_namespace,
                                                          data_file_id = data_file_id       ,
                                                          body         = long_content       )

            assert result_long.file_size > result_short.file_size