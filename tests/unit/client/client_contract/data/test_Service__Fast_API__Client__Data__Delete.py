# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Service__Fast_API__Client__Data__Delete
# Verify data file deletion operations under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                               import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client__Requests                    import Cache__Service__Client__Requests
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                             import register_cache_service__in_memory
from mgraph_ai_service_cache_client.client.client_contract.data.Cache__Service__Client__Data__Delete        import Cache__Service__Client__Data__Delete
from osbot_utils.testing.__                                                                                 import __, __SKIP__
from osbot_utils.testing.__helpers                                                                          import obj
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from osbot_utils.utils.Objects                                                                              import base_classes
from osbot_utils.utils.Misc                                                                                 import random_string
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                              import Enum__Cache__Data_Type


class test_Service__Fast_API__Client__Data__Delete(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                                            # Setup in-memory client
        #cls.client_cache_service, cls.cache_service = client_cache_service()
        cls.cache_service_client  = register_cache_service__in_memory(return_client=True)
        cls.data_delete           = cls.cache_service_client.data().delete()
        cls.data_retrieve         = cls.cache_service_client.data().retrieve()
        cls.data_store            = cls.cache_service_client.data_store()
        cls.store_client          = cls.cache_service_client.store()
        cls.test_namespace        = Safe_Str__Id("test-data-delete")

    def _create_cache_entry(self):                                                                          # Helper to create a fresh cache entry
        store_result = self.store_client.store__string(strategy  = "direct"                          ,
                                                       namespace = self.test_namespace               ,
                                                       body      = f"main entry {random_string()}"   )
        return store_result.cache_id

    def _add_data_files(self, cache_id, count=3, data_key=None):                                            # Helper to add multiple data files
        file_ids = []
        for i in range(count):
            file_id = f"data-file-{i}-{random_string(prefix='')}"
            if data_key:
                self.data_store.data__store_string__with__id_and_key(cache_id     = cache_id           ,
                                                                     namespace    = self.test_namespace,
                                                                     data_key     = data_key           ,
                                                                     data_file_id = file_id            ,
                                                                     body         = f"content {i}"     )
            else:
                self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_file_id = file_id            ,
                                                             body         = f"content {i}"     )
            file_ids.append(file_id)
        return file_ids

    def _file_exists(self, cache_id, data_file_id, data_key=None):                                          # Helper to check if data file exists
        if data_key:
            result = self.data_retrieve.data__string__with__id_and_key(cache_id     = cache_id           ,
                                                                       namespace    = self.test_namespace,
                                                                       data_key     = data_key           ,
                                                                       data_file_id = data_file_id       )
        else:
            result = self.data_retrieve.data__string__with__id(cache_id     = cache_id           ,
                                                               namespace    = self.test_namespace,
                                                               data_file_id = data_file_id       )
        return result is not None

    # ═══════════════════════════════════════════════════════════════════════════
    # Setup Verification
    # ═══════════════════════════════════════════════════════════════════════════

    def test__setUpClass(self):                                                                             # Verify test setup
        with self.data_delete as _:
            assert type(_) is Cache__Service__Client__Data__Delete
            assert base_classes(_) == [Type_Safe, object]

    def test__init__(self):                                                                                 # Test initialization
        with self.data_delete as _:
            assert type(_.requests) is Cache__Service__Client__Requests

    # ═══════════════════════════════════════════════════════════════════════════
    # delete__all__data__files - Delete All Files
    # ═══════════════════════════════════════════════════════════════════════════

    def test__delete__all__data__files__removes_all_files(self):                                            # Test deleting all data files
        cache_id = self._create_cache_entry()
        file_ids = self._add_data_files(cache_id, count=5)

        # Verify files exist
        for file_id in file_ids:
            assert self._file_exists(cache_id, file_id) is True

        with self.data_delete as _:
            result = _.delete__all__data__files(cache_id  = cache_id          ,
                                                namespace = self.test_namespace)

            assert result is not None                                                                       # Should return success response

        # Verify all files deleted
        for file_id in file_ids:
            assert self._file_exists(cache_id, file_id) is False

    def test__delete__all__data__files__empty_entry(self):                                                  # Test deleting from entry with no data files
        cache_id = self._create_cache_entry()                                                               # Entry with no data files

        with self.data_delete as _:
            result = _.delete__all__data__files(cache_id  = cache_id          ,
                                                namespace = self.test_namespace)

            assert result is not None                                                                       # Should succeed even with no files

    def test__delete__all__data__files__non_existent_cache_entry(self):                                     # Test deleting from non-existent cache entry
        non_existent_id = Cache_Id()

        with self.data_delete as _:
            result = _.delete__all__data__files(cache_id  = non_existent_id   ,
                                                namespace = self.test_namespace)
            # Should handle gracefully (may return empty result or error)

    def test__delete__all__data__files__wrong_namespace(self):                                              # Test namespace isolation
        cache_id = self._create_cache_entry()
        file_ids = self._add_data_files(cache_id, count=2)

        with self.data_delete as _:
            result = _.delete__all__data__files(cache_id  = cache_id      ,
                                                namespace = "different-ns")

        # Files should still exist in original namespace
        for file_id in file_ids:
            assert self._file_exists(cache_id, file_id) is True

    # ═══════════════════════════════════════════════════════════════════════════
    # delete__all__data__files__with__key - Delete by Key Path
    # ═══════════════════════════════════════════════════════════════════════════

    def test__delete__all__data__files__with__key__removes_only_keyed_files(self):                          # Test deleting files under specific key
        cache_id   = self._create_cache_entry()
        data_key_1 = "logs/app"
        data_key_2 = "logs/system"

        # Add files under different keys
        files_key_1 = self._add_data_files(cache_id, count=3, data_key=data_key_1)
        files_key_2 = self._add_data_files(cache_id, count=2, data_key=data_key_2)

        # Verify all files exist
        for file_id in files_key_1:
            assert self._file_exists(cache_id, file_id, data_key_1) is True
        for file_id in files_key_2:
            assert self._file_exists(cache_id, file_id, data_key_2) is True

        with self.data_delete as _:
            result = _.delete__all__data__files__with__key(cache_id  = cache_id          ,
                                                           namespace = self.test_namespace,
                                                           data_key  = data_key_1        )
            assert obj(result) == __(status='success',
                                     message='Deleted 3 data files',
                                     cache_id=cache_id,
                                     deleted_count=3,
                                     deleted_files=__SKIP__,
                                     data_key='logs/app',
                                     namespace='test-data-delete')
            assert result is not None

        # Files under key_1 should be deleted
        for file_id in files_key_1:
            assert self._file_exists(cache_id=cache_id, data_file_id=file_id, data_key=data_key_1) is False

        # Files under key_2 should still exist
        for file_id in files_key_2:
            assert self._file_exists(cache_id, file_id, data_key_2) is True

    def test__delete__all__data__files__with__key__non_existent_key(self):                                  # Test deleting from non-existent key path
        cache_id = self._create_cache_entry()
        file_ids = self._add_data_files(cache_id, count=2, data_key="existing/path")

        with self.data_delete as _:
            result = _.delete__all__data__files__with__key(cache_id  = cache_id          ,
                                                           namespace = self.test_namespace,
                                                           data_key  = "nonexistent/path")
            # Should handle gracefully

        # Original files should still exist
        for file_id in file_ids:
            assert self._file_exists(cache_id, file_id, "existing/path") is True

    def test__delete__all__data__files__with__key__nested_path(self):                                       # Test deleting from nested key path
        cache_id     = self._create_cache_entry()
        parent_key   = "data"
        child_key    = "data/reports"
        grandchild   = "data/reports/2024"

        # Add files at different nesting levels
        self._add_data_files(cache_id, count=1, data_key=parent_key)
        self._add_data_files(cache_id, count=2, data_key=child_key)
        files_gc = self._add_data_files(cache_id, count=1, data_key=grandchild)

        with self.data_delete as _:
            # Delete only grandchild level
            result = _.delete__all__data__files__with__key(cache_id  = cache_id          ,
                                                           namespace = self.test_namespace,
                                                           data_key  = grandchild        )

        # Grandchild files should be deleted
        for file_id in files_gc:
            assert self._file_exists(cache_id, file_id, grandchild) is False

    # ═══════════════════════════════════════════════════════════════════════════
    # delete__data__file__with__id - Delete Single File
    # ═══════════════════════════════════════════════════════════════════════════

    def test__delete__data__file__with__id__removes_single_file(self):                                      # Test deleting single file by ID
        cache_id = self._create_cache_entry()
        file_ids = self._add_data_files(cache_id, count=3)
        target_file = file_ids[1]                                                                           # Delete middle file

        # Verify target exists
        assert self._file_exists(cache_id, target_file) is True

        with self.data_delete as _:
            result = _.delete__data__file__with__id(cache_id     = cache_id              ,
                                                    namespace    = self.test_namespace   ,
                                                    data_type    = Enum__Cache__Data_Type.STRING,
                                                    data_file_id = target_file           )

            assert result is not None

        # Target should be deleted
        assert self._file_exists(cache_id, target_file) is False

        # Other files should still exist
        assert self._file_exists(cache_id, file_ids[0]) is True
        assert self._file_exists(cache_id, file_ids[2]) is True

    def test__delete__data__file__with__id__non_existent_file(self):                                        # Test deleting non-existent file
        cache_id = self._create_cache_entry()

        with self.data_delete as _:
            result = _.delete__data__file__with__id(cache_id     = cache_id              ,
                                                    namespace    = self.test_namespace   ,
                                                    data_type    = Enum__Cache__Data_Type.STRING,
                                                    data_file_id = "non-existent-file"   )
            # Should handle gracefully (may return error or empty response)

    def test__delete__data__file__with__id__wrong_data_type(self):                                          # Test deleting with wrong data type
        cache_id = self._create_cache_entry()

        # Store as string
        file_id = f"string-file-{random_string(prefix='')}"
        self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = file_id            ,
                                                     body         = "content"          )

        with self.data_delete as _:
            # Try to delete as JSON type (wrong type)
            result = _.delete__data__file__with__id(cache_id     = cache_id            ,
                                                    namespace    = self.test_namespace ,
                                                    data_type    = Enum__Cache__Data_Type.JSON,
                                                    data_file_id = file_id             )

        # File should still exist (wrong type specified)
        assert self._file_exists(cache_id, file_id) is True

    def test__delete__data__file__with__id__json_file(self):                                                # Test deleting JSON file
        cache_id = self._create_cache_entry()
        file_id  = f"json-file-{random_string(prefix='')}"

        self.data_store.data__store_json__with__id(cache_id     = cache_id           ,
                                                   namespace    = self.test_namespace,
                                                   data_file_id = file_id            ,
                                                   body         = {"key": "value"}   )

        # Verify exists
        json_result = self.data_retrieve.data__json__with__id(cache_id     = cache_id           ,
                                                              namespace    = self.test_namespace,
                                                              data_file_id = file_id            )
        assert json_result is not None

        with self.data_delete as _:
            result = _.delete__data__file__with__id(cache_id     = cache_id            ,
                                                    namespace    = self.test_namespace ,
                                                    data_type    = Enum__Cache__Data_Type.JSON,
                                                    data_file_id = file_id             )

        # Verify deleted
        json_result = self.data_retrieve.data__json__with__id(cache_id     = cache_id           ,
                                                              namespace    = self.test_namespace,
                                                              data_file_id = file_id            )
        assert json_result is None

    def test__delete__data__file__with__id__binary_file(self):                                              # Test deleting binary file
        cache_id = self._create_cache_entry()
        file_id  = f"binary-file-{random_string(prefix='')}"

        self.data_store.data__store_binary__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = file_id            ,
                                                     body         = bytes(range(20))   )

        # Verify exists
        binary_result = self.data_retrieve.data__binary__with__id(cache_id     = cache_id           ,
                                                                  namespace    = self.test_namespace,
                                                                  data_file_id = file_id            )
        assert binary_result is not None

        with self.data_delete as _:
            result = _.delete__data__file__with__id(cache_id     = cache_id              ,
                                                    namespace    = self.test_namespace   ,
                                                    data_type    = Enum__Cache__Data_Type.BINARY,
                                                    data_file_id = file_id               )

        # Verify deleted
        binary_result = self.data_retrieve.data__binary__with__id(cache_id     = cache_id           ,
                                                                  namespace    = self.test_namespace,
                                                                  data_file_id = file_id            )
        assert binary_result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # delete__data__file__with__id_and_key - Delete Single File with Key
    # ═══════════════════════════════════════════════════════════════════════════

    def test__delete__data__file__with__id_and_key__removes_specific_file(self):                            # Test deleting file with key path
        cache_id = self._create_cache_entry()
        data_key = "configs/production"
        file_id  = f"config-{random_string(prefix='')}"

        self.data_store.data__store_string__with__id_and_key(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_key     = data_key           ,
                                                             data_file_id = file_id            ,
                                                             body         = "config content"   )

        # Verify exists
        assert self._file_exists(cache_id, file_id, data_key) is True

        with self.data_delete as _:
            result = _.delete__data__file__with__id_and_key(cache_id     = cache_id              ,
                                                            namespace    = self.test_namespace   ,
                                                            data_type    = Enum__Cache__Data_Type.STRING,
                                                            data_key     = data_key              ,
                                                            data_file_id = file_id               )

            assert result is not None

        # Verify deleted
        assert self._file_exists(cache_id, file_id, data_key) is False

    def test__delete__data__file__with__id_and_key__wrong_key(self):                                        # Test deleting with wrong key path
        cache_id = self._create_cache_entry()
        data_key = "correct/path"
        file_id  = f"file-{random_string(prefix='')}"

        self.data_store.data__store_string__with__id_and_key(cache_id     = cache_id           ,
                                                             namespace    = self.test_namespace,
                                                             data_key     = data_key           ,
                                                             data_file_id = file_id            ,
                                                             body         = "content"          )

        with self.data_delete as _:
            # Try to delete with wrong key
            result = _.delete__data__file__with__id_and_key(cache_id     = cache_id              ,
                                                            namespace    = self.test_namespace   ,
                                                            data_type    = Enum__Cache__Data_Type.STRING,
                                                            data_key     = "wrong/path"          ,
                                                            data_file_id = file_id               )

        # File should still exist at correct path
        assert self._file_exists(cache_id, file_id, data_key) is True

    def test__delete__data__file__with__id_and_key__preserves_other_files(self):                            # Test that only target file is deleted
        cache_id = self._create_cache_entry()
        data_key = "shared/folder"

        # Add multiple files under same key
        file_ids = []
        for i in range(3):
            file_id = f"file-{i}-{random_string(prefix='')}"
            self.data_store.data__store_string__with__id_and_key(cache_id     = cache_id           ,
                                                                 namespace    = self.test_namespace,
                                                                 data_key     = data_key           ,
                                                                 data_file_id = file_id            ,
                                                                 body         = f"content {i}"     )
            file_ids.append(file_id)

        target_file = file_ids[1]

        with self.data_delete as _:
            result = _.delete__data__file__with__id_and_key(cache_id     = cache_id              ,
                                                            namespace    = self.test_namespace   ,
                                                            data_type    = Enum__Cache__Data_Type.STRING,
                                                            data_key     = data_key              ,
                                                            data_file_id = target_file           )

        # Only target should be deleted
        assert self._file_exists(cache_id, file_ids[0], data_key) is True
        assert self._file_exists(cache_id, file_ids[1], data_key) is False                                  # Deleted
        assert self._file_exists(cache_id, file_ids[2], data_key) is True

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__integration__create_delete_verify_lifecycle(self):                                            # Test complete create-delete-verify cycle
        cache_id = self._create_cache_entry()
        file_id  = f"lifecycle-{random_string(prefix='')}"

        # Step 1: Create
        self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = file_id            ,
                                                     body         = "test content"     )

        # Step 2: Verify exists
        assert self._file_exists(cache_id, file_id) is True

        # Step 3: Delete
        with self.data_delete as _:
            _.delete__data__file__with__id(cache_id     = cache_id              ,
                                           namespace    = self.test_namespace   ,
                                           data_type    = Enum__Cache__Data_Type.STRING,
                                           data_file_id = file_id               )

        # Step 4: Verify deleted
        assert self._file_exists(cache_id, file_id) is False

        # Step 5: Re-create with same ID
        self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = file_id            ,
                                                     body         = "new content"      )

        # Step 6: Verify re-created
        assert self._file_exists(cache_id, file_id) is True

    def test__integration__delete_all_then_single_operations(self):                                         # Test mixing delete operations
        cache_id = self._create_cache_entry()

        # Create files in different locations
        root_files = self._add_data_files(cache_id, count=2)
        key_files  = self._add_data_files(cache_id, count=2, data_key="subpath")

        # Delete all at root (should not affect keyed files)
        with self.data_delete as _:
            _.delete__all__data__files(cache_id  = cache_id          ,
                                       namespace = self.test_namespace)

        # Root files should be deleted, keyed files depend on implementation
        # (they may or may not be deleted by delete__all__data__files)

    def test__integration__multiple_data_types_deletion(self):                                              # Test deleting different data types
        cache_id = self._create_cache_entry()

        # Create files of different types
        string_id = f"str-{random_string(prefix='')}"
        json_id   = f"json-{random_string(prefix='')}"
        binary_id = f"bin-{random_string(prefix='')}"

        self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = string_id          ,
                                                     body         = "string"           )

        self.data_store.data__store_json__with__id(cache_id     = cache_id           ,
                                                   namespace    = self.test_namespace,
                                                   data_file_id = json_id            ,
                                                   body         = {"type": "json"}   )

        self.data_store.data__store_binary__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = binary_id          ,
                                                     body         = bytes([1,2,3])     )

        with self.data_delete as _:
            # Delete each type
            _.delete__data__file__with__id(cache_id     = cache_id                   ,
                                           namespace    = self.test_namespace        ,
                                           data_type    = Enum__Cache__Data_Type.STRING,
                                           data_file_id = string_id                  )

            _.delete__data__file__with__id(cache_id     = cache_id                 ,
                                           namespace    = self.test_namespace      ,
                                           data_type    = Enum__Cache__Data_Type.JSON,
                                           data_file_id = json_id                  )

            _.delete__data__file__with__id(cache_id     = cache_id                   ,
                                           namespace    = self.test_namespace        ,
                                           data_type    = Enum__Cache__Data_Type.BINARY,
                                           data_file_id = binary_id                  )

        # Verify all deleted
        assert self._file_exists(cache_id, string_id) is False
        assert self.data_retrieve.data__json__with__id(cache_id=cache_id, namespace=self.test_namespace, data_file_id=json_id) is None
        assert self.data_retrieve.data__binary__with__id(cache_id=cache_id, namespace=self.test_namespace, data_file_id=binary_id) is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Namespace Isolation Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__namespace_isolation__delete_in_wrong_namespace(self):                                         # Test namespace isolation for all delete methods
        cache_id = self._create_cache_entry()
        file_id  = f"isolated-{random_string(prefix='')}"

        self.data_store.data__store_string__with__id(cache_id     = cache_id           ,
                                                     namespace    = self.test_namespace,
                                                     data_file_id = file_id            ,
                                                     body         = "content"          )

        with self.data_delete as _:
            # Try delete in wrong namespace
            _.delete__data__file__with__id(cache_id     = cache_id                   ,
                                           namespace    = "wrong-namespace"          ,
                                           data_type    = Enum__Cache__Data_Type.STRING,
                                           data_file_id = file_id                    )

        # File should still exist in correct namespace
        assert self._file_exists(cache_id, file_id) is True