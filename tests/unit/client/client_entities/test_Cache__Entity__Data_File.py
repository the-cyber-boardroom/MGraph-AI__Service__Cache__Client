# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Entity__Data_File - Tests for Cache__Entity__Data_File bound client
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client              import Cache__Service__Client
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service             import register_cache_service__in_memory
from mgraph_ai_service_cache_client.client.client_entities.Cache__Entity                    import Cache__Entity
from mgraph_ai_service_cache_client.client.client_entities.Cache__Entity__Data_File         import Cache__Entity__Data_File
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Store__Response import Schema__Cache__Data__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__File__Data_Key  import Safe_Str__Cache__File__Data_Key
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__File__File_Id   import Safe_Str__Cache__File__File_Id
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__Namespace       import Safe_Str__Cache__Namespace
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.utils.Objects                                                              import base_types


class test_Cache__Entity__Data_File(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects
        cls.cache_client  = register_cache_service__in_memory(return_client=True)
        cls.namespace     = 'test-cache-data-file'
        cls.cache_key     = 'test/data-file'
        cls.file_id       = 'root'
        cls.data_key      = 'html'
        cls.data_file_id  = 'raw'
        cls.sample_data   = {'cache_key': cls.cache_key}
        cls.sample_html   = '<html><body><p>Test content</p></body></html>'
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

    def data_file(self) -> Cache__Entity__Data_File:                                               # Helper to create bound data file
        return Cache__Entity__Data_File(cache_client = self.cache_client ,
                                        cache_id     = self.cache_id     ,
                                        namespace    = self.namespace    ,
                                        data_key     = self.data_key     ,
                                        data_file_id = self.data_file_id )

    # ═══════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Cache__Entity__Data_File() as _:
            assert type(_)          is Cache__Entity__Data_File
            assert base_types(_)    == [Type_Safe, object]
            assert type(_.cache_client)   is Cache__Service__Client
            assert type(_.cache_id    )   is Cache_Id
            assert type(_.namespace   )   is Safe_Str__Cache__Namespace
            assert type(_.data_key    )   is Safe_Str__Cache__File__Data_Key
            assert type(_.data_file_id)   is Safe_Str__Cache__File__File_Id

    def test__init____with_values(self):                                                    # Test with values provided
        with self.data_file() as _:
            assert _.cache_client   is self.cache_client
            assert _.cache_id       == self.cache_id
            assert _.namespace      == self.namespace
            assert _.data_key       == self.data_key
            assert _.data_file_id   == self.data_file_id


    # ═══════════════════════════════════════════════════════════════════════════
    # Content Operations Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_store_string(self):                                                            # Test storing string content
        with self.data_file() as _:
            result = _.store__string(self.sample_html)

            assert type(result)      is Schema__Cache__Data__Store__Response
            assert result.cache_id   == self.cache_id
            assert result.data_key   == self.data_key
            assert result.file_id    == self.data_file_id
            assert result.data_type  == 'string'
            assert result.file_size  == len(self.sample_html)
            assert result.obj()      == __(cache_id=self.cache_id,
                                           data_files_created=['test-cache-data-file/data/key-based/test/data-file/root/data/html/raw.txt'],
                                           data_key='html',
                                           data_type='string',
                                           extension='txt',
                                           file_id='raw',
                                           file_size=45,
                                           namespace='test-cache-data-file',
                                           timestamp=__SKIP__)

    def test_string(self):                                                                  # Test retrieving string content
        with self.data_file() as _:
            result = _.store__string(self.sample_html)
            assert _.string()    == self.sample_html
            assert result.obj()  == __(cache_id=self.cache_id,
                                       data_files_created=['test-cache-data-file/data/key-based/test/data-file/root/data/html/raw.txt'],
                                       data_key='html',
                                       data_type='string',
                                       extension='txt',
                                       file_id='raw',
                                       file_size=45,
                                       namespace='test-cache-data-file',
                                       timestamp=__SKIP__)


    def test_string__not_found(self):                                                       # Test retrieving non-existent string
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'nonexistent'    ,
                               data_file_id = 'file'           ) as _:
            result = _.string()

            assert result is None

    def test_exists__string(self):                                                                  # Test checking content existence
        with self.data_file() as _:
            _.store__string(self.sample_html)

            result = _.exists__string()

            assert result is True

    def test_exists__not_found(self):                                                       # Test non-existent content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'nonexistent'    ,
                               data_file_id = 'file'           ) as _:
            result = _.exists__string()

            assert result is False

    def test_store_json(self):                                                              # Test storing JSON content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'test-json'      ,
                               data_file_id = 'data'           ) as _:
            data   = {'key': 'value', 'count': 42}
            result = _.store__json(data)

            assert type(result)     is Schema__Cache__Data__Store__Response
            assert result.data_type == 'json'
            assert result.obj()     == __(cache_id=self.cache_id,
                                          data_files_created=['test-cache-data-file/data/key-based/test/data-file/root/data/test-json/data.json'],
                                          data_key='test-json',
                                          data_type='json',
                                          extension='json',
                                          file_id='data',
                                          file_size=39,
                                          namespace='test-cache-data-file',
                                          timestamp=__SKIP__)

    def test_json(self):                                                                    # Test retrieving JSON content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'test-json-get'  ,
                               data_file_id = 'data'           ) as _:
            data  = {'key': 'value', 'count': 42}
            result = _.store__json(data)

            assert _.json() == data

            assert result.obj() == __( cache_id=self.cache_id,
                                       data_files_created=['test-cache-data-file/data/key-based/test/data-file/root/data/test-json-get/data.json'],
                                       data_key='test-json-get',
                                       data_type='json',
                                       extension='json',
                                       file_id='data',
                                       file_size=39,
                                       namespace='test-cache-data-file',
                                       timestamp=__SKIP__)

    def test_update_string(self):                                                           # Test updating string content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'update-str'     ,
                               data_file_id = 'data'           ) as _:
            _.store__string('original')

            result = _.update__string('updated')

            assert result is True
            assert _.string() == 'updated'

    def test_update_json(self):                                                             # Test updating JSON content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   ,
                               data_key     = 'update-json'    ,
                               data_file_id = 'data'           ) as _:
            _.store__json({'v': 1})

            result = _.update__json({'v': 2})

            assert result is True
            assert _.json() == {'v': 2}

    def test_delete__data_type(self):                                                                  # Test deleting content
        with Cache__Entity__Data_File(cache_client = self.cache_client,
                                      cache_id     = self.cache_id    ,
                                      namespace    = self.namespace   ,
                                      data_key     = 'delete-test'    ,
                                      data_file_id = 'data'           ) as _:
            _.store__string('to delete')
            assert _.exists__string() is True

            result = _.delete__data_type()

            assert result is True
            assert _.exists__string() is False


    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_factory_from_entity(self):                                                     # Test creating via Cache__Entity factory
        entity    = Cache__Entity(cache_client = self.cache_client,
                                  cache_id     = self.cache_id    ,
                                  namespace    = self.namespace   )
        data_file = entity.data_file(data_key='factory', data_file_id='test')

        assert type(data_file)       is Cache__Entity__Data_File
        assert data_file.cache_client is self.cache_client
        assert data_file.cache_id    == self.cache_id
        assert data_file.namespace   == self.namespace
        assert data_file.data_key    == 'factory'
        assert data_file.data_file_id == 'test'

        # Use it
        data_file.store__string('via factory')
        assert data_file.string() == 'via factory'

    def test_chained_factory_usage(self):                                                   # Test chained entity → data_file usage
        entity = Cache__Entity(cache_client = self.cache_client,
                               cache_id     = self.cache_id    ,
                               namespace    = self.namespace   )

        # One-liner to store and retrieve
        entity.data_file('chained', 'test').store__string('chained content')
        content = entity.data_file('chained', 'test').string()

        assert content == 'chained content'
