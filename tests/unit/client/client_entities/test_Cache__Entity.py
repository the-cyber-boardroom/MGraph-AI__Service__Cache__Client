# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Entity - Tests for Cache__Entity bound client
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.utils.Version                                           import version__mgraph_ai_service_cache_client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_entities.Cache__Entity                    import Cache__Entity
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Retrieve__Success          import Schema__Cache__Retrieve__Success
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__List__Response  import Schema__Cache__Data__List__Response
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Store__Response import Schema__Cache__Data__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type              import Enum__Cache__Data_Type
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__File__Metadata        import Schema__Cache__File__Metadata
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__File__Refs            import Schema__Cache__File__Refs
from mgraph_ai_service_cache_client.schemas.cache.safe_str.Safe_Str__Cache__Namespace       import Safe_Str__Cache__Namespace
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.utils.Objects                                                              import base_types
from tests.unit.Cache_Client__Fast_API__Test_Objs                                           import client_cache_service


class test_Cache__Entity(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Shared test objects
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.namespace   = 'test-cache-entity'
        cls.cache_key   = 'test/entity'
        cls.file_id     = 'root'
        cls.sample_data = {'cache_key': cls.cache_key, 'name': 'test entity'}
        cls.cache_id    = cls.create_test_entity()

    @classmethod
    def create_test_entity(cls):                                                            # Create entity for tests
        response = cls.cache_client.store().store__json__cache_key(namespace       = cls.namespace                       ,
                                                                   strategy        = Enum__Cache__Store__Strategy.KEY_BASED,
                                                                   cache_key       = cls.cache_key                        ,
                                                                   body            = cls.sample_data                      ,
                                                                   file_id         = cls.file_id                          ,
                                                                   json_field_path = 'cache_key'                          )
        return response.cache_id if response else None

    def entity(self) -> Cache__Entity:                                                      # Helper to create bound entity
        return Cache__Entity(cache_client = self.cache_client,
                             cache_id     = self.cache_id    ,
                             namespace    = self.namespace   )

    # ═══════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Cache__Entity() as _:
            assert type(_)              is Cache__Entity
            assert base_types(_)        == [Type_Safe, object]
            assert type(_.cache_client) is Cache__Service__Fast_API__Client
            assert type(_.cache_id)     is Cache_Id
            assert type(_.namespace)    is Safe_Str__Cache__Namespace
            assert _.obj()              == __(cache_client=__(config=__(base_url=None,
                                                                         api_key=None,
                                                                         api_key_header=None,
                                                                         mode='in_memory',
                                                                         fast_api_app=None,
                                                                         timeout=30,
                                                                         service_name='Cache__Service__Fast_API',
                                                                         service_version=version__mgraph_ai_service_cache_client)),
                                               cache_id='',
                                               namespace='')

    def test__init____with_values(self):                                                    # Test with values provided
        with self.entity() as _:
            assert _.cache_client   is self.cache_client
            assert _.cache_id       == self.cache_id
            assert _.namespace      == self.namespace

    # ═══════════════════════════════════════════════════════════════════════════
    # Entry Operations Tests (Tier 1)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_entry__json(self):                                                                   # Test getting entry data
        with self.entity() as _:
            result = _.entry__json()

            assert type(result) is dict
            assert result       == self.sample_data

    def test_entry__with_metadata(self):                                                             # Test getting full entry with metadata
        with self.entity() as _:
            result = _.entry__with_metadata()

            assert type(result)             is Schema__Cache__Retrieve__Success
            assert result.data              == self.sample_data
            assert result.metadata          is not None
            assert result.metadata.cache_id == self.cache_id
            assert result.obj()             == __(data=__(cache_key='test/entity', name='test entity'),
                                                          metadata=__(cache_id=self.cache_id,
                                                                      cache_hash='3fe62295e631cace',
                                                                      cache_key='test/entity',
                                                                      file_id='root',
                                                                      namespace='test-cache-entity',
                                                                      strategy='key_based',
                                                                      stored_at=__SKIP__,
                                                                      file_type='json',
                                                                      content_encoding=None,
                                                                      content_size=0),
                                                          data_type='json')

    def test_metadata(self):                                                                # Test getting entry metadata
        with self.entity() as _:
            result = _.metadata()

            assert type(result)            is Schema__Cache__File__Metadata
            assert result.data             is not None
            assert result.data.cache_id    == self.cache_id
            assert result.data.namespace   == self.namespace
            assert result.obj()            == __(content__size=57,
                                                 tags=[],
                                                 timestamp=__SKIP__,
                                                 data=__(cache_hash='3fe62295e631cace',
                                                         cache_key='test/entity',
                                                         cache_id=self.cache_id,
                                                         content_encoding=None,
                                                         file_id='root',
                                                         file_type='json',
                                                         json_field_path='cache_key',
                                                         namespace='test-cache-entity',
                                                         stored_at=__SKIP__,
                                                         strategy='key_based'),
                                                 content__hash='4a8b4bbb4c',
                                                 chain_hash=None,
                                                 previous_version_path=None)

    def test_refs(self):                                                                    # Test getting file references
        with self.entity() as _:
            result = _.refs()

            assert type(result)   is Schema__Cache__File__Refs
            assert result.cache_id   == self.cache_id
            assert result.namespace  == self.namespace
            assert len(result.all_paths.data) == 3                                           # Should have data files
            assert result.obj() == __(all_paths=__SKIP__,
                                      cache_id=self.cache_id,
                                      cache_hash='3fe62295e631cace',
                                      file_paths=__(content_files=['test-cache-entity/data/key-based/test/entity/root.json'],
                                                    data_folders=['test-cache-entity/data/key-based/test/entity/root/data']),
                                      file_type='json',
                                      namespace='test-cache-entity',
                                      strategy='key_based',
                                      timestamp=__SKIP__,)

    def test_exists(self):                                                                  # Test checking entity existence
        with self.entity() as _:
            result = _.exists()

            assert result is True

    def test_exists__not_found(self):                                                       # Test non-existent entity
        with Cache__Entity(cache_client = self.cache_client            ,
                           cache_id     = Cache_Id.new()               ,
                           namespace    = self.namespace               ) as _:
            result = _.exists()

            assert result is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Data Store Operations Tests (Tier 2)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_data__store_string(self):                                                      # Test storing string data
        with self.entity() as _:
            content = '<html><body><p>Test HTML</p></body></html>'

            result = _.data__store_string(data_key     = 'html'  ,
                                          data_file_id = 'raw'   ,
                                          content      = content )

            assert type(result)      is Schema__Cache__Data__Store__Response
            assert result.cache_id   == self.cache_id
            assert result.data_key   == 'html'
            assert result.file_id    == 'raw'
            assert result.data_type  == 'string'
            assert result.file_size  == len(content)

    def test_data__store_json(self):                                                        # Test storing JSON data
        with self.entity() as _:
            data = {'flow_id': 'test-flow', 'status': 'completed', 'tasks': []}

            result = _.data__store_json(data_key     = 'html/raw',
                                        data_file_id = 'flow'    ,
                                        data         = data      )

            assert type(result)      is Schema__Cache__Data__Store__Response
            assert result.cache_id   == self.cache_id
            assert result.data_key   == 'html/raw'
            assert result.file_id    == 'flow'
            assert result.data_type  == 'json'
            assert result.obj()      == __(cache_id=self.cache_id,
                                           data_files_created=['test-cache-entity/data/key-based/test/entity/root/data/html/raw/flow.json'],
                                           data_key='html/raw',
                                           data_type='json',
                                           extension='json',
                                           file_id='flow',
                                           file_size=74,
                                           namespace='test-cache-entity',
                                           timestamp=__SKIP__)

    # ═══════════════════════════════════════════════════════════════════════════
    # Data Retrieve Operations Tests (Tier 2)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_data__string(self):                                                            # Test retrieving string data
        with self.entity() as _:
            content = '<html><body><p>Retrieve test</p></body></html>'
            result  = _.data__store_string(data_key='test', data_file_id='retrieve', content=content)

            assert _.data__string(data_key='test', data_file_id='retrieve') == content
            assert result.obj()                                             == __(cache_id=self.cache_id,
                                                                                  data_files_created=['test-cache-entity/data/key-based/test/entity/root/data/test/retrieve.txt'],
                                                                                  data_key='test',
                                                                                  data_type='string',
                                                                                  extension='txt',
                                                                                  file_id='retrieve',
                                                                                  file_size=46,
                                                                                  namespace='test-cache-entity',
                                                                                  timestamp=__SKIP__)

    def test_data__string__not_found(self):                                                 # Test retrieving non-existent string
        with self.entity() as _:
            result = _.data__string(data_key='nonexistent', data_file_id='file')

            assert result is None

    def test_data__json(self):                                                              # Test retrieving JSON data
        with self.entity() as _:
            data = {'key': 'value', 'count': 42}
            _.data__store_json(data_key='test', data_file_id='json-retrieve', data=data)

            result = _.data__json(data_key='test', data_file_id='json-retrieve')

            assert result == data

    def test_data__exists(self):                                                            # Test checking data file existence
        with self.entity() as _:
            _.data__store_string(data_key='exists-test', data_file_id='file', content='test')

            result = _.data__exists(data_key='exists-test', data_file_id='file')

            assert result is True
            assert _.data__delete(data_key='exists-test', data_file_id='file') is True

    def test_data__exists__not_found(self):                                                 # Test non-existent data file
        with self.entity() as _:
            result = _.data__exists(data_key='nonexistent', data_file_id='file')

            assert result is False

    def test_data__exists__json_type(self):                                                 # Test checking JSON data existence
        with self.entity() as _:
            _.data__store_json(data_key='json-exists', data_file_id='test', data={'a': 1})

            result = _.data__exists(data_key  = 'json-exists'              ,
                                    data_file_id = 'test'                  ,
                                    data_type    = Enum__Cache__Data_Type.JSON)

            assert result is True
            assert _.data__delete(data_key     = 'json-exists',
                                  data_file_id = 'test',
                                  data_type    = Enum__Cache__Data_Type.JSON) is True

    # ═══════════════════════════════════════════════════════════════════════════
    # Data List Operations Tests (Tier 2)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_data__files(self):                                                             # Test listing all data files
        with self.entity() as _:
            _.data__store_string(data_key='list-test', data_file_id='file1', content='a')
            _.data__store_string(data_key='list-test', data_file_id='file2', content='b')

            result = _.data__files()

            assert type(result)      is Schema__Cache__Data__List__Response
            assert len(result.files) == 2                                                   # At least our 2 files
            assert result.obj()      == __(cache_id=self.cache_id,
                                           namespace='test-cache-entity',
                                           data_key='',
                                           file_count=2,
                                           files=[__(data_file_id='file1',
                                                     data_key='list-test',
                                                     data_type='string',
                                                     file_path='test-cache-entity/data/key-based/test/entity/root/data/list-test/file1.txt',
                                                     file_size=1,
                                                     extension='txt'),
                                                  __(data_file_id='file2',
                                                     data_key='list-test',
                                                     data_type='string',
                                                     file_path='test-cache-entity/data/key-based/test/entity/root/data/list-test/file2.txt',
                                                     file_size=1,
                                                     extension='txt')],
                                           total_size=2)

    def test_data__files__with_filter(self):                                                # Test listing with data_key filter
        with self.entity() as _:
            _.data__store_string(data_key='filter-a', data_file_id='file', content='a')
            _.data__store_string(data_key='filter-b', data_file_id='file', content='b')

            result = _.data__files(data_key='filter-a')

            assert type(result)  is Schema__Cache__Data__List__Response
            assert result.obj()  == __(cache_id=self.cache_id,
                                       namespace='test-cache-entity',
                                       data_key='filter-a',
                                       file_count=1,
                                       files=[__(data_file_id='file',
                                                 data_key='filter-a',
                                                 data_type='string',
                                                 file_path='test-cache-entity/data/key-based/test/entity/root/data/filter-a/file.txt',
                                                 file_size=1,
                                                 extension='txt')],
                                       total_size=1)


    # ═══════════════════════════════════════════════════════════════════════════
    # Data Update Operations Tests (Tier 2)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_data__update_string(self):                                                     # Test updating string data
        with self.entity() as _:
            _.data__store_string(data_key='update-test', data_file_id='str', content='original')

            result = _.data__update_string(data_key     = 'update-test',
                                           data_file_id = 'str'        ,
                                           content      = 'updated'    )

            assert result is True
            assert _.data__string(data_key='update-test', data_file_id='str') == 'updated'

    def test_data__update_json(self):                                                       # Test updating JSON data
        with self.entity() as _:
            _.data__store_json(data_key='update-json', data_file_id='data', data={'v': 1})

            result = _.data__update_json(data_key     = 'update-json',
                                         data_file_id = 'data'       ,
                                         data         = {'v': 2}     )

            assert result is True
            assert _.data__json(data_key='update-json', data_file_id='data') == {'v': 2}

    # ═══════════════════════════════════════════════════════════════════════════
    # Data Delete Operations Tests (Tier 2)
    # ═══════════════════════════════════════════════════════════════════════════

    def test_data__delete(self):                                                            # Test deleting data file
        with self.entity() as _:
            _.data__store_string(data_key='delete-test', data_file_id='file', content='to delete')
            assert _.data__exists(data_key='delete-test', data_file_id='file') is True

            result = _.data__delete(data_key='delete-test', data_file_id='file')

            assert result is True
            assert _.data__exists(data_key='delete-test', data_file_id='file') is False

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_flow_data_storage_pattern(self):                                               # Test the html/raw/flow.json pattern
        with self.entity() as _:
            html_content = '<html><body><p>Integration test</p></body></html>'
            flow_data    = {'flow_id'   : 'flow_id___abc123'              ,
                            'flow_name' : 'action__html_to_cache__save'   ,
                            'status'    : 'completed'                     ,
                            'duration'  : 0.006                           }

            # Store HTML
            result__store_string = _.data__store_string(data_key='html', data_file_id='raw', content=html_content)

            # Store flow data alongside
            result__store_json = _.data__store_json(data_key='html/raw', data_file_id='flow', data=flow_data)

            assert result__store_string.obj() == __(cache_id=self.cache_id,
                                                    data_files_created=['test-cache-entity/data/key-based/test/entity/root/data/html/raw.txt'],
                                                    data_key='html',
                                                    data_type='string',
                                                    extension='txt',
                                                    file_id='raw',
                                                    file_size=49,
                                                    namespace='test-cache-entity',
                                                    timestamp=__SKIP__)
            assert result__store_json.obj()  == __(cache_id=self.cache_id,
                                                   data_files_created=['test-cache-entity/data/key-based/test/entity/root/data/html/raw/flow.json'],
                                                   data_key='html/raw',
                                                   data_type='json',
                                                   extension='json',
                                                   file_id='flow',
                                                   file_size=135,
                                                   namespace='test-cache-entity',
                                                   timestamp=__SKIP__)
            assert _.data__files__paths().contains([ 'test-cache-entity/data/key-based/test/entity/root/data/html/raw.txt',
                                                      'test-cache-entity/data/key-based/test/entity/root/data/html/raw/flow.json']) is True

            # Verify both exist
            assert _.data__exists(data_key='html'    , data_file_id='raw')              is True
            assert _.data__exists(data_key='html/raw', data_file_id='flow',
                                  data_type=Enum__Cache__Data_Type.JSON)                is True

            # Retrieve and verify
            assert _.data__string(data_key='html', data_file_id='raw') == html_content
            assert _.data__json  (data_key='html/raw', data_file_id='flow') == flow_data

    def test_entity_complete_workflow(self):                                                # Test complete entity workflow
        with self.entity() as _:
            # Verify entity exists
            assert _.exists() is True

            # Get entry data
            entry = _.entry__json()
            assert entry == self.sample_data

            # Get metadata
            metadata = _.metadata()
            assert metadata.data.cache_id == self.cache_id

            # Get refs
            refs = _.refs()
            assert refs.cache_id == self.cache_id

            # Store data
            _.data__store_string(data_key='workflow', data_file_id='test', content='complete')

            # Verify in file list
            files = _.data__files(data_key='workflow')
            assert len(files.files) >= 1
