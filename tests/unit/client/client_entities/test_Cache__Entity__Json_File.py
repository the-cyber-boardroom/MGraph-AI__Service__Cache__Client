# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Entity__Json_File - Tests for Cache__Entity__Json_File
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service             import register_cache_service__in_memory
from mgraph_ai_service_cache_client.client.client_entities.Cache__Entity__Data_File         import Cache__Entity__Data_File
from mgraph_ai_service_cache_client.client.client_entities.Cache__Entity__Json_File         import Cache__Entity__Json_File
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Store__Response import Schema__Cache__Data__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Objects                                                              import base_types


class test_Cache__Entity__Json_File(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects
        cls.cache_client  = register_cache_service__in_memory(return_client=True)
        cls.namespace     = 'test-cache-entity-json-file'
        cls.cache_key     = 'test/json-file'
        cls.file_id       = 'root'
        cls.data_key      = 'config'
        cls.data_file_id  = 'settings'
        cls.sample_data   = {'cache_key': cls.cache_key}
        cls.sample_json   = {'name': 'test', 'count': 42, 'enabled': True}
        cls.cache_id      = cls.create_test_entity()

    @classmethod
    def create_test_entity(cls):                                                            # Create entity for tests
        response = cls.cache_client.store().store__json__cache_key(namespace       = cls.namespace                       ,
                                                                   strategy        = Enum__Cache__Store__Strategy.KEY_BASED,
                                                                   cache_key       = cls.cache_key                        ,
                                                                   body            = cls.sample_data                      ,
                                                                   file_id         = cls.file_id                          ,
                                                                   json_field_path = 'cache_key'                          )
        return response.cache_id if response else None

    def json_file(self) -> Cache__Entity__Json_File:                                        # Helper to create JSON file wrapper
        return Cache__Entity__Json_File(cache_client = self.cache_client  ,
                                        cache_id     = self.cache_id      ,
                                        namespace    = self.namespace     ,
                                        data_key     = self.data_key      ,
                                        data_file_id = self.data_file_id  )

    # ═══════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test inheritance
        with Cache__Entity__Json_File() as _:
            assert type(_)       is Cache__Entity__Json_File
            assert base_types(_) == [Cache__Entity__Data_File, Type_Safe, object]

    def test__init____with_values(self):                                                    # Test with values provided
        with self.json_file() as _:
            assert _.cache_client is self.cache_client
            assert _.cache_id     == self.cache_id
            assert _.namespace    == self.namespace
            assert _.data_key     == self.data_key
            assert _.data_file_id == self.data_file_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Store Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_store(self):                                                                   # Test storing JSON
        with self.json_file() as _:
            result = _.store(self.sample_json)

            assert type(result)     is Schema__Cache__Data__Store__Response
            assert result.cache_id  == self.cache_id
            assert result.data_key  == self.data_key
            assert result.file_id   == self.data_file_id
            assert result.data_type == 'json'
            assert result.obj()     == __(cache_id           = self.cache_id                                                                        ,
                                          data_files_created = ['test-cache-entity-json-file/data/key-based/test/json-file/root/data/config/settings.json'],
                                          data_key           = 'config'                                                                             ,
                                          data_type          = 'json'                                                                               ,
                                          extension          = 'json'                                                                               ,
                                          file_id            = 'settings'                                                                           ,
                                          file_size          = __SKIP__                                                                             ,
                                          namespace          = 'test-cache-entity-json-file'                                                        ,
                                          timestamp          = __SKIP__                                                                             )

    # ═══════════════════════════════════════════════════════════════════════════
    # Retrieve Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_retrieve(self):                                                                # Test retrieving JSON
        with self.json_file() as _:
            _.store(self.sample_json)

            result = _.retrieve()

            assert result == self.sample_json

    def test_retrieve__not_found(self):                                                     # Test retrieving non-existent JSON
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'nonexistent'    ,
                                      data_file_id = 'file'           ) as _:
            result = _.retrieve()

            assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Exists Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_exists(self):                                                                  # Test checking JSON existence
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'exists-test'    ,
                                      data_file_id = 'file'           ) as _:
            _.store({'test': 'data'})

            result = _.exists()

            assert result is True

    def test_exists__not_found(self):                                                       # Test non-existent JSON
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'no-file'        ,
                                      data_file_id = 'test'           ) as _:
            result = _.exists()

            assert result is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Update Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_update(self):                                                                  # Test updating JSON
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'update-test'    ,
                                      data_file_id = 'file'           ) as _:
            _.store({'status': 'initial'})

            result = _.update({'status': 'updated'})

            assert result is True
            assert _.retrieve()['status'] == 'updated'

    # ═══════════════════════════════════════════════════════════════════════════
    # Delete Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_delete(self):                                                                  # Test deleting JSON
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'delete-test'    ,
                                      data_file_id = 'file'           ) as _:
            _.store({'to': 'delete'})
            assert _.exists() is True

            result = _.delete()

            assert result is True
            assert _.exists() is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_full_json_workflow(self):                                                      # Test complete JSON file workflow
        with Cache__Entity__Json_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'workflow'       ,
                                      data_file_id = 'data'           ) as _:
            # Store
            data = {'version': 1, 'items': ['a', 'b', 'c']}
            _.store(data)
            assert _.exists()   is True
            assert _.retrieve() == data

            # Update
            updated_data = {'version': 2, 'items': ['a', 'b', 'c', 'd']}
            _.update(updated_data)
            assert _.retrieve() == updated_data

            # Delete
            _.delete()
            assert _.exists() is False

    def test_uses_parent_methods(self):                                                     # Verify store/retrieve use parent's store_json/json
        with self.json_file() as _:
            data = {'test': 'parent-methods'}

            # store() should use parent's store_json()
            _.store(data)

            # retrieve() should use parent's json()
            assert _.retrieve() == _.json()

            # exists() should use parent's exists__json()
            assert _.exists() == _.exists__json()