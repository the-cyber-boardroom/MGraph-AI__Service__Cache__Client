from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                         import __, __SKIP__
from osbot_utils.testing.__helpers                                                                  import obj
from osbot_utils.utils.Misc                                                                         import is_guid
from osbot_utils.utils.Objects                                                                      import base_classes
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from mgraph_ai_service_cache_client.client.testing.Cache_Client_Test_Helpers                        import Cache_Client_Test_Helpers
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Store__Response                    import Schema__Cache__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__Store__Response         import Schema__Cache__Data__Store__Response
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                   import client_cache_service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client         import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy                import Enum__Cache__Store__Strategy


class test_Cache_Client_Test_Helpers(TestCase):                         # Test the test helpers class itself

    @classmethod
    def setUpClass(cls) -> None:                                        # Setup in-memory client for testing helpers
        cls.client_cache_service, cls.cache_service = client_cache_service()
        cls.helpers                                 = Cache_Client_Test_Helpers(client=cls.client_cache_service)

    # ═════════════════════════════════════════════════════════════════════════════
    # Initialization & Setup
    # ═════════════════════════════════════════════════════════════════════════════

    def test__init__helper_class(self):                                             # Test helper class initialization
        with self.helpers as _:
            assert type(_)                    is Cache_Client_Test_Helpers
            assert base_classes(_)            == [Type_Safe, object]
            assert type(_.client)             is Cache__Service__Fast_API__Client
            assert _.client                   is not None
            assert _.client                   == self.client_cache_service

    def test__init__creates_new_instance(self):                                         # Test creating new helper instance
        new_helpers = Cache_Client_Test_Helpers(client=self.client_cache_service)

        assert new_helpers                    is not None
        assert type(new_helpers)              is Cache_Client_Test_Helpers
        assert new_helpers.client             == self.client_cache_service
        assert new_helpers                    is not self.helpers                  # Different instance

    # ═════════════════════════════════════════════════════════════════════════════
    # String Entry Creation - Basic Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__create_string_entry__defaults(self):                      # Test creating string entry with default parameters
        store_result = self.helpers.create_string_entry()
        result       = store_result.json()
        assert type(store_result) is Schema__Cache__Store__Response


        # Verify return structure
        assert type(result)                   is dict
        assert 'cache_id'                     in result
        assert 'cache_hash'                   in result
        assert 'namespace'                    in result
        assert 'paths'                        in result
        assert 'size'                         in result

        # Verify values
        assert is_guid(result['cache_id'])    is True
        assert result['namespace']            == 'test'                            # Default namespace
        assert result['size']                 >  0

        cache_id    = result['cache_id']
        cache_hash  = result['cache_hash']
        assert result                         == {'cache_hash': cache_hash,
                                                  'cache_id': cache_id,
                                                  'namespace': 'test',
                                                  'paths': {'by_hash': [ f'test/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json'],
                                                           'by_id'   : [ f'test/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json' ],
                                                           'data'    : [ f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',
                                                                         f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config',
                                                                         f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata']},
                                                  'size': 10}

        expected_paths      = self.helpers.build_expected_paths(cache_id=cache_id, cache_hash=cache_hash, namespace='test')
        expected_paths__obj = obj(expected_paths)

        assert expected_paths ==  {'by_hash': [ f'test/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json'],
                                   'by_id': [   f'test/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json'],
                                   'data': [    f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',
                                                f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config',
                                                f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata']}

        assert result         == { 'cache_hash': cache_hash     ,
                                   'cache_id'  : cache_id       ,
                                   'namespace' : 'test'         ,
                                   'paths'     : expected_paths ,
                                   'size'      : 10             }
        assert obj(result)    == __(cache_id   = cache_id           ,
                                    cache_hash = cache_hash         ,
                                    namespace  ='test'              ,
                                    paths      = obj(expected_paths),
                                    size       = 10                 )

        assert store_result.obj() == __(cache_id    = cache_id,
                                        cache_hash  = cache_hash ,
                                        namespace   = 'test',
                                        paths       = __(by_hash = [ f'test/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json',],
                                                         by_id   = [ f'test/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',],
                                                         data    =  [ f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',
                                                                      f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config' ,
                                                                      f'test/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata']),
                                       size=10)

        assert store_result.obj() == __(cache_id    = cache_id      ,
                                        cache_hash  = cache_hash    ,
                                        namespace   = 'test'        ,
                                        paths       = obj(expected_paths),
                                        size        = 10)

        assert store_result.obj() == __(cache_id    = cache_id           ,
                                        cache_hash  = cache_hash         ,
                                        namespace   = 'test'             ,
                                        paths       = expected_paths__obj,
                                        size        = 10                 )

        store_result_2       = self.helpers.create_string_entry()             # this will use a random value
        store_result_3       = self.helpers.create_string_entry()

        assert store_result.cache_id   != store_result_2.cache_id             # cache Ids are different
        assert store_result.cache_id   != store_result_3.cache_id
        assert store_result.cache_hash != store_result_2.cache_hash           # and so are the cache hashes
        assert store_result.cache_hash != store_result_3.cache_hash

    def test__create_string_entry__custom_namespace(self):              # Test creating string entry with custom namespace
        namespace = 'test-helpers-custom-ns'
        result    = self.helpers.create_string_entry(namespace=namespace)
        assert type(result) is Schema__Cache__Store__Response

        assert result.namespace            == namespace
        assert is_guid(result.cache_id)    is True

    def test__create_string_entry__custom_value(self):          # Test creating string entry with custom value
        custom_value = 'my_custom_test_value'
        result_1     = self.helpers.create_string_entry(value=custom_value)
        assert type(result_1) is Schema__Cache__Store__Response

        cache_id  = result_1.cache_id                             # Verify stored by retrieving
        namespace = result_1.namespace

        retrieved = self.client_cache_service.retrieve().retrieve__cache_id__string(cache_id  = cache_id  ,
                                                                                    namespace = namespace)

        assert retrieved                      == custom_value

        result_2       = self.helpers.create_string_entry(value=custom_value)
        result_3       = self.helpers.create_string_entry(value=custom_value)

        assert result_1.cache_id   != result_2.cache_id             # cache Ids are different
        assert result_1.cache_id   != result_3.cache_id
        assert result_1.cache_hash == result_2.cache_hash           # but hashes are the same
        assert result_1.cache_hash == result_2.cache_hash           # since we used the same content

    def test__create_string_entry__all_strategies(self):            # Test creating string entries with different strategies
        strategies = [  Enum__Cache__Store__Strategy.DIRECT             ,
                        Enum__Cache__Store__Strategy.TEMPORAL           ,
                        Enum__Cache__Store__Strategy.TEMPORAL_LATEST    ,
                        Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED ,
                        Enum__Cache__Store__Strategy.KEY_BASED          ]

        for strategy in strategies:
            result         = self.helpers.create_string_entry(strategy=strategy)
            cache_id       = result.cache_id
            cache_hash     = result.cache_hash
            expected_paths = obj(self.helpers.build_expected_paths(cache_id   = cache_id,
                                                                   cache_hash = cache_hash,
                                                                   strategy   = strategy))
            assert type(result) is Schema__Cache__Store__Response
            assert result.obj() == __(cache_id    = cache_id     ,
                                     cache_hash  = cache_hash    ,
                                     namespace   = 'test'        ,
                                     paths       = expected_paths,
                                     size        = 10            )


    def test__create_string_entry__with_cache_key(self):                # Test creating string entry with cache_key
        cache_key = 'test/helpers/cache/key'
        result_1  = self.helpers.create_string_entry(cache_key=cache_key)                   # strategy defaults to Enum__Cache__Store__Strategy.DIRECT

        cache_id       = result_1.cache_id
        cache_hash     = result_1.cache_hash
        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = cache_id,       # strategy defaults to Enum__Cache__Store__Strategy.DIRECT
                                                               cache_hash = cache_hash))
        assert type(result_1) is Schema__Cache__Store__Response
        assert result_1.obj() == __(cache_id    = cache_id     ,
                                    cache_hash  = cache_hash    ,
                                    namespace   = 'test'        ,
                                    paths       = expected_paths,
                                    size        = 10            )

        result_2       = self.helpers.create_string_entry(cache_key=cache_key)
        result_3       = self.helpers.create_string_entry(cache_key=cache_key)

        assert result_1.cache_id   != result_2.cache_id             # cache Ids are different
        assert result_1.cache_id   != result_3.cache_id
        assert result_1.cache_hash != result_2.cache_hash           # and so are the hashes
        assert result_1.cache_hash != result_2.cache_hash           #


        strategy  = Enum__Cache__Store__Strategy.KEY_BASED
        result_4  = self.helpers.create_string_entry(cache_key=cache_key, strategy=strategy)

        cache_id_4      = result_4.cache_id
        cache_hash_4    = result_4.cache_hash
        expected_paths_4 = obj(self.helpers.build_expected_paths(cache_id   = cache_id_4  ,
                                                                 cache_hash = cache_hash_4,
                                                                 cache_key  = cache_key   ,
                                                                 strategy   = strategy    ))

        assert result_4.obj() == __(cache_id    = cache_id_4      ,
                                    cache_hash  = cache_hash_4    ,
                                    namespace   = 'test'          ,
                                    paths       = expected_paths_4,
                                    size        = 10              )

        assert result_4.paths['data'][0] == f"test/data/key-based/{cache_key}/{cache_id_4}.json"  # confirm the cache_key is used in the path

        result_5  = self.helpers.create_string_entry(cache_key=cache_key, strategy=strategy)
        result_6  = self.helpers.create_string_entry(cache_key=cache_key, strategy=strategy)

        assert result_4.cache_id   != result_5.cache_id             # cache Ids are different
        assert result_4.cache_id   != result_6.cache_id
        assert result_4.cache_hash != result_5.cache_hash           # and so are the hashes
        assert result_4.cache_hash != result_6.cache_hash




    def test__create_string_entry__with_file_id(self):          # Test creating string entry with file_id
        file_id = 'custom-file-identifier'
        result  = self.helpers.create_string_entry(file_id=file_id)
        assert type(result) is Schema__Cache__Store__Response

        cache_id    = result.cache_id
        cache_hash  = result.cache_hash

        data_paths = result.paths.get('data')                           # Verify file_id used in paths
        assert len(data_paths) == 3

        assert any(file_id in str(path) for path in data_paths)
        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = cache_id  ,
                                                               cache_hash = cache_hash,
                                                               file_id    = file_id   ))
        assert type(result) is Schema__Cache__Store__Response
        assert result.obj() == __(cache_id    = cache_id     ,
                                  cache_hash  = cache_hash    ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 10            )

    def test__create_string_entry__with_cache_key_and_file_id(self):        # Test creating string entry with both cache_key and file_id
        cache_key = 'test/path'
        file_id   = 'test-file-id'
        result    = self.helpers.create_string_entry(cache_key=cache_key,
                                                     file_id=file_id,
                                                     strategy=Enum__Cache__Store__Strategy.KEY_BASED)
        assert type(result) is Schema__Cache__Store__Response

        assert is_guid(result.cache_id)    is True

        # Both should be in paths
        data_paths = result.paths.get('data')
        assert any(cache_key in str(path) for path in data_paths)
        assert any(file_id   in str(path) for path in data_paths)
        assert len(data_paths) == 3

        cache_id   = result.cache_id
        cache_hash = result.cache_hash
        strategy = Enum__Cache__Store__Strategy.KEY_BASED
        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = cache_id   ,
                                                               cache_hash = cache_hash ,
                                                               cache_key  = cache_key  ,
                                                               file_id    = file_id    ,
                                                               strategy   = strategy))
        assert result.obj() == __(cache_id    = cache_id     ,
                                  cache_hash  = cache_hash    ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 10            )

    # ═════════════════════════════════════════════════════════════════════════════
    # JSON Entry Creation - Basic Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__create_json_entry__defaults(self):                         # Test creating JSON entry with defaults
        result = self.helpers.create_json_entry()
        assert type(result) is Schema__Cache__Store__Response

        assert is_guid(result.cache_id)    is True
        assert result.namespace            == 'test'
        assert result.size                 >  0

        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = result.cache_id   ,
                                                               cache_hash = result.cache_hash ))
        assert result.obj() == __(cache_id    = result.cache_id     ,
                                  cache_hash  = result.cache_hash   ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 44            )


    def test__create_json_entry__custom_data(self):     # Test creating JSON entry with custom data
        custom_data = {'key': 'value', 'number': 42, 'nested': {'inner': 'data'}}
        result      = self.helpers.create_json_entry(data=custom_data)
        assert type(result) is Schema__Cache__Store__Response

        cache_id  = result.cache_id                                             # Verify by retrieving
        namespace = result.namespace

        retrieved = self.client_cache_service.retrieve().retrieve__cache_id__json(cache_id  = cache_id  ,
                                                                                  namespace = namespace )

        assert retrieved                      == custom_data

    def test__create_json_entry__with_strategy(self):                   # Test creating JSON entry with specific strategy
        strategy = Enum__Cache__Store__Strategy.KEY_BASED
        result   = self.helpers.create_json_entry(strategy=strategy)
        assert type(result) is Schema__Cache__Store__Response
        assert is_guid(result.cache_id)    is True

        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = result.cache_id   ,
                                                               cache_hash = result.cache_hash ,
                                                               strategy   = strategy          ))
        assert result.obj() == __(cache_id    = result.cache_id     ,
                                  cache_hash  = result.cache_hash   ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 44            )


    def test__create_json_entry__with_cache_key(self):      # Test creating JSON entry with cache_key
        cache_key = 'configs/app/settings'
        result    = self.helpers.create_json_entry(cache_key=cache_key)
        assert type(result) is Schema__Cache__Store__Response

        assert is_guid(result.cache_id)    is True

        expected_paths = obj(self.helpers.build_expected_paths(cache_id   = result.cache_id   ,
                                                               cache_hash = result.cache_hash ,
                                                               cache_key  = cache_key         ))
        assert result.obj() == __(cache_id    = result.cache_id     ,
                                  cache_hash  = result.cache_hash   ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 44            )

    # ═════════════════════════════════════════════════════════════════════════════
    # Binary Entry Creation - Basic Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__bug__create_binary_entry__defaults(self):      # Test creating binary entry with defaults
        result = self.helpers.create_binary_entry()
        assert type(result) is Schema__Cache__Store__Response
        assert is_guid(result.cache_id)    is True
        assert result.namespace            == 'test'
        assert result.size                 ==  24

        expected_paths = obj(self.helpers.build_expected_paths(cache_id    = result.cache_id   ,
                                                               cache_hash  = result.cache_hash ,
                                                               extension   = 'bin'             ))
        assert result.obj() == __(cache_id    = result.cache_id     ,
                                  cache_hash  = result.cache_hash   ,
                                  namespace   = 'test'        ,
                                  paths       = expected_paths,
                                  size        = 24            )


    def test__create_binary_entry__custom_data(self):           # Test creating binary entry with custom data
        custom_data = b'custom binary content here'
        result      = self.helpers.create_binary_entry(data=custom_data)
        assert type(result) is Schema__Cache__Store__Response

        # Verify size matches
        assert result.size                 == len(custom_data)

        # Verify by retrieving
        cache_id  = result.cache_id
        namespace = result.namespace

        retrieved = self.client_cache_service.retrieve().retrieve__cache_id__binary(cache_id  = cache_id ,
                                                                                    namespace = namespace)

        assert type(retrieved)                is bytes
        assert retrieved                      == custom_data

    def test__create_binary_entry__large_data(self):                                # Test creating binary entry with large data"""
        large_data = b'x' * (1024 * 100)                                            # 100KB
        result     = self.helpers.create_binary_entry(data=large_data)

        assert result.size                 == 1024 * 100
        assert is_guid(result.cache_id)    is True

        # Verify by retrieving
        cache_id  = result.cache_id
        namespace = result.namespace

        retrieved = self.client_cache_service.retrieve().retrieve__cache_id__binary(cache_id  = cache_id ,
                                                                                    namespace = namespace)

        assert type(retrieved)                is bytes
        assert retrieved                      == large_data

    # ═════════════════════════════════════════════════════════════════════════════
    # Data File Addition - String Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__add_data_string__auto_generated_id(self):
        """Test adding string data file with auto-generated ID"""
        # Setup: Create main entry
        namespace    = 'test-helpers-add-string'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id

        # Action: Add data file
        custom_data  = 'test_data_content'
        data_result  = self.helpers.add_data_string(cache_id  = cache_id     ,
                                                    namespace = namespace    ,
                                                    data      = custom_data  )

        # Verify result structure
        assert type(data_result)            is Schema__Cache__Data__Store__Response
        assert data_result.cache_id         == cache_id
        assert data_result.namespace        == namespace
        assert data_result.data_type        == 'string'
        assert data_result.extension        == 'txt'
        assert is_guid(data_result.file_id) is True
        assert data_result.file_size        >  0

    def test__add_data_string__custom_file_id(self):            # Test adding string data file with custom file_id
        # Setup
        namespace      = 'test-helpers-add-string-id'
        data_file_id   = 'my-custom-data-id'                                              # Action: Add with custom ID
        extension      = 'txt'

        main_entry     = self.helpers.create_string_entry(namespace=namespace)                      # create main file
        cache_id       = main_entry.cache_id
        cache_hash     = main_entry.cache_hash
        expected_paths = obj(self.helpers.build_expected_paths(cache_id    = cache_id   ,
                                                               cache_hash  = cache_hash ,
                                                               namespace   = namespace  ))


        data_result  = self.helpers.add_data_string(cache_id     = cache_id     ,                   # create text file inside main file
                                                    namespace    = namespace    ,
                                                    data_file_id = data_file_id )


        assert data_result.file_id == data_file_id                                                  # Verify custom ID used
        assert type(main_entry )   is Schema__Cache__Store__Response
        assert type(data_result)   is Schema__Cache__Data__Store__Response

        assert main_entry.obj()    == __(cache_id    = cache_id      ,
                                         cache_hash  = cache_hash    ,
                                         namespace   = namespace     ,
                                         paths       = expected_paths,
                                         size        = 10            )
        assert data_result.obj()   == __(cache_id           = cache_id,
                                         data_files_created = [f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_file_id}.{extension}'],
                                         data_key           = ''                          ,
                                         data_type          = 'string'                    ,
                                         extension          = extension                       ,
                                         file_id            = 'my-custom-data-id'         ,
                                         file_size          = 8                           ,
                                         namespace          = 'test-helpers-add-string-id',
                                         timestamp          = __SKIP__                    )

    def test__add_data_string__with_key_and_id(self):           # Test adding string data file with data_key and file_id
        # Setup
        namespace    = 'test-helpers-add-string-key'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id

        # Action: Add with key and ID
        data_key           = 'logs/application'
        data_file_id       = 'app-log-001'
        extension          = 'txt'
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_key}/{data_file_id}.{extension}'
        data_result        = self.helpers.add_data_string(cache_id     = cache_id     ,
                                                          namespace    = namespace    ,
                                                          data_key     = data_key     ,
                                                          data_file_id = data_file_id )

        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response

        # Verify structure
        assert data_result.data_key        == data_key
        assert data_result.file_id         == data_file_id

        assert data_result.obj()   == __(cache_id           = cache_id            ,
                                         data_files_created = [expected_data_file],
                                         data_key           = data_key            ,
                                         data_type          = 'string'            ,
                                         extension          = extension           ,
                                         file_id            = data_file_id        ,
                                         file_size          = 8                   ,
                                         namespace          = namespace           ,
                                         timestamp          = __SKIP__            )

    # ═════════════════════════════════════════════════════════════════════════════
    # Data File Addition - JSON Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__add_data_json__auto_generated_id(self):                                   # Test adding JSON data file with auto-generated ID
        # Setup
        namespace   = 'test-helpers-add-json'
        main_entry  = self.helpers.create_string_entry(namespace=namespace)
        cache_id    = main_entry.cache_id

        # Action
        custom_data        = {'test': 'data', 'value': 123}
        extension          = 'json'
        data_result        = self.helpers.add_data_json(cache_id  = cache_id     ,
                                                        namespace = namespace    ,
                                                        data      = custom_data  )

        file_id             = data_result.file_id
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{file_id}.{extension}'


        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response



        # Verify
        assert data_result.data_type       == extension
        assert data_result.extension       == extension
        assert is_guid(data_result.file_id) is True

        assert data_result.obj()   == __(cache_id           = cache_id            ,
                                         data_files_created = [expected_data_file],
                                         data_key           = ''                  ,
                                         data_type          = extension           ,
                                         extension          = extension           ,
                                         file_id            = file_id             ,
                                         file_size          = 40                  ,
                                         namespace          = namespace           ,
                                         timestamp          = __SKIP__            )

    def test__add_data_json__custom_file_id(self):                      # Test adding JSON data file with custom file_id
        # Setup
        namespace    = 'test-helpers-add-json-id'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id

        # Action
        data_file_id       = 'config-data'
        extension          = "json"
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_file_id}.{extension}'
        data_result        = self.helpers.add_data_json(cache_id     = cache_id     ,
                                                        namespace    = namespace    ,
                                                        data_file_id = data_file_id )

        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response


        # Verify
        assert data_result.file_id         == data_file_id
        assert data_result.obj()   == __(cache_id           = cache_id            ,
                                         data_files_created = [expected_data_file],
                                         data_key           = ''                  ,
                                         data_type          = extension           ,
                                         extension          = extension           ,
                                         file_id            = data_file_id        ,
                                         file_size          = 49                  ,
                                         namespace          = namespace           ,
                                         timestamp          = __SKIP__            )


    def test__add_data_json__with_key_and_id(self):                             # Test adding JSON data file with key and ID
        # Setup
        namespace    = 'test-helpers-add-json-key'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id

        # Action
        data_key           = 'configs/database'
        data_file_id       = 'prod-config'
        extension          = "json"
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_key}/{data_file_id}.{extension}'

        data_result  = self.helpers.add_data_json(cache_id     = cache_id     ,
                                                  namespace    = namespace    ,
                                                  data_key     = data_key     ,
                                                  data_file_id = data_file_id )

        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response


        # Verify
        assert data_result.data_key        == data_key
        assert data_result.file_id         == data_file_id
        assert data_result.obj()           == __(cache_id           = cache_id            ,
                                                 data_files_created = [expected_data_file],
                                                 data_key           = data_key            ,
                                                 data_type          = extension           ,
                                                 extension          = extension           ,
                                                 file_id            = data_file_id        ,
                                                 file_size          = 49                  ,
                                                 namespace          = namespace           ,
                                                 timestamp          = __SKIP__            )

    # ═════════════════════════════════════════════════════════════════════════════
    # Data File Addition - Binary Tests
    # ═════════════════════════════════════════════════════════════════════════════

    def test__add_data_binary__auto_generated_id(self):                 # Test adding binary data file with auto-generated ID
        # Setup
        namespace   = 'test-helpers-add-binary'
        main_entry  = self.helpers.create_string_entry(namespace=namespace)
        cache_id    = main_entry.cache_id

        # Action
        custom_data        = b'binary test content'
        data_type          = 'binary'
        extension          = 'bin'
        data_result        = self.helpers.add_data_binary(cache_id  = cache_id     ,
                                                          namespace = namespace    ,
                                                          data      = custom_data  )
        data_file_id       = data_result.file_id
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_file_id}.{extension}'

        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response


        # Verify

        assert data_result.data_type        == data_type
        assert data_result.extension        == extension
        assert data_result.file_size        == len(custom_data)
        assert is_guid(data_result.file_id) is True
        assert data_result.obj()            == __(cache_id           = cache_id            ,
                                                  data_files_created = [expected_data_file],
                                                  data_key           = ''                  ,
                                                  data_type          = data_type           ,
                                                  extension          = extension           ,
                                                  file_id            = data_file_id        ,
                                                  file_size          = 19                  ,
                                                  namespace          = namespace           ,
                                                  timestamp          = __SKIP__            )


    def test__add_data_binary__custom_file_id(self):                    # Test adding binary data file with custom file_id
        # Setup
        namespace    = 'test-helpers-add-binary-id'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id
        data_type    = 'binary'
        extension    = 'bin'

        # Action
        data_file_id       = 'binary-image'
        data_result        = self.helpers.add_data_binary(cache_id     = cache_id     ,
                                                          namespace    = namespace    ,
                                                          data_file_id = data_file_id )
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_file_id}.{extension}'

        assert type(main_entry )   is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)   is Schema__Cache__Data__Store__Response

        # Verify
        assert data_result.file_id == data_file_id
        assert data_result.obj()   == __(cache_id           = cache_id            ,
                                         data_files_created = [expected_data_file],
                                         data_key           = ''                  ,
                                         data_type          = data_type           ,
                                         extension          = extension           ,
                                         file_id            = data_file_id        ,
                                         file_size          = 24                  ,
                                         namespace          = namespace           ,
                                         timestamp          = __SKIP__            )



    def test__add_data_binary__with_key_and_id(self):                           # Test adding binary data file with key and ID
        # Setup
        namespace    = 'test-helpers-add-binary-key'
        main_entry   = self.helpers.create_string_entry(namespace=namespace)
        cache_id     = main_entry.cache_id

        # Action
        data_key     = 'images/thumbnails'
        data_file_id = 'thumb-001'
        data_type    = 'binary'
        extension    = 'bin'
        expected_data_file = f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{data_key}/{data_file_id}.{extension}'

        data_result  = self.helpers.add_data_binary(cache_id     = cache_id     ,
                                                    namespace    = namespace    ,
                                                    data_key     = data_key     ,
                                                    data_file_id = data_file_id )

        assert type(main_entry )    is Schema__Cache__Store__Response                    # confirm return types
        assert type(data_result)    is Schema__Cache__Data__Store__Response

        # Verify
        assert data_result.data_key == data_key
        assert data_result.file_id  == data_file_id

        assert data_result.obj()   == __(cache_id           = cache_id            ,
                                         data_files_created = [expected_data_file],
                                         data_key           = data_key            ,
                                         data_type          = data_type           ,
                                         extension          = extension           ,
                                         file_id            = data_file_id        ,
                                         file_size          = 24                  ,
                                         namespace          = namespace           ,
                                         timestamp          = __SKIP__            )


    # ═════════════════════════════════════════════════════════════════════════════
    # Complex Scenario: create_entry_with_data_files
    # ═════════════════════════════════════════════════════════════════════════════

    def test__create_entry_with_data_files__default_counts(self):       # Test creating entry with default data file counts
        namespace = 'test-helpers-with-data'

        # Action: Create entry with data files (default: 2 string, 2 json, 1 binary)
        cache_id, store_result, files__in_cache_id = self.helpers.create_entry_with_data_files(namespace=namespace)


        # Verify main entry
        assert is_guid(cache_id)           is True
        assert store_result.cache_id       == cache_id
        assert store_result.namespace      == namespace
        assert cache_id                    is not None

        assert len(files__in_cache_id) == 8                                                                          # 3x default + 2x string, 2x json, 1x binary
        assert files__in_cache_id      == [ f'{cache_id}.json',
                                            f'{cache_id}.json.config',
                                            f'{cache_id}.json.metadata',
                                            f'{cache_id}/data/binary-data-0.bin',
                                            f'{cache_id}/data/json-data-0.json' ,
                                            f'{cache_id}/data/json-data-1.json',
                                            f'{cache_id}/data/string-data-0.txt',
                                            f'{cache_id}/data/string-data-1.txt']


    def test__create_entry_with_data_files__custom_counts(self):        # Test creating entry with custom data file counts
        namespace = 'test-helpers-with-data-custom'

        # Action: Custom counts
        cache_id, store_result, files__in_cache_id = self.helpers.create_entry_with_data_files(namespace    = namespace ,
                                                                                               string_count = 5        ,
                                                                                               json_count   = 3        ,
                                                                                               binary_count = 2        )

        # Verify entry created
        assert is_guid(cache_id)           is True
        assert store_result.namespace      == namespace
        assert len(files__in_cache_id)     == 13
        assert files__in_cache_id          == [  f'{cache_id}.json',
                                                 f'{cache_id}.json.config',
                                                 f'{cache_id}.json.metadata',
                                                 f'{cache_id}/data/binary-data-0.bin',          # binary_count = 2
                                                 f'{cache_id}/data/binary-data-1.bin',
                                                 f'{cache_id}/data/json-data-0.json',           # json_count   = 3
                                                 f'{cache_id}/data/json-data-1.json',
                                                 f'{cache_id}/data/json-data-2.json',
                                                 f'{cache_id}/data/string-data-0.txt',          # string_count = 5
                                                 f'{cache_id}/data/string-data-1.txt',
                                                 f'{cache_id}/data/string-data-2.txt',
                                                 f'{cache_id}/data/string-data-3.txt',
                                                 f'{cache_id}/data/string-data-4.txt']

    def test__create_entry_with_data_files__with_keys(self):    # Test creating entry with data files using key paths
        namespace = 'test-helpers-with-data-keys'

        # Action: Use data keys
        cache_id, store_result, files__in_cache_id = self.helpers.create_entry_with_data_files( namespace     = namespace ,
                                                                                                string_count  = 2         ,
                                                                                                json_count    = 1         ,
                                                                                                binary_count  = 1         ,
                                                                                                use_data_keys = True      )

        # Verify entry created
        assert is_guid(cache_id)           is True
        assert store_result.namespace      == namespace
        assert len(files__in_cache_id)     == 7
        assert files__in_cache_id          == [ f'{cache_id}.json',
                                                f'{cache_id}.json.config',
                                                f'{cache_id}.json.metadata',
                                                f'{cache_id}/data/binaries/data-0/binary-data-0.bin',
                                                f'{cache_id}/data/jsons/data-0/json-data-0.json'    ,
                                                f'{cache_id}/data/strings/data-0/string-data-0.txt' ,
                                                f'{cache_id}/data/strings/data-1/string-data-1.txt' ]

    def test__create_entry_with_data_files__zero_counts(self):
        """Test creating entry with zero data files"""
        namespace = 'test-helpers-with-data-zero'

        # Action: No data files, just main entry
        cache_id, store_result,files__in_cache_id = self.helpers.create_entry_with_data_files(namespace    = namespace ,
                                                                                              string_count = 0        ,
                                                                                              json_count   = 0        ,
                                                                                              binary_count = 0        )

        # Verify only main entry created
        assert is_guid(cache_id)       is True
        assert store_result.namespace  == namespace
        assert len(files__in_cache_id) == 3
        assert files__in_cache_id      == [ f'{cache_id}.json',
                                            f'{cache_id}.json.config',
                                            f'{cache_id}.json.metadata']

    # ═════════════════════════════════════════════════════════════════════════════
    # Verification Methods
    # ═════════════════════════════════════════════════════════════════════════════

    def test__verify_entry_exists__existing_entry(self):    # Test verifying an existing entry"""
        # Setup: Create entry
        namespace = 'test-helpers-verify-exists'
        result    = self.helpers.create_string_entry(namespace=namespace)
        cache_id  = result.cache_id

        # Action: Verify exists
        exists = self.helpers.verify_entry_exists(cache_id  = cache_id  ,
                                                  namespace = namespace )

        # Verify
        assert exists is True

    def test__verify_entry_exists__non_existent_entry(self):    # Test verifying a non-existent entry
        # Action: Check non-existent GUID
        fake_cache_id = '00000000-0000-0000-0000-000000000000'
        exists        = self.helpers.verify_entry_exists(cache_id  = fake_cache_id ,
                                                         namespace = 'test'        )

        # Verify
        assert exists is False

    def test__verify_entry_exists_by_hash__existing(self):      # Test verifying entry by hash - existing
        # Setup: Create entry
        namespace  = 'test-helpers-verify-hash'
        result     = self.helpers.create_string_entry(namespace=namespace, value='test_value')
        cache_hash = result.cache_hash

        # Action: Verify by hash
        exists = self.helpers.verify_entry_exists_by_hash(cache_hash = cache_hash ,
                                                         namespace  = namespace  )

        # Verify
        assert exists is True

    def test__verify_entry_exists_by_hash__non_existent(self):          # Test verifying entry by hash - non-existent
        # Action: Check fake hash
        fake_hash = '0000000000'
        exists    = self.helpers.verify_entry_exists_by_hash(cache_hash = fake_hash ,
                                                            namespace  = 'test'     )

        # Verify
        assert exists                         is False

    def test__verify_data_file_exists__existing(self):      # Test verifying data file exists - existing
        # Setup: Create entry with data file
        namespace        = 'test-helpers-verify-data-exists'
        cache_id, _, _   = self.helpers.create_entry_with_data_files(namespace    = namespace,
                                                                    string_count = 1       )
        expected_file_id = 'string-data-0'

        # Action: Verify data file exists
        exists = self.helpers.verify_data_file_exists(cache_id     = cache_id         ,
                                                      data_file_id = expected_file_id ,
                                                      namespace    = namespace        )

        # Verify
        assert exists is True

    def test__verify_data_file_exists__non_existent(self):      # Test verifying data file exists - non-existent
        namespace = 'test-helpers-verify-data-not-exists'       # Setup: Create entry WITHOUT data files
        result    = self.helpers.create_string_entry(namespace=namespace)
        cache_id  = result.cache_id

        # Action: Check for non-existent data file
        exists = self.helpers.verify_data_file_exists(cache_id     = cache_id         ,
                                                     data_file_id = 'non-existent' ,
                                                     namespace    = namespace      )

        # Verify
        assert exists                         is False

    def test__get_all_namespaces__after_creating_entries(self):     # Test getting all namespaces after creating entries
        # Setup: Create entries in unique namespaces
        ns1 = 'test-helpers-ns-list-1'
        ns2 = 'test-helpers-ns-list-2'
        ns3 = 'test-helpers-ns-list-3'

        self.helpers.create_string_entry(namespace=ns1)
        self.helpers.create_string_entry(namespace=ns2)
        self.helpers.create_string_entry(namespace=ns3)

        # Action: Get all namespaces
        namespaces = self.helpers.get_all_namespaces()

        # Verify: Our namespaces are in the list
        assert type(namespaces)               is list
        assert ns1                            in namespaces
        assert ns2                            in namespaces
        assert ns3                            in namespaces

    # ═════════════════════════════════════════════════════════════════════════════
    # Complex Scenario Builders
    # ═════════════════════════════════════════════════════════════════════════════

    def test__create_multi_strategy_entries__all_strategies(self):      # Test creating entries with all storage strategies
        namespace = 'test-helpers-multi-strategy'

        # Action: Create entries with all strategies
        results = self.helpers.create_multi_strategy_entries(namespace=namespace)

        # Verify: All strategies created
        expected_strategies = ['direct', 'temporal', 'temporal_latest', 'temporal_versioned', 'key_based']
        assert type(results)   is dict
        assert len(results)    == 5

        for strategy in expected_strategies:
            assert strategy                            in results
            assert is_guid(results[strategy].cache_id) is True
            assert results[strategy].namespace         == namespace

    def test__create_versioned_entries__default_count(self):        # Test creating versioned entries with default count
        namespace = 'test-helpers-versioned'
        cache_key = 'test/versioned/key'

        # Action: Create 3 versions (default)
        results = self.helpers.create_versioned_entries(namespace = namespace ,
                                                       cache_key = cache_key )

        # Verify: 3 versions created
        assert type(results) is list
        assert len(results)  == 3

        for i, result in enumerate(results):
            assert is_guid(result.cache_id) is True
            assert result.namespace         == namespace

    def test__create_versioned_entries__custom_count(self):
        """Test creating versioned entries with custom count"""
        namespace     = 'test-helpers-versioned-custom'
        cache_key     = 'test/versioned/key'
        version_count = 5

        # Action: Create 5 versions
        results = self.helpers.create_versioned_entries(namespace     = namespace     ,
                                                       cache_key     = cache_key     ,
                                                       version_count = version_count )

        # Verify: 5 versions created
        assert len(results)                   == 5

    def test__create_namespace_hierarchy__default_depth(self):      # Test creating namespace hierarchy with default depth
        base_namespace = 'test-helpers-hierarchy'

        # Action: Create hierarchy (default: depth=3, 2 entries per level)
        results = self.helpers.create_namespace_hierarchy(base_namespace=base_namespace)

        # Verify: 3 namespaces created
        assert type(results)                  is dict
        assert len(results)                   == 3

        # Verify structure
        assert base_namespace                 in results
        assert f"{base_namespace}-level1"     in results
        assert f"{base_namespace}-level2"     in results

        # Verify entries per namespace
        for namespace, entries in results.items():
            assert type(entries)              is list
            assert len(entries)               == 2                              # Default entries_per_ns

    def test__create_namespace_hierarchy__custom_params(self):      # Test creating namespace hierarchy with custom parameters
        base_namespace  = 'test-helpers-hierarchy-custom'
        depth           = 4
        entries_per_ns  = 3

        # Action: Custom hierarchy
        results = self.helpers.create_namespace_hierarchy(base_namespace = base_namespace  ,
                                                         depth          = depth           ,
                                                         entries_per_ns = entries_per_ns  )

        # Verify: 4 namespaces created
        assert len(results)                   == 4

        # Verify entries count
        for namespace, entries in results.items():
            assert len(entries)               == 3

    # ═════════════════════════════════════════════════════════════════════════════
    # Cleanup Operations
    # ═════════════════════════════════════════════════════════════════════════════

    def test__delete_entry__successful(self):       # Test deleting an entry
        namespace = 'test-helpers-delete'
        result    = self.helpers.create_string_entry(namespace=namespace)               # Setup: Create entry
        cache_id  = result.cache_id

        exists_before = self.helpers.verify_entry_exists(cache_id  = cache_id  ,        # Verify exists before deletion
                                                         namespace = namespace )

        delete_result = self.helpers.delete_entry(cache_id  = cache_id  ,               # Action: Delete
                                                  namespace = namespace )

        assert exists_before                  is True
        assert type(delete_result)            is dict
        assert 'deleted_count'                in delete_result                          # Verify deletion result
        assert obj(delete_result)             == __(status='success',
                                                    cache_id=cache_id,
                                                    deleted_count=5,
                                                    failed_count=0,
                                                    deleted_paths=__SKIP__,
                                                    failed_paths=[])


        exists_after = self.helpers.verify_entry_exists(cache_id  = cache_id  ,         # Verify no longer exists
                                                       namespace = namespace )
        assert exists_after                   is False

    def test__delete_all_data_files__successful(self):  # Test deleting all data files from entry
        # Setup: Create entry with data files
        namespace        = 'test-helpers-delete-data'
        cache_id, _,_      = self.helpers.create_entry_with_data_files(namespace    = namespace,
                                                                       string_count = 2       ,
                                                                       json_count   = 1       )

        # Action: Delete all data files
        delete_result = self.helpers.delete_all_data_files(cache_id  = cache_id  ,
                                                          namespace = namespace )

        # Verify deletion
        assert type(delete_result)            is dict
        assert 'deleted_count'                in delete_result
        assert delete_result['deleted_count'] == 4                              # At least 3 files deleted
        assert obj(delete_result)             == __(status        = 'success',
                                                    message       = 'Deleted 4 data files',
                                                    cache_id      = cache_id,
                                                    deleted_count = 4,
                                                    deleted_files = [f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/string-data-0.txt',
                                                                     f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/string-data-1.txt',
                                                                     f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/json-data-0.json',
                                                                     f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/binary-data-0.bin'],
                                                    data_key      = None,
                                                    namespace     = 'test-helpers-delete-data' )


    # ═════════════════════════════════════════════════════════════════════════════
    # Edge Cases and Error Scenarios
    # ═════════════════════════════════════════════════════════════════════════════

    def test__bug__create_string_entry__empty_value(self):       # Test creating entry with empty string value
        result = self.helpers.create_string_entry(value='')

        assert is_guid(result.cache_id)    is True                  # todo: BUG: review this since this should be a bug (i.e. we shouldn't return a GUID if there is no file created)
        assert __(cache_id=result.cache_id,
                  cache_hash='',
                  namespace='',
                  paths=__(),
                  size=0)

    def test__bug__create_json_entry__empty_dict(self):             # Test creating entry with empty JSON dict
        result = self.helpers.create_json_entry(data={})

        assert is_guid(result.cache_id)    is True
        assert __(cache_id=result.cache_id,                         # todo: BUG: review this since this should be a bug (i.e. we shouldn't return a GUID if there is no file created)
                  cache_hash='',
                  namespace='',
                  paths=__(),
                  size=0)

    def test__bug__create_binary_entry__empty_bytes(self):               # Test creating entry with empty bytes
        result = self.helpers.create_binary_entry(data=b'')

        assert is_guid(result.cache_id)    is True
        assert __(cache_id=result.cache_id,                         # todo: BUG: review this since this should be a bug (i.e. we shouldn't return a GUID if there is no file created)
                  cache_hash='',
                  namespace='',
                  paths=__(),
                  size=0)

    def test__add_data_string__none_value_uses_default(self):       # Test that None data value uses auto-generated default
        # Setup
        namespace  = 'test-helpers-add-none'
        main_entry = self.helpers.create_string_entry(namespace=namespace)
        cache_id   = main_entry.cache_id

        # Action: Add with data=None (should use default)
        data_result = self.helpers.add_data_string(cache_id  = cache_id  ,
                                                   namespace = namespace ,
                                                   data      = None      )

        # Verify: Default random data was generated
        assert data_result.file_size               ==  8
        assert is_guid(data_result.file_id)        is True
        assert len(data_result.data_files_created) == 1


    def test__verify_methods__with_invalid_namespace(self):     # Test verification methods with invalid namespace
        # Action: Verify in non-existent namespace
        fake_cache_id = '00000000-0000-0000-0000-000000000000'
        exists        = self.helpers.verify_entry_exists(cache_id  = fake_cache_id     ,
                                                         namespace = 'non-existent-ns' )

        # Verify: Returns False (not error)
        assert exists  is False

    # ═════════════════════════════════════════════════════════════════════════════
    # Integration: Multiple Helpers Working Together
    # ═════════════════════════════════════════════════════════════════════════════

    def test__integration__create_verify_delete_workflow(self): # Test complete workflow using multiple helper methods
        # Step 1: Create entry
        namespace = 'test-helpers-integration'
        result    = self.helpers.create_string_entry(namespace=namespace, value='test_data')
        cache_id  = result.cache_id

        # Step 2: Verify exists
        exists = self.helpers.verify_entry_exists(cache_id  = cache_id  ,
                                                 namespace = namespace )
        assert exists is True

        # Step 3: Add data files
        cache_id2, _, _ = self.helpers.create_entry_with_data_files(namespace    = namespace,
                                                                    string_count = 2       )

        # Step 4: Verify data files exist
        data_exists = self.helpers.verify_data_file_exists(cache_id     = cache_id2      ,
                                                          data_file_id = 'string-data-0',
                                                          namespace    = namespace      )
        assert data_exists is True

        # Step 5: Delete all data files
        self.helpers.delete_all_data_files(cache_id  = cache_id2 ,
                                           namespace = namespace )

        # Step 6: Verify data files deleted
        data_exists_after = self.helpers.verify_data_file_exists(cache_id     = cache_id2      ,
                                                                 data_file_id = 'string-data-0',
                                                                 namespace    = namespace      )
        assert data_exists_after is False

        # Step 7: Delete main entries
        self.helpers.delete_entry(cache_id  = cache_id  ,
                                 namespace = namespace )
        self.helpers.delete_entry(cache_id  = cache_id2 ,
                                 namespace = namespace )

    def test__integration__multi_strategy_and_verification(self):           # Test creating multi-strategy entries and verifying each
        namespace = 'test-helpers-integration-multi'

        # Step 1: Create entries with all strategies
        results = self.helpers.create_multi_strategy_entries(namespace=namespace)

        # Step 2: Verify each entry exists
        for strategy, result in results.items():
            cache_id = result.cache_id
            exists   = self.helpers.verify_entry_exists(cache_id  = cache_id  ,
                                                       namespace = namespace )
            assert exists is True, f"Entry with {strategy} strategy should exist"

        # Step 3: Verify namespace is in global list
        all_namespaces = self.helpers.get_all_namespaces()
        assert namespace in all_namespaces

    def test__integration__versioned_entries_and_retrieval(self):   # Test creating versioned entries and verifying all versions
        namespace     = 'test-helpers-integration-versioned'
        cache_key     = 'test/versioned/data'
        version_count = 4

        # Step 1: Create versions
        results = self.helpers.create_versioned_entries(namespace     = namespace     ,
                                                       cache_key     = cache_key     ,
                                                       version_count = version_count )

        # Step 2: Verify each version exists
        for i, result in enumerate(results):
            cache_id = result.cache_id
            exists   = self.helpers.verify_entry_exists(cache_id  = cache_id  ,
                                                       namespace = namespace )
            assert exists is True, f"Version {i} should exist"

        # Step 3: Verify all have different cache_ids
        cache_ids = [r.cache_id for r in results]
        assert len(set(cache_ids))  == version_count                  # All unique