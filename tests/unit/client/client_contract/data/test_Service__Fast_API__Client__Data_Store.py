from unittest                                                                   import TestCase
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service import register_cache_service__in_memory
from osbot_utils.utils.Misc                                                     import random_string, random_bytes, is_guid
from mgraph_ai_service_cache_client.client.testing.Cache_Client_Test_Helpers    import Cache_Client_Test_Helpers



class test_Service__Fast_API__Client__Data_Store__Comprehensive(TestCase):                          # Comprehensive data store operations test suite"""

    @classmethod
    def setUpClass(cls) -> None:                                                                    # Setup in-memory client - no HTTP server needed
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.data_store            = cls.cache_service_client.data_store()
        cls.data_retrieve         = cls.cache_service_client.data().retrieve()
        cls.data_delete           = cls.cache_service_client.data().delete()
        cls.helpers               = Cache_Client_Test_Helpers(cache_service_client=cls.cache_service_client)

    # ═════════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═════════════════════════════════════════════════════════════════════════════

    def test__setup__client_initialized(self):                                      # Verify test setup is correct
        assert self.cache_service_client is not None
        assert self.data_store           is not None
        assert self.data_retrieve        is not None
        assert self.data_delete          is not None
        assert self.helpers              is not None

    # ═════════════════════════════════════════════════════════════════════════════
    # String Data Storage - Basic Operations
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_store__string__auto_generated_id(self):
        """Test storing string data with auto-generated file_id"""
        # Setup: Create main cache entry
        namespace    = 'test-data-store-string-auto'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store string data file
        data_value   = random_string('test_data_')
        store_result = self.helpers.add_data_string(cache_id  = cache_id  ,
                                                    namespace = namespace ,
                                                    data      = data_value)

        # Verify: Store result structure
        assert store_result.cache_id           == cache_id
        assert store_result.namespace          == namespace
        assert store_result.data_type          == 'string'
        assert store_result.extension          == 'txt'
        assert is_guid(store_result.file_id)   is True                          # Auto-generated GUID
        assert store_result.file_size          >  0

        # Verify: Can retrieve the data back
        data_file_id = store_result.file_id
        retrieved    = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert retrieved == data_value

    def test__data_store__string__with_custom_id(self):
        """Test storing string data with custom file_id"""
        # Setup
        namespace    = 'test-data-store-string-id'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with custom ID
        data_value   = random_string('test_data_')
        data_file_id = 'my-custom-string-id'
        store_result = self.helpers.add_data_string(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_file_id = data_file_id ,
                                                    data         = data_value   )

        # Verify: Custom ID used
        assert store_result.file_id == data_file_id

        # Verify: Retrieve using custom ID
        retrieved = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                              namespace    = namespace    ,
                                                              data_file_id = data_file_id )
        assert retrieved == data_value

    def test__data_store__string__with_key_and_id(self):
        """Test storing string data with data_key path and file_id"""
        # Setup
        namespace    = 'test-data-store-string-key'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with both key path and ID
        data_value   = random_string('test_data_')
        data_key     = 'logs/application/errors'
        data_file_id = 'error-log-001'
        store_result = self.helpers.add_data_string(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_key     = data_key     ,
                                                    data_file_id = data_file_id ,
                                                    data         = data_value   )

        # Verify: Stored with key structure
        assert store_result.data_key == data_key
        assert store_result.file_id  == data_file_id

        # Verify: Retrieve using key and ID
        retrieved = self.data_retrieve.data__string__with__id_and_key(cache_id     = cache_id     ,
                                                                      namespace    = namespace    ,
                                                                      data_key     = data_key     ,
                                                                      data_file_id = data_file_id )
        assert retrieved == data_value

    # ═════════════════════════════════════════════════════════════════════════════
    # JSON Data Storage - Basic Operations
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_store__json__auto_generated_id(self):
        """Test storing JSON data with auto-generated file_id"""
        # Setup
        namespace  = 'test-data-store-json-auto'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store JSON data
        data_value = {'message': 'test', 'count': 42, 'random': random_string()}
        store_result = self.helpers.add_data_json(cache_id  = cache_id  ,
                                                  namespace = namespace ,
                                                  data      = data_value)

        # Verify: Store result
        assert store_result.data_type == 'json'
        assert store_result.extension == 'json'
        assert is_guid(store_result.file_id) is True

        # Verify: Retrieve JSON back
        data_file_id = store_result.file_id
        retrieved    = self.data_retrieve.data__json__with__id(cache_id     = cache_id     ,
                                                               namespace    = namespace    ,
                                                               data_file_id = data_file_id )
        assert type(retrieved) is dict
        assert retrieved       == data_value

    def test__data_store__json__with_custom_id(self):
        """Test storing JSON data with custom file_id"""
        # Setup
        namespace    = 'test-data-store-json-id'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with custom ID
        data_value   = {'config': 'production', 'timeout': 30}
        data_file_id = 'production-config'
        store_result = self.helpers.add_data_json(cache_id     = cache_id     ,
                                                 namespace    = namespace    ,
                                                 data_file_id = data_file_id ,
                                                 data         = data_value   )

        # Verify: Custom ID used
        assert store_result.file_id == data_file_id

        # Verify: Retrieve
        retrieved = self.data_retrieve.data__json__with__id(cache_id     = cache_id     ,
                                                           namespace    = namespace    ,
                                                           data_file_id = data_file_id )
        assert retrieved == data_value

    def test__data_store__json__with_key_and_id(self):
        """Test storing JSON data with data_key and file_id"""
        # Setup
        namespace    = 'test-data-store-json-key'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with key and ID
        data_value   = {'status': 'active', 'items': [1, 2, 3]}
        data_key     = 'configs/app/settings'
        data_file_id = 'app-settings-v2'
        store_result = self.helpers.add_data_json(cache_id     = cache_id     ,
                                                 namespace    = namespace    ,
                                                 data_key     = data_key     ,
                                                 data_file_id = data_file_id ,
                                                 data         = data_value   )

        # Verify: Structure correct
        assert store_result.data_key == data_key
        assert store_result.file_id  == data_file_id

        # Verify: Retrieve
        retrieved = self.data_retrieve.data__json__with__id_and_key(cache_id     = cache_id     ,
                                                                    namespace    = namespace    ,
                                                                    data_key     = data_key     ,
                                                                    data_file_id = data_file_id )
        assert retrieved == data_value

    # ═════════════════════════════════════════════════════════════════════════════
    # Binary Data Storage - Basic Operations
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_store__binary__auto_generated_id(self):
        """Test storing binary data with auto-generated file_id"""
        # Setup
        namespace  = 'test-data-store-binary-auto'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store binary data
        data_value   = random_bytes(length=100)
        store_result = self.helpers.add_data_binary(cache_id  = cache_id  ,
                                                    namespace = namespace ,
                                                    data      = data_value)

        # Verify: Store result
        assert store_result.data_type == 'binary'
        assert store_result.extension == 'bin'
        assert store_result.file_size == 100
        assert is_guid(store_result.file_id) is True

        # Verify: Retrieve binary back
        data_file_id = store_result.file_id
        retrieved    = self.data_retrieve.data__binary__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert type(retrieved) is bytes
        assert retrieved       == data_value

    def test__data_store__binary__with_custom_id(self):
        """Test storing binary data with custom file_id"""
        # Setup
        namespace    = 'test-data-store-binary-id'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with custom ID
        data_value   = random_bytes(length=256)
        data_file_id = 'binary-image-001'
        store_result = self.helpers.add_data_binary(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_file_id = data_file_id ,
                                                    data         = data_value   )

        # Verify: Custom ID used
        assert store_result.file_id  == data_file_id
        assert store_result.file_size == 256

        # Verify: Retrieve
        retrieved = self.data_retrieve.data__binary__with__id(cache_id     = cache_id     ,
                                                              namespace    = namespace    ,
                                                              data_file_id = data_file_id )
        assert retrieved == data_value

    def test__data_store__binary__with_key_and_id(self):
        """Test storing binary data with data_key and file_id"""
        # Setup
        namespace    = 'test-data-store-binary-key'
        main_entry   = self.helpers.create_string_entry(namespace = namespace)
        cache_id     = main_entry.cache_id

        # Action: Store with key and ID
        data_value   = random_bytes(length=512)
        data_key     = 'images/thumbnails'
        data_file_id = 'thumb-user-avatar'
        store_result = self.helpers.add_data_binary(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_key     = data_key     ,
                                                    data_file_id = data_file_id ,
                                                    data         = data_value   )

        # Verify: Structure
        assert store_result.data_key  == data_key
        assert store_result.file_id   == data_file_id
        assert store_result.file_size == 512

        # Verify: Retrieve
        retrieved = self.data_retrieve.data__binary__with__id_and_key(cache_id     = cache_id     ,
                                                                      namespace    = namespace    ,
                                                                      data_key     = data_key     ,
                                                                      data_file_id = data_file_id )
        assert retrieved == data_value

    # ═════════════════════════════════════════════════════════════════════════════
    # Multiple Data Files - Complex Scenarios
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_store__multiple_files__same_entry(self):
        """Test storing multiple data files to same cache entry"""
        # Setup
        namespace  = 'test-data-store-multiple'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store 3 string, 2 json, 1 binary files
        string_ids = []
        for i in range(3):
            result = self.helpers.add_data_string(cache_id     = cache_id         ,
                                                 namespace    = namespace        ,
                                                 data_file_id = f'string-{i}'    ,
                                                 data         = f'string_data_{i}')
            string_ids.append(result.file_id)

        json_ids = []
        for i in range(2):
            result = self.helpers.add_data_json(cache_id     = cache_id      ,
                                               namespace    = namespace     ,
                                               data_file_id = f'json-{i}'   ,
                                               data         = {'index': i}  )
            json_ids.append(result.file_id)

        binary_result = self.helpers.add_data_binary(cache_id     = cache_id     ,
                                                     namespace    = namespace    ,
                                                     data_file_id = 'binary-0'   )
        binary_id = binary_result.file_id

        # Verify: All files stored
        assert len(string_ids) == 3
        assert len(json_ids)   == 2
        assert binary_id       == 'binary-0'

        # Verify: Can retrieve each file
        for i, file_id in enumerate(string_ids):
            retrieved = self.data_retrieve.data__string__with__id(cache_id     = cache_id  ,
                                                                  namespace    = namespace ,
                                                                  data_file_id = file_id   )
            assert retrieved == f'string_data_{i}'

    def test__data_store__hierarchical_keys(self):
        """Test storing data files with hierarchical key paths"""
        # Setup
        namespace  = 'test-data-store-hierarchy'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store files with nested paths
        paths = [
            'logs/app/error',
            'logs/app/info',
            'logs/system/debug',
            'configs/database/prod',
            'configs/database/dev'
        ]

        stored_files = {}
        for path in paths:
            result = self.helpers.add_data_string(cache_id     = cache_id          ,
                                                 namespace    = namespace         ,
                                                 data_key     = path              ,
                                                 data_file_id = path.split('/')[-1],
                                                 data         = f'data_for_{path}' )
            stored_files[path] = result.file_id

        # Verify: All paths stored correctly
        assert len(stored_files) == 5

        # Verify: Can retrieve using full paths
        for path, file_id in stored_files.items():
            retrieved = self.data_retrieve.data__string__with__id_and_key(
                cache_id     = cache_id  ,
                namespace    = namespace ,
                data_key     = path      ,
                data_file_id = file_id
            )
            assert retrieved == f'data_for_{path}'

    # ═════════════════════════════════════════════════════════════════════════════
    # Data Deletion Operations
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_delete__single_file(self):
        """Test deleting a single data file"""
        # Setup: Create entry with data file
        namespace       = 'test-data-delete-single'
        cache_id, _, _  = self.helpers.create_entry_with_data_files(namespace    = namespace,
                                                                 string_count = 1       )

        # Verify: File exists before deletion
        assert self.helpers.verify_data_file_exists(cache_id     = cache_id   ,
                                                   data_file_id = 'string-data-0',
                                                   namespace    = namespace   ) is True

        # Action: Delete the data file
        # NOTE: GAP - No direct delete single data file method in client
        # Would need: client.data().delete().delete__data__file__with__id(...)
        # For now, delete all data files
        delete_result = self.data_delete.delete__all__data__files(cache_id  = cache_id  ,
                                                                  namespace = namespace )

        # Verify: Files deleted
        assert delete_result.get('deleted_count') >= 1

        # Verify: File no longer exists
        assert self.helpers.verify_data_file_exists(cache_id     = cache_id   ,
                                                   data_file_id = 'string-data-0',
                                                   namespace    = namespace   ) is False

    def test__data_delete__all_files(self):
        """Test deleting all data files from cache entry"""
        # Setup: Create entry with multiple data files
        namespace       = 'test-data-delete-all'
        cache_id, _, _  = self.helpers.create_entry_with_data_files(namespace    = namespace,
                                                                    string_count = 3       ,
                                                                    json_count   = 2       ,
                                                                    binary_count = 1       )

        # Action: Delete all data files
        delete_result = self.data_delete.delete__all__data__files(cache_id  = cache_id  ,
                                                                  namespace = namespace )

        # Verify: All files deleted
        assert delete_result.get('deleted_count') == 6                              # 3 string + 2 json + 1 binary
        assert len(delete_result.get('deleted_files')) == 6

    def test__data_delete__with_key_path(self):
        """Test deleting data files under specific key path"""
        # Setup: Create files in different key paths
        namespace   = 'test-data-delete-key'
        main_entry  = self.helpers.create_string_entry(namespace = namespace)
        cache_id    = main_entry.cache_id

        # Store files in 'logs' path
        for i in range(3):
            self.helpers.add_data_string(cache_id     = cache_id      ,
                                        namespace    = namespace     ,
                                        data_key     = 'logs'        ,
                                        data_file_id = f'log-{i}'    )

        # Store files in 'configs' path
        for i in range(2):
            self.helpers.add_data_string(cache_id     = cache_id      ,
                                        namespace    = namespace     ,
                                        data_key     = 'configs'     ,
                                        data_file_id = f'config-{i}' )

        # Action: Delete only 'logs' path
        delete_result = self.data_delete.delete__all__data__files__with__key(
            cache_id  = cache_id  ,
            namespace = namespace ,
            data_key  = 'logs'
        )

        # Verify: Only logs deleted (3 files)
        assert delete_result.get('deleted_count') == 3

        # NOTE: GAP - No way to verify configs files still exist without admin access
        # Would need: client.data().list(cache_id, namespace, data_key='configs')

    # ═════════════════════════════════════════════════════════════════════════════
    # Edge Cases and Error Scenarios
    # ═════════════════════════════════════════════════════════════════════════════

    def test__data_store__empty_string(self):
        """Test storing empty string data"""
        # Setup
        namespace  = 'test-data-edge-empty-string'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store empty string
        store_result = self.helpers.add_data_string(cache_id  = cache_id  ,
                                                    namespace = namespace ,
                                                    data      = ''        )

        assert store_result is None

    def test__data_store__empty_json(self):
        """Test storing empty JSON object"""
        # Setup
        namespace  = 'test-data-edge-empty-json'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store empty dict
        store_result = self.helpers.add_data_json(cache_id  = cache_id  ,
                                                  namespace = namespace ,
                                                  data      = {}        )

        assert store_result is None

    def test__data_store__empty_binary(self):
        """Test storing empty binary data"""
        # Setup
        namespace  = 'test-data-edge-empty-binary'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store empty bytes
        store_result = self.helpers.add_data_binary(cache_id  = cache_id  ,
                                                    namespace = namespace ,
                                                    data      = b''       )

        assert store_result is None


    def test__data_store__large_string(self):
        """Test storing large string data (1MB+)"""
        # Setup
        namespace  = 'test-data-edge-large-string'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store 1MB string
        large_data   = 'x' * (1024 * 1024)                                          # 1MB
        store_result = self.helpers.add_data_string(cache_id  = cache_id  ,
                                                    namespace = namespace ,
                                                    data      = large_data)

        # Verify: Stored successfully
        assert store_result.file_size == 1024 * 1024

        # Verify: Can retrieve large data
        data_file_id = store_result.file_id
        retrieved    = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert len(retrieved) == 1024 * 1024
        assert retrieved      == large_data

    def test__data_store__special_characters_in_keys(self):
        """Test data keys with special characters"""
        # Setup
        namespace  = 'test-data-edge-special-chars'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store with special characters in key (will be sanitized by Safe_Str)
        data_key     = 'logs/app name/file-with-spaces'
        data_file_id = 'file-with-dashes_and_underscores'
        store_result = self.helpers.add_data_string(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_key     = data_key     ,
                                                    data_file_id = data_file_id ,
                                                    data         = 'test_data'  )

        # Verify: Stored (keys may be sanitized)
        assert store_result.file_id == data_file_id

        # Verify: Can retrieve using sanitized key
        retrieved_key = store_result.data_key                                    # Get actual sanitized key
        retrieved     = self.data_retrieve.data__string__with__id_and_key(
            cache_id     = cache_id      ,
            namespace    = namespace     ,
            data_key     = retrieved_key ,
            data_file_id = data_file_id
        )
        assert retrieved == 'test_data'

    def test__data_store__unicode_content(self):
        """Test storing Unicode content"""
        # Setup
        namespace  = 'test-data-edge-unicode'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Action: Store Unicode string
        unicode_data = '你好世界 🌍 مرحبا العالم Привет мир'
        store_result = self.helpers.add_data_string(cache_id  = cache_id     ,
                                                    namespace = namespace    ,
                                                    data      = unicode_data )

        # Verify: Retrieved correctly
        data_file_id = store_result.file_id
        retrieved    = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert retrieved == unicode_data

    # ═════════════════════════════════════════════════════════════════════════════
    # Integration Tests - Complex Multi-Step Workflows
    # ═════════════════════════════════════════════════════════════════════════════

    def test__integration__create_retrieve_update_delete_workflow(self):
        """Test complete lifecycle: create → retrieve → update → delete"""
        # Setup
        namespace  = 'test-integration-lifecycle'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Step 1: Create initial data file
        data_file_id = 'config-file'
        initial_data = 'version_1'
        self.helpers.add_data_string(cache_id     = cache_id     ,
                                    namespace    = namespace    ,
                                    data_file_id = data_file_id ,
                                    data         = initial_data )

        # Step 2: Retrieve and verify
        retrieved_v1 = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert retrieved_v1 == initial_data

        # Step 3: Update (overwrite with same file_id)
        updated_data = 'version_2'
        self.helpers.add_data_string(cache_id     = cache_id     ,
                                    namespace    = namespace    ,
                                    data_file_id = data_file_id ,
                                    data         = updated_data )

        # Step 4: Retrieve updated version
        retrieved_v2 = self.data_retrieve.data__string__with__id(cache_id     = cache_id     ,
                                                                 namespace    = namespace    ,
                                                                 data_file_id = data_file_id )
        assert retrieved_v2 == updated_data
        assert retrieved_v2 != retrieved_v1

        # Step 5: Delete
        self.data_delete.delete__all__data__files(cache_id  = cache_id  ,
                                                  namespace = namespace )

        # Step 6: Verify deletion
        assert self.helpers.verify_data_file_exists(cache_id     = cache_id     ,
                                                   data_file_id = data_file_id ,
                                                   namespace    = namespace    ) is False

    def test__integration__mixed_data_types_same_entry(self):
        """Test storing and retrieving mixed data types on same entry"""
        # Setup
        namespace  = 'test-integration-mixed'
        main_entry = self.helpers.create_string_entry(namespace = namespace)
        cache_id   = main_entry.cache_id

        # Store different types
        string_data = 'text_content'
        json_data   = {'key': 'value', 'number': 123}
        binary_data = random_bytes(length=100)

        string_result = self.helpers.add_data_string(cache_id     = cache_id      ,
                                                     namespace    = namespace     ,
                                                     data_file_id = 'text-file'   ,
                                                     data         = string_data   )

        json_result = self.helpers.add_data_json(cache_id     = cache_id      ,
                                                namespace    = namespace     ,
                                                data_file_id = 'json-file'   ,
                                                data         = json_data     )

        binary_result = self.helpers.add_data_binary(cache_id     = cache_id      ,
                                                     namespace    = namespace     ,
                                                     data_file_id = 'binary-file' ,
                                                     data         = binary_data   )

        # Verify: All stored successfully
        assert string_result.data_type == 'string'
        assert json_result.data_type   == 'json'
        assert binary_result.data_type == 'binary'

        # Retrieve each type correctly
        retrieved_string = self.data_retrieve.data__string__with__id(cache_id     = cache_id    ,
                                                                     namespace    = namespace   ,
                                                                     data_file_id = 'text-file' )

        retrieved_json = self.data_retrieve.data__json__with__id(cache_id     = cache_id    ,
                                                                 namespace    = namespace   ,
                                                                 data_file_id = 'json-file' )

        retrieved_binary = self.data_retrieve.data__binary__with__id(cache_id     = cache_id      ,
                                                                     namespace    = namespace     ,
                                                                     data_file_id = 'binary-file' )

        # Verify: All correct
        assert retrieved_string == string_data
        assert retrieved_json   == json_data
        assert retrieved_binary == binary_data


# ═════════════════════════════════════════════════════════════════════════════════
# Additional Gaps Identified During Test Development
# ═════════════════════════════════════════════════════════════════════════════════
"""
NEW GAPS FOUND:

1. No client method to delete single data file by ID
   - Have: delete__all__data__files() - deletes all
   - Have: delete__all__data__files__with__key() - deletes by key
   - Missing: delete__data__file__with__id(cache_id, data_file_id, namespace)
   
2. No client method to list data files for an entry
   - Would need: client.data().list(cache_id, namespace) -> List[data_file_info]
   - Currently impossible to enumerate data files without admin access
   
3. No client method to update/replace data file content
   - Currently: Re-storing with same file_id overwrites (undocumented behavior)
   - Should have: client.data_store().update(...) explicit method
   
4. No client method to get data file metadata without content
   - Would need: client.data().info(cache_id, data_file_id, namespace)
   - Returns: size, type, timestamp without retrieving full content
   
5. No batch data operations
   - Would need: client.data_store().store_multiple([...])
   - Would need: client.data().retrieve_multiple([...])
   
6. No data file existence check without retrieval
   - Would need: client.data().exists(cache_id, data_file_id, namespace) -> bool
   - Currently must try retrieve and catch error (inefficient)
   
7. Error handling unclear
   - What happens when retrieving non-existent data file?
   - What error types are returned?
   - Need standardized error responses
"""