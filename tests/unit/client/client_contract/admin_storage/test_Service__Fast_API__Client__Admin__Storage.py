from unittest                                                                                                       import TestCase
from osbot_utils.helpers.duration.decorators.capture_duration                                                       import capture_duration
from osbot_utils.testing.__                                                                                         import __, __SKIP__
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                                import Serverless__Fast_API__Config
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                                       import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client                         import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config                 import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.client_contract.admin_storage.Service__Fast_API__Client__Admin__Storage  import Service__Fast_API__Client__Admin__Storage
from mgraph_ai_service_cache_client.client.requests.Cache__Service__Fast_API__Client__Requests                      import Cache__Service__Fast_API__Client__Requests
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                                import Enum__Client__Mode
from mgraph_ai_service_cache_client.schemas.routes.admin.Schema__Routes__Admin__Storage__Files_All__Response        import Schema__Routes__Admin__Storage__Files_All__Response


class test_Service__Fast_API__Client__Admin__Storage(TestCase):                   # Test suite for admin storage operations using in-memory FastAPI client

    @classmethod
    def setUpClass(cls) -> None:                                                 # Setup in-memory FastAPI client for testing
        with capture_duration() as duration:
            cls.serverless_config       = Serverless__Fast_API__Config       (enable_api_key = False                            )
            cls.cache_service__fast_api = Cache_Service__Fast_API            (config         = cls.serverless_config            ).setup()
            cls.server_config           = Cache__Service__Fast_API__Client__Config  ()
            cls.requests                = Cache__Service__Fast_API__Client__Requests(config         = cls.server_config                ,
                                                                                     _app           = cls.cache_service__fast_api.app())
            cls.fast_api_client         = Cache__Service__Fast_API__Client          (config         = cls.server_config,
                                                                                     _requests      = cls.requests)
            cls.admin_storage          = cls.fast_api_client.admin_storage()
            cls.cache_service          = cls.cache_service__fast_api.cache_service
        # if not_in_github_action():
        #     assert duration.seconds < 0.5

    def test__setup(self):                                                        # Verify test setup is correct
        assert self.requests.mode         == Enum__Client__Mode.IN_MEMORY
        assert self.requests._test_client is not None
        assert self.requests._app         is not None
        assert type(self.fast_api_client) is Cache__Service__Fast_API__Client
        assert type(self.admin_storage)   is Service__Fast_API__Client__Admin__Storage
        assert self.admin_storage._client is self.fast_api_client

        #assert self.fast_api_client.obj() == __()                               # todo: wire up this .obj() test (since the object is quite big and some of it we don't need to test, and most likely will cause issues in GH actions)

    def test__init__(self):                                                       # Test Service__Fast_API__Client__Admin__Storage initialization
        with self.admin_storage as _:
            assert type(_)          is Service__Fast_API__Client__Admin__Storage
            assert type(_._client)  is Cache__Service__Fast_API__Client
            assert type(_.requests) is Cache__Service__Fast_API__Client__Requests
            assert _.requests       is self.requests

    def test__bucket_name(self):                                                  # Test retrieving bucket name
        result = self.admin_storage.bucket_name()
        assert type(result)                is dict
        assert 'bucket-name'               in result
        assert type(result['bucket-name']) is str
        assert result['bucket-name']       in ['mgraph-ai-cache', 'NA']
        assert result                      == {'bucket-name': 'NA'}

    def test__file__exists__with_nonexistent_file(self):                          # Test checking existence of non-existent file
        test_path = 'nonexistent/path/to/file.json'
        result    = self.admin_storage.file__exists(test_path)
        assert type(result)      is dict
        assert 'exists'         in result
        assert 'path'           in result
        assert result['exists'] is False
        assert result['path']   == test_path
        assert result           == {'exists': False, 'path': 'nonexistent/path/to/file.json'}

    def test__file__exists__with_existing_file(self):                             # Test checking existence of file that exists
        test_data     = {"test": "data", "number": 42}
        namespace     = "test-admin-storage"
        cache_hash    = self.cache_service.hash_from_json(test_data)
        store_result  = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        cache_id      = store_result.cache_id
        content_files = store_result.paths.get('data', [])
        expected_path = f'test-admin-storage/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json'
        file_path     = content_files[0]
        result        = self.admin_storage.file__exists(file_path)

        assert len(content_files) > 0
        assert type(result)      is dict
        assert result['exists']  is True
        assert result['path']    == file_path
        assert result            == { 'exists': True         ,
                                      'path'  : expected_path}

    def test__file__bytes__with_existing_file(self):                              # Test retrieving file content as bytes
        test_data  = {"key": "value", "items": [1, 2, 3]}
        namespace  = "test-admin-bytes"
        cache_hash = self.cache_service.hash_from_json(test_data)
        store_result = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        file_path = store_result.paths['data'][0]
        result    = self.admin_storage.file__bytes(file_path)
        assert type(result) is bytes
        assert len(result)   > 0
        assert result       == b'{\n  "key": "value",\n  "items": [\n    1,\n    2,\n    3\n  ]\n}'

    def test__file__json__with_existing_file(self):                               # Test retrieving file content as JSON
        test_data    = {"message": "hello", "count": 100, "active": True}
        namespace    = "test-admin-json"
        cache_hash   = self.cache_service.hash_from_json(test_data)
        store_result = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        file_path    = store_result.paths['data'][0]
        result       = self.admin_storage.file__json(file_path)
        assert type(result) is dict
        assert result       == test_data

    def test__file__json__with_nonexistent_file(self):                            # Test retrieving non-existent file as JSON returns 404
        test_path = 'nonexistent/file.json'
        result    = self.admin_storage.file__json(test_path)
        assert type(result)         is dict
        assert 'error_type'         in result
        assert result['error_type'] == 'FILE_NOT_FOUND'
        assert 'path'               in result
        assert result['path']       == test_path

    def test__files__in__path__default_params(self):                           # Test listing files in parent path with default parameters
        namespace = "test-files-in-path__default-params"
        for i in range(3):
            test_data  = {"index": i, "value": f"test-{i}"}
            cache_hash = self.cache_service.hash_from_json(test_data)
            self.cache_service.store_with_strategy(storage_data = test_data ,           # these 3 files will always have the same hash
                                                   cache_hash   = cache_hash ,
                                                   strategy     = "direct"   ,
                                                   namespace    = namespace  )
        path = f'{namespace}/refs/by-hash/25/f2'
        result = self.admin_storage.files__in__path(path=path)
        assert type(result) is list
        assert len(result) > 0
        assert result == ['25f249f06786c7cf.json'        ,
                          '25f249f06786c7cf.json.config' ,
                          '25f249f06786c7cf.json.metadata']

        result_2 = self.admin_storage.files__in__path(path=path, return_full_path=True )
        assert result_2 == [f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json'        ,
                            f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json.config' ,
                            f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json.metadata']

        path_3   = f'{namespace}/refs/by-hash/'
        result_3 = self.admin_storage.files__in__path(path=path_3, recursive=True )
        assert result_3 == [ f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json',
                             f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json.config',
                             f'{namespace}/refs/by-hash/25/f2/25f249f06786c7cf.json.metadata',
                             f'{namespace}/refs/by-hash/3d/69/3d693601f5fab122.json',
                             f'{namespace}/refs/by-hash/3d/69/3d693601f5fab122.json.config',
                             f'{namespace}/refs/by-hash/3d/69/3d693601f5fab122.json.metadata',
                             f'{namespace}/refs/by-hash/c0/ff/c0ff7685548acfd2.json',
                             f'{namespace}/refs/by-hash/c0/ff/c0ff7685548acfd2.json.config',
                             f'{namespace}/refs/by-hash/c0/ff/c0ff7685548acfd2.json.metadata']

        result__folders__1 = self.admin_storage.folders()
        assert namespace in result__folders__1

        result__folders__2 = self.admin_storage.folders(return_full_path=True)
        assert namespace in result__folders__2

        result__folders__3 = self.admin_storage.folders(return_full_path=False, path=namespace+'/refs/by-hash/')
        assert result__folders__3 == ['25', '3d', 'c0']

        result__folders__3 = self.admin_storage.folders(return_full_path=True , path=namespace+'/refs/by-hash/')
        assert result__folders__3 == [f'{namespace}/refs/by-hash/25',
                                      f'{namespace}/refs/by-hash/3d',
                                      f'{namespace}/refs/by-hash/c0']

        result__folders__4 = self.admin_storage.folders(recursive=True, return_full_path=True, path=namespace+'/refs/by-hash/')
        assert result__folders__4 ==[ f'{namespace}/refs/by-hash/25',
                                      f'{namespace}/refs/by-hash/25/f2',
                                      f'{namespace}/refs/by-hash/3d',
                                      f'{namespace}/refs/by-hash/3d/69',
                                      f'{namespace}/refs/by-hash/c0',
                                      f'{namespace}/refs/by-hash/c0/ff']

        result__folders__5 = self.admin_storage.folders(recursive=True, return_full_path=False,  path=namespace+'/refs/by-hash')
        assert result__folders__5 == ['25'   ,
                                      '25/f2',
                                      '3d'   ,
                                      '3d/69',
                                      'c0'   ,
                                      'c0/ff']


    def test__files__all__path__recursive_listing(self):                         # Test getting all files recursively under a path
        namespace   = "test-admin-recursive"
        test_data    = {"index": 1}
        cache_hash   = self.cache_service.hash_from_json(test_data)
        store_result = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        cache_id     = store_result.cache_id
        result = self.admin_storage.files__all__path(path = namespace)
        assert type(result)         is Schema__Routes__Admin__Storage__Files_All__Response
        assert result.obj()         == __( timestamp  = __SKIP__,
                                           file_count = 9,
                                           files      = [ f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',
                                                          f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config',
                                                          f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata',
                                                          f'{namespace}/refs/by-hash/9c/af/9caf1f672d20295b.json',
                                                          f'{namespace}/refs/by-hash/9c/af/9caf1f672d20295b.json.config',
                                                          f'{namespace}/refs/by-hash/9c/af/9caf1f672d20295b.json.metadata',
                                                          f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json',
                                                          f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config',
                                                          f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata'])


    def test__folders__default_params(self):                                     # Test listing folders with default parameters
        result = self.admin_storage.folders()
        assert type(result) is list
        assert len(result) >= 0
        #assert result == []

    def test__folders__with_path(self):                                          # Test listing folders in specific path
        namespace   = "test-admin-folders"
        test_data   = {"data": "test"}
        cache_hash  = self.cache_service.hash_from_json(test_data)
        self.cache_service.store_with_strategy(storage_data = test_data ,
                                               cache_hash   = cache_hash ,
                                               strategy     = "direct"   ,
                                               namespace    = namespace  )
        result = self.admin_storage.folders(path = namespace)
        assert type(result) is list
        assert result == ['data', 'refs']

    def test__folders__with_return_full_path(self):                              # Test listing folders with full path option
        result = self.admin_storage.folders(path              = '',
                                            return_full_path = True)
        assert type(result) is list
        #assert result == []

    def test__delete__file__with_existing_file(self):                            # Test deleting an existing file
        test_data   = {"to_delete": True}
        namespace   = "test-admin-delete"
        cache_hash  = self.cache_service.hash_from_json(test_data)
        store_result = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        file_path     = store_result.paths['data'][0]
        exists_result = self.admin_storage.file__exists(file_path)
        assert exists_result == { 'exists': True,
                                  'path'  : file_path}
        delete_result = self.admin_storage.file__delete(file_path)
        assert delete_result == {'deleted': True,
                                 'path'   : file_path}

        exists_after = self.admin_storage.file__exists(file_path)
        assert exists_after == { 'exists': False,
                                 'path': file_path}
        delete_after = self.admin_storage.file__delete(file_path)
        assert delete_after == {'deleted': False,
                                 'path'   : file_path}


    def test__delete__file__with_nonexistent_file(self):                         # Test deleting non-existent file
        test_path = 'nonexistent/file.json'
        result    = self.admin_storage.file__delete(test_path)
        assert type(result) is dict
        assert result       == { 'deleted': False,
                                 'path'   : test_path}


    def test__edge_case__empty_path(self):                                       # Test operations with empty path
        result = self.admin_storage.files__in__path(path = '')
        assert type(result) is list

    def test__edge_case__special_characters_in_path(self):                       # Test file operations with special characters
        test_path = 'test/path/with-special_chars.json'
        result    = self.admin_storage.file__exists(test_path)
        assert type(result)      is dict
        assert 'exists'         in result
        assert result['exists'] is False

    def test__integration__create_check_retrieve_delete(self):                   # Integration test: create, check, retrieve, and delete file
        namespace  = "test-admin-integration"
        test_data  = {"integration": "test", "complete": True}
        cache_hash = self.cache_service.hash_from_json(test_data)
        store_result = self.cache_service.store_with_strategy(storage_data = test_data ,
                                                              cache_hash   = cache_hash ,
                                                              strategy     = "direct"   ,
                                                              namespace    = namespace  )
        file_path      = store_result.paths['data'][0]
        exists_result  = self.admin_storage.file__exists(file_path)
        assert exists_result['exists'] is True
        json_result    = self.admin_storage.file__json(file_path)
        assert json_result == test_data
        bytes_result   = self.admin_storage.file__bytes(file_path)
        assert type(bytes_result) is bytes
        assert len(bytes_result) > 0
        delete_result  = self.admin_storage.file__delete(file_path)
        assert type(delete_result) is dict
        exists_after   = self.admin_storage.file__exists(file_path)
        assert exists_after['exists'] is False
        assert delete_result == { 'deleted': True      ,
                                  'path'   : file_path }

