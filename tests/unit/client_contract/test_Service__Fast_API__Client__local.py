from unittest                                                                           import TestCase
from osbot_fast_api.utils.Fast_API_Server                                               import Fast_API_Server
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                    import Serverless__Fast_API__Config
from osbot_utils.helpers.duration.decorators.capture_duration                           import capture_duration
from osbot_utils.testing.__                                                             import __, __SKIP__
from osbot_utils.testing.__helpers                                                      import obj
from osbot_utils.utils.Http                                                             import GET_json, url_join_safe
from osbot_utils.utils.Misc                                                             import list_set, is_guid, random_string, random_bytes
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                           import Cache_Service__Fast_API
from mgraph_ai_service_cache.utils.Version                                              import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client           import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config   import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Requests import Service__Fast_API__Client__Requests, Service__Fast_API__Client__Requests__Result
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy    import Enum__Cache__Store__Strategy


class test_Service__Fast_API__Client__local(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with capture_duration() as duration:
            cls.serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)
            cls.cache_service__fast_api = Cache_Service__Fast_API(config=cls.serverless_config).setup()
            cls.fast_api_server         = Fast_API_Server(app=cls.cache_service__fast_api.app())
            cls.server_url              = cls.fast_api_server.url().rstrip("/")                              # note: the trailing / was causing issues with the auto-generated request code


            cls.server_config           = Service__Fast_API__Client__Config(base_url=cls.server_url, verify_ssl=False)
            cls.fast_api_client         = Service__Fast_API__Client        (config=cls.server_config)

            cls.fast_api_server.start()

        #assert duration.seconds < 0.5               # server setup and start should not take more than 0.5 (locally takes about 0.25)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fast_api_server.stop()

    def test__local_server(self):
        assert self.fast_api_server.running is True
        assert GET_json(url_join_safe(self.server_url, '/info/health' )) == { 'status'     : 'ok'                            }
        assert GET_json(url_join_safe(self.server_url, '/info/status' )) == { 'environment': 'local'                         ,
                                                                              'name'       : 'mgraph_ai_service_cache'       ,
                                                                              'status'     : 'operational'                   ,
                                                                              'version'    : version__mgraph_ai_service_cache}
    def test__init__(self):
        with self.fast_api_client as _:
            assert _.config.obj() == __(base_url       = self.server_url    ,
                                       api_key         = None               ,
                                       api_key_header  = 'X-API-Key'        ,
                                       timeout         = 30                 ,
                                       verify_ssl      = False              ,
                                       service_name    ='Service__Fast_API' ,
                                       service_version = 'v0.5.67'          )

    def test__direct__docs(self):
        with self.fast_api_client.info() as _:
            assert type(_._client          ) is Service__Fast_API__Client
            assert type(_._client._requests) is Service__Fast_API__Client__Requests

        with self.fast_api_client.info()._client._requests as _:
            kwargs = dict(method = 'GET',
                          path   = '/docs')
            response = _.execute(**kwargs)
            assert type(response) is Service__Fast_API__Client__Requests__Result
            assert response.status_code == 200
            expected_html__docs = """
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>Cache_Service__Fast_API - Swagger UI</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({
        url: '/openapi.json',
    "dom_id": "#swagger-ui",
"layout": "BaseLayout",
"deepLinking": true,
"showExtensions": true,
"showCommonExtensions": true,
oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })
    </script>
    </body>
    </html>
    """
            assert response.text == expected_html__docs

    def test__direct__openapi_json(self):
        with self.fast_api_client.info()._client._requests as _:
            kwargs = dict(method = 'GET',
                          path   = '/openapi.json')
            response = _.execute(**kwargs)
            assert type(response) is Service__Fast_API__Client__Requests__Result
            assert response.status_code == 200
            paths = response.json.get('paths')

            assert list_set(paths) == [  '/admin/storage/bucket-name',
                                         '/admin/storage/file/bytes/{path}',
                                         '/admin/storage/file/exists/{path}',
                                         '/admin/storage/file/json/{path}',
                                         '/admin/storage/files/all/{path}',
                                         '/admin/storage/files/parent-path',
                                         '/admin/storage/folders',
                                         '/admin/storage/{path}',
                                         '/auth/set-auth-cookie',
                                         '/auth/set-cookie-form',
                                         '/info/health',
                                         '/info/server',
                                         '/info/status',
                                         '/info/versions',
                                         '/server/create/test-fixtures',
                                         '/server/storage/info',
                                         '/{namespace}/cache/{cache_id}/data/binary/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/binary/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/delete/all',
                                         '/{namespace}/cache/{cache_id}/data/delete/all/{data_key}',
                                         '/{namespace}/cache/{cache_id}/data/delete/{data_type}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/delete/{data_type}/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/json/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/json/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/binary',
                                         '/{namespace}/cache/{cache_id}/data/store/binary/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/binary/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/json',
                                         '/{namespace}/cache/{cache_id}/data/store/json/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/json/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/string',
                                         '/{namespace}/cache/{cache_id}/data/store/string/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/store/string/{data_key}/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/string/{data_file_id}',
                                         '/{namespace}/cache/{cache_id}/data/string/{data_key}/{data_file_id}',
                                         '/{namespace}/delete/{cache_id}',
                                         '/{namespace}/exists/hash/{cache_hash}',
                                         '/{namespace}/file-hashes',
                                         '/{namespace}/file-ids',
                                         '/{namespace}/retrieve/hash/{cache_hash}',
                                         '/{namespace}/retrieve/hash/{cache_hash}/binary',
                                         '/{namespace}/retrieve/hash/{cache_hash}/json',
                                         '/{namespace}/retrieve/hash/{cache_hash}/string',
                                         '/{namespace}/retrieve/{cache_id}',
                                         '/{namespace}/retrieve/{cache_id}/binary',
                                         '/{namespace}/retrieve/{cache_id}/config',
                                         '/{namespace}/retrieve/{cache_id}/json',
                                         '/{namespace}/retrieve/{cache_id}/metadata',
                                         '/{namespace}/retrieve/{cache_id}/refs',
                                         '/{namespace}/retrieve/{cache_id}/refs/all',
                                         '/{namespace}/retrieve/{cache_id}/string',
                                         '/{namespace}/stats',
                                         '/{namespace}/zip/{cache_id}/batch/operations',
                                         '/{namespace}/zip/{cache_id}/file/add/from/bytes/{file_path}',
                                         '/{namespace}/zip/{cache_id}/file/add/from/string/{file_path}',
                                         '/{namespace}/zip/{cache_id}/file/delete/{file_path}',
                                         '/{namespace}/zip/{cache_id}/file/retrieve/{file_path}',
                                         '/{namespace}/zip/{cache_id}/files/list',
                                         '/{namespace}/zip/{cache_id}/retrieve',
                                         '/{namespace}/{strategy}/store/binary',
                                         '/{namespace}/{strategy}/store/binary/{cache_key}',
                                         '/{namespace}/{strategy}/store/json',
                                         '/{namespace}/{strategy}/store/json/{cache_key}',
                                         '/{namespace}/{strategy}/store/string',
                                         '/{namespace}/{strategy}/store/string/{cache_key}',
                                         '/{namespace}/{strategy}/zip/create/{cache_key}/{file_id}',
                                         '/{namespace}/{strategy}/zip/store/{cache_key}/{file_id}']

    def test_info(self):
        with self.fast_api_client.info() as _:
            assert _.health() == { 'status'     : 'ok'                             }
            assert _.status() == { 'environment': 'local'                          ,
                                   'name'       : 'mgraph_ai_service_cache'        ,
                                   'status'     : 'operational'                    ,
                                   'version'    : version__mgraph_ai_service_cache }

    def test_admin_storage(self):
        with self.fast_api_client.admin_storage() as _:
            assert _.bucket_name() == {'bucket-name': 'NA'}
            assert _.folders    () == '[]'                            # BUG, this should be a valid json object

    def test_storage__store__string(self):
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            body       = 'this is a test value'

            result     = _.store__string(strategy   = strategy  ,
                                         namespace  = namespace ,
                                         body       = body      )

            cache_id   = result.get('cache_id')
            cache_hash = result.get('cache_hash')

            assert is_guid(cache_id) is True

            expected   = __(cache_id   = cache_id                                     ,
                            cache_hash = cache_hash                                   ,
                            namespace  = namespace                                   ,
                            paths      = __( data    = [ f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json'         ,
                                                         f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config'   ,
                                                         f'{namespace}/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata' ],
                                             by_hash = [ f'{namespace}/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json'       ,
                                                         f'{namespace}/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json.config',
                                                         f'{namespace}/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json.metadata'],
                                             by_id   = [ f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json'             ,
                                                         f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.config'       ,
                                                         f'{namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json.metadata' ] ),
                            size       = len(body.encode('utf-8')) + 2 )

            assert obj(result) == expected


    def test_storage__store__json(self):
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            body       = {'answer': 42 }

            result     = _.store__json(strategy   = strategy  ,
                                       namespace  = namespace ,
                                       body       = body      )
            assert type(result) is dict
            assert is_guid(result.get('cache_id')) is True
            assert result.get('namespace'        ) == namespace
            assert result.get('size'             ) == 18

    def test_storage__store__binary(self):
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            body       = b"these are some bytes!"

            result     = _.store__binary(strategy   = strategy  ,
                                         namespace  = namespace ,
                                         body       = body      )

            assert type(result) is dict
            assert is_guid(result.get('cache_id')) is True
            assert result.get('namespace'        ) == namespace
            assert result.get('size'             ) == 21

    def test_retrieve__string(self):
        strategy   = Enum__Cache__Store__Strategy.DIRECT
        namespace  = 'pytests'
        an_string  = random_string('this is a random value')

        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.retrieve() as _:
            retrieve__result = _.retrieve__cache_id__string(cache_id=cache_id, namespace=namespace)

        assert is_guid(cache_id) is True
        assert retrieve__result  == an_string


    def test_retrieve__json(self):
        strategy   = Enum__Cache__Store__Strategy.DIRECT
        namespace  = 'pytests'
        an_json    = {'answer' : random_string('this is a random value') }

        with self.fast_api_client.store() as _:
            store__result = _.store__json(strategy=strategy, namespace=namespace, body=an_json)
            cache_id      = store__result.get('cache_id')


        with self.fast_api_client.retrieve() as _:
            retrieve__result = _.retrieve__cache_id__json(cache_id=cache_id, namespace=namespace)

        assert is_guid(cache_id)      is True
        assert type(retrieve__result) is dict
        assert retrieve__result       == an_json

    def test_retrieve__bytes(self):
        strategy   = Enum__Cache__Store__Strategy.DIRECT
        namespace  = 'pytests'
        an_binary  = random_bytes()

        with self.fast_api_client.store() as _:
            store__result = _.store__binary(strategy=strategy, namespace=namespace, body=an_binary)
            cache_id      = store__result.get('cache_id')


        with self.fast_api_client.retrieve() as _:
            retrieve__result = _.retrieve__cache_id__binary(cache_id=cache_id, namespace=namespace)

        assert is_guid(cache_id)      is True
        assert type(retrieve__result) is bytes
        assert retrieve__result       == an_binary

    def test_store__data__string(self):
        strategy     = Enum__Cache__Store__Strategy.DIRECT
        namespace    = 'pytests'
        an_string    = random_string('this is a random value')
        data_key     = 'some/data/key'
        data_file_id = 'an-data-file-id'
        data_string  = 'this is some data'

        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.data_store() as _:
            store_string__result                 = _.data__store_string(cache_id=cache_id, namespace=namespace, body=data_string)
            store_string__file_id                = store_string__result.get('file_id')

            store_string__with_id__result        = _.data__store_string__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_string)

            store_string__with_id_and_key_result = _.data__store_string__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_string)



        assert obj(store_string__result) == __(cache_id            = cache_id                                    ,
                                               data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{store_string__file_id}.txt' ],
                                               data_key            = ''                                          ,
                                               data_type           = 'string'                                    ,
                                               extension           = 'txt'                                       ,
                                               file_id             = store_string__file_id                       ,
                                               file_size           = 17                                          ,
                                               namespace           = 'pytests'                                   ,
                                               timestamp           = __SKIP__ )

        assert obj(store_string__with_id__result) == __(cache_id            = cache_id                                    ,
                                                        data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/an-data-file-id.txt' ],
                                                        data_key            = ''                                  ,
                                                        data_type           = 'string'                            ,
                                                        extension           = 'txt'                               ,
                                                        file_id             = 'an-data-file-id'                   ,
                                                        file_size           = 17                                  ,
                                                        namespace           = 'pytests'                           ,
                                                        timestamp           = __SKIP__ )

        assert obj(store_string__with_id_and_key_result) == __(cache_id            = cache_id                                    ,
                                                               data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/some/data/key/an-data-file-id.txt' ],
                                                               data_key            = 'some/data/key'               ,
                                                               data_type           = 'string'                      ,
                                                               extension           = 'txt'                         ,
                                                               file_id             = 'an-data-file-id'             ,
                                                               file_size           = 17                            ,
                                                               namespace           = 'pytests'                     ,
                                                               timestamp           = __SKIP__ )


    def test_store__data__json(self):
        strategy     = Enum__Cache__Store__Strategy.DIRECT
        namespace    = 'pytests'
        an_string    = random_string('this is a random value')
        data_key     = 'some/data/key'
        data_file_id = 'an-data-file-id'
        data_json    = {'answer': 42, 'question': 'what is the meaning of life?' + random_string()}

        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.data_store() as _:
            store_json__result                 = _.data__store_json(cache_id=cache_id, namespace=namespace, body=data_json)
            store_json__file_id                = store_json__result.get('file_id')

            store_json__with_id__result        = _.data__store_json__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_json)

            store_json__with_id_and_key_result = _.data__store_json__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_json)


        assert obj(store_json__result) == __(cache_id            = cache_id,
                                             data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{store_json__file_id}.json' ],
                                             data_key            = '',
                                             data_type           = 'json',
                                             extension           = 'json',
                                             file_id             = store_json__file_id,
                                             file_size           = 76       ,
                                             namespace           = 'pytests',
                                             timestamp           = __SKIP__ )

        assert obj(store_json__with_id__result) == __(cache_id            = cache_id,
                                                      data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/an-data-file-id.json' ],
                                                      data_key            = '',
                                                      data_type           = 'json',
                                                      extension           = 'json',
                                                      file_id             = 'an-data-file-id',
                                                      file_size           = 76       ,
                                                      namespace           = 'pytests',
                                                      timestamp           = __SKIP__ )

        assert obj(store_json__with_id_and_key_result) == __(cache_id            = cache_id,
                                                             data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/some/data/key/an-data-file-id.json' ],
                                                             data_key            = 'some/data/key',
                                                             data_type           = 'json',
                                                             extension           = 'json',
                                                             file_id             = 'an-data-file-id',
                                                             file_size           = 76       ,
                                                             namespace           = 'pytests',
                                                             timestamp           = __SKIP__ )


    def test_store__data__binary(self):
        strategy     = Enum__Cache__Store__Strategy.DIRECT
        namespace    = 'pytests'
        an_string    = random_string('this is a random value')
        data_key     = 'some/data/key'
        data_file_id = 'an-data-file-id'
        data_binary  = random_bytes()

        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.data_store() as _:
            store_binary__result                 = _.data__store_binary(cache_id=cache_id, namespace=namespace, body=data_binary)
            store_binary__file_id                = store_binary__result.get('file_id')

            store_binary__with_id__result        = _.data__store_binary__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_binary)

            store_binary__with_id_and_key_result = _.data__store_binary__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_binary)

        assert obj(store_binary__result) == __(cache_id            = cache_id,
                                               data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/{store_binary__file_id}.bin' ],
                                               data_key            = '',
                                               data_type           = 'binary',
                                               extension           = 'bin',
                                               file_id             = store_binary__file_id,
                                               file_size           = len(data_binary),
                                               namespace           = 'pytests',
                                               timestamp           = __SKIP__ )

        assert obj(store_binary__with_id__result) == __(cache_id            = cache_id,
                                                        data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/an-data-file-id.bin' ],
                                                        data_key            = '',
                                                        data_type           = 'binary',
                                                        extension           = 'bin',
                                                        file_id             = 'an-data-file-id',
                                                        file_size           = len(data_binary),
                                                        namespace           = 'pytests',
                                                        timestamp           = __SKIP__ )

        assert obj(store_binary__with_id_and_key_result) == __(cache_id            = cache_id,
                                                               data_files_created  = [ f'pytests/data/direct/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}/data/some/data/key/an-data-file-id.bin' ],
                                                               data_key            = 'some/data/key',
                                                               data_type           = 'binary',
                                                               extension           = 'bin',
                                                               file_id             = 'an-data-file-id',
                                                               file_size           = len(data_binary),
                                                               namespace           = 'pytests',
                                                               timestamp           = __SKIP__ )

    def test_store_and_retrieve__data__string(self):
        strategy     = Enum__Cache__Store__Strategy.DIRECT
        namespace    = 'pytests'
        an_string    = random_string('this is a random value')
        data_key     = 'some/data/key'
        data_file_id = 'an-data-file-id'
        data_string_1  = random_string('this is some data')
        data_string_2  = random_string('this is some data')
        data_string_3  = random_string('this is some data')

        # Store cache and data
        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')


        with self.fast_api_client.data_store() as _:
            # Test basic storage (auto-generated file_id)
            store_string__result    = _.data__store_string(cache_id=cache_id, namespace=namespace, body=data_string_1)
            store_string__file_id   = store_string__result.get('file_id')

            # Test storage with specific file_id
            _.data__store_string__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_string_2)

            # Test storage with both key and file_id
            _.data__store_string__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_string_3)


        # Retrieve data
        with self.fast_api_client.data().retrieve() as _:

            # Retrieve with auto-generated file_id
            retrieve_string__result = _.data__string__with__id(cache_id=cache_id, namespace=namespace, data_file_id=store_string__file_id)

            # Retrieve with specific file_id
            retrieve_string__with_id__result = _.data__string__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id)

            # Retrieve with specific file_id and data_key
            retrieve_string__with_id_and_key__result = _.data__string__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id)

        # Assertions
        assert is_guid(cache_id)                             is True
        assert retrieve_string__result                       == data_string_1
        assert retrieve_string__with_id__result              == data_string_2
        assert retrieve_string__with_id_and_key__result      == data_string_3


    def test_store_and_retrieve__data__json(self):
        strategy     = Enum__Cache__Store__Strategy.DIRECT
        namespace    = 'pytests'
        an_string    = random_string('this is a random value')
        data_key     = 'some/data/key'
        data_file_id = 'an-data-file-id'
        data_json_1  = {'answer': random_string('random answer'), 'number': 42}
        data_json_2  = {'answer': random_string('random answer'), 'number': 42}
        data_json_3  = {'answer': random_string('random answer'), 'number': 42}

        # Store cache and data
        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.data_store() as _:
            # Test basic storage (auto-generated file_id)
            store_json__result  = _.data__store_json(cache_id=cache_id, namespace=namespace, body=data_json_1)
            store_json__file_id = store_json__result.get('file_id')

            # Test storage with specific file_id
            _.data__store_json__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_json_2)

            # Test storage with both key and file_id
            _.data__store_json__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_json_3)

        # Retrieve data
        with self.fast_api_client.data().retrieve() as _:
            # Retrieve with auto-generated file_id
            retrieve_json__result = _.data__json__with__id(cache_id=cache_id, namespace=namespace, data_file_id=store_json__file_id)

            # Retrieve with specific file_id
            retrieve_json__with_id__result = _.data__json__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id)

            # Retrieve with both key and file_id
            retrieve_json__with_id_and_key__result = _.data__json__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id)

        # Assertions
        assert is_guid(cache_id)                         is True
        assert type(retrieve_json__result)               is dict
        assert retrieve_json__result                     == data_json_1
        assert retrieve_json__with_id__result            == data_json_2
        assert retrieve_json__with_id_and_key__result    == data_json_3


    def test_store_and_retrieve__data__binary(self):
        strategy       = Enum__Cache__Store__Strategy.DIRECT
        namespace      = 'pytests'
        an_string      = random_string('this is a random value')
        data_key       = 'some/data/key'
        data_file_id   = 'an-data-file-id'
        data_binary_1  = random_bytes()
        data_binary_2  = random_bytes()
        data_binary_3  = random_bytes()

        # Store cache and data
        with self.fast_api_client.store() as _:
            store__result = _.store__string(strategy=strategy, namespace=namespace, body=an_string)
            cache_id      = store__result.get('cache_id')

        with self.fast_api_client.data_store() as _:
            # Test basic storage (auto-generated file_id)
            store_binary__result  = _.data__store_binary(cache_id=cache_id, namespace=namespace, body=data_binary_1)
            store_binary__file_id = store_binary__result.get('file_id')

            # Test storage with specific file_id
            _.data__store_binary__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id, body=data_binary_2)

            # Test storage with both key and file_id
            _.data__store_binary__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id, body=data_binary_3)

        # Retrieve data
        with self.fast_api_client.data().retrieve() as _:
            # Retrieve with auto-generated file_id
            retrieve_binary__result = _.data__binary__with__id(cache_id=cache_id, namespace=namespace, data_file_id=store_binary__file_id)

            # Retrieve with specific file_id
            retrieve_binary__with_id__result = _.data__binary__with__id(cache_id=cache_id, namespace=namespace, data_file_id=data_file_id)

            # Retrieve with both key and file_id
            retrieve_binary__with_id_and_key__result = _.data__binary__with__id_and_key(cache_id=cache_id, namespace=namespace, data_key=data_key, data_file_id=data_file_id)

        # Assertions
        assert is_guid(cache_id)                             is True
        assert type(retrieve_binary__result)                 is bytes
        assert retrieve_binary__result                       == data_binary_1
        assert retrieve_binary__with_id__result              == data_binary_2
        assert retrieve_binary__with_id_and_key__result      == data_binary_3


    def test_storage__store__string__with_cache_key(self):      # Test storing string data with a cache_key parameter
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            cache_key  = 'test/string/cache/key'
            body       = 'this is a test value with cache key'

            result     = _.store__string__cache_key(namespace  = namespace  ,
                                                    strategy   = strategy   ,
                                                    cache_key  = cache_key  ,
                                                    body       = body       )

            cache_id   = result.get('cache_id')
            cache_hash = result.get('cache_hash')

            assert is_guid(cache_id) is True
            assert result.get('namespace') == namespace
            assert result.get('size') > 0

            # Verify we can retrieve it back
            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__string(cache_id=cache_id, namespace=namespace )
            assert retrieve_result == body


    def test_storage__store__json__with_cache_key(self):        # Test storing JSON data with a cache_key parameter
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            cache_key  = 'test/json/cache/key'
            body       = {'answer': 42, 'question': 'meaning of life', 'cache_key': cache_key}

            result     = _.store__json__cache_key(namespace  = namespace,
                                                  strategy   = strategy ,
                                                  cache_key  = cache_key,
                                                  body       = body     )

            cache_id   = result.get('cache_id')
            cache_hash = result.get('cache_hash')
            assert cache_hash               == "224b0b70739c9b17"
            assert is_guid(cache_id)        is True
            assert result.get('namespace')  == namespace
            assert result.get('size')       == len(str(body).encode('utf-8')) + 2 + 6

            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__json(cache_id  = cache_id ,       # Verify retrieval
                                                                                       namespace = namespace)
            assert retrieve_result == body

    def test_storage__store__json__with_cache_key__and__json_field_path(self):        # Test storing JSON data with a cache_key parameter
        with self.fast_api_client.store() as _:
            strategy        = Enum__Cache__Store__Strategy.DIRECT
            namespace       = 'pytests'
            cache_key       = 'test/json/cache/key'
            body            = {'answer': 42, 'question': 'meaning of life', 'cache_key': cache_key}
            json_field_path = "answer"

            result     = _.store__json__cache_key(namespace       = namespace      ,
                                                  strategy        = strategy       ,
                                                  cache_key       = cache_key      ,
                                                  body            = body           ,
                                                  json_field_path = json_field_path)

            cache_id   = result.get('cache_id')
            cache_hash = result.get('cache_hash')
            assert cache_hash               == "73475cb40a568e8d"
            assert is_guid(cache_id)        is True
            assert result.get('namespace')  == namespace
            assert result.get('size')       == len(str(body).encode('utf-8')) + 2 + 6

            retrieve_result_1 = self.fast_api_client.retrieve().retrieve__cache_id__json  (cache_id  = cache_id ,       # Verify retrieval
                                                                                           namespace = namespace)
            retrieve_result_2 = self.fast_api_client.retrieve().retrieve__hash__cache_hash(cache_hash  = cache_hash ,       # Verify retrieval
                                                                                           namespace = namespace)
            assert retrieve_result_1             == body
            assert retrieve_result_2.get('data') == body



    def test_storage__store__binary__with_cache_key(self):
        """Test storing binary data with a cache_key parameter"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.DIRECT
            namespace  = 'pytests'
            cache_key  = 'test/binary/cache/key'
            body       = b"these are some bytes with cache key!"

            result     = _.store__binary__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body
            )

            cache_id   = result.get('cache_id')

            assert is_guid(cache_id) is True
            assert result.get('namespace') == namespace
            assert result.get('size') == len(body)

            # Verify retrieval
            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__binary(
                cache_id=cache_id,
                namespace=namespace
            )
            assert retrieve_result == body


    def test_storage__store__all_strategies(self):
        """Test storing data with different strategies"""
        strategies = [
            Enum__Cache__Store__Strategy.DIRECT,
            Enum__Cache__Store__Strategy.TEMPORAL,
            Enum__Cache__Store__Strategy.TEMPORAL_LATEST,
            Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED,
            Enum__Cache__Store__Strategy.KEY_BASED
        ]

        namespace = 'pytests'
        body      = 'test value for different strategies'

        results = {}

        with self.fast_api_client.store() as _:
            for strategy in strategies:
                result = _.store__string(
                    strategy  = strategy,
                    namespace = namespace,
                    body      = body
                )

                cache_id = result.get('cache_id')
                assert is_guid(cache_id) is True
                results[strategy.value] = cache_id

                # Verify each can be retrieved
                retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__string(
                    cache_id=cache_id,
                    namespace=namespace
                )
                assert retrieve_result == body

        # Verify we got unique cache_ids for each strategy
        assert len(set(results.values())) == len(strategies)


    def test_storage__store__with_cache_key__temporal_strategies(self):
        """Test cache_key parameter works with temporal strategies"""
        with self.fast_api_client.store() as _:
            namespace = 'pytests'
            cache_key = 'temporal/test/key'
            body      = {'test': 'temporal data', 'timestamp': random_string()}

            # Test TEMPORAL strategy
            result_temporal = _.store__json__cache_key(
                namespace = namespace,
                strategy  = Enum__Cache__Store__Strategy.TEMPORAL,
                cache_key = cache_key,
                body      = body
            )

            # Test TEMPORAL_LATEST strategy
            result_temporal_latest = _.store__json__cache_key(
                namespace = namespace,
                strategy  = Enum__Cache__Store__Strategy.TEMPORAL_LATEST,
                cache_key = cache_key,
                body      = body
            )

            assert is_guid(result_temporal.get('cache_id')) is True
            assert is_guid(result_temporal_latest.get('cache_id')) is True


    def test_storage__store__string__all_data_types_with_key(self):
        """Test storing all data types (string, json, binary) with cache_key"""
        with self.fast_api_client.store() as _:
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED
            namespace = 'pytests'

            # Store string
            string_key  = 'test/string/key'
            string_body = random_string('test string value')
            string_result = _.store__string__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = string_key,
                body      = string_body
            )

            # Store JSON
            json_key  = 'test/json/key'
            json_body = {'random': random_string(), 'number': 42}
            json_result = _.store__json__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = json_key,
                body      = json_body
            )

            # Store binary
            binary_key  = 'test/binary/key'
            binary_body = random_bytes()
            binary_result = _.store__binary__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = binary_key,
                body      = binary_body
            )

            # Verify all were stored successfully
            assert is_guid(string_result.get('cache_id')) is True
            assert is_guid(json_result.get('cache_id')) is True
            assert is_guid(binary_result.get('cache_id')) is True

            # Verify retrieval
            string_retrieved = self.fast_api_client.retrieve().retrieve__cache_id__string(
                cache_id=string_result.get('cache_id'),
                namespace=namespace
            )
            assert string_retrieved == string_body

            json_retrieved = self.fast_api_client.retrieve().retrieve__cache_id__json(
                cache_id=json_result.get('cache_id'),
                namespace=namespace
            )
            assert json_retrieved == json_body

            binary_retrieved = self.fast_api_client.retrieve().retrieve__cache_id__binary(
                cache_id=binary_result.get('cache_id'),
                namespace=namespace
            )
            assert binary_retrieved == binary_body


    def test_storage__store__cache_key__special_characters(self):
        """Test cache_key with various path-like structures"""
        with self.fast_api_client.store() as _:
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED
            namespace = 'pytests'

            test_cases = [
                'simple-key',
                'path/to/resource',
                'deep/nested/path/to/resource',
                'with-dashes-and_underscores',
                'with.dots.in.name',
            ]

            for cache_key in test_cases:
                body = f'test value for key: {cache_key}'
                result = _.store__string__cache_key(
                    namespace = namespace,
                    strategy  = strategy,
                    cache_key = cache_key,
                    body      = body
                )

                assert is_guid(result.get('cache_id')) is True
                assert result.get('namespace') == namespace


    def test_storage__store__same_content_different_keys(self):
        """Test storing same content with different cache_keys"""
        with self.fast_api_client.store() as _:
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED
            namespace = 'pytests'
            body      = 'same content for different keys'

            result1 = _.store__string__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = 'key/one',
                body      = body
            )

            result2 = _.store__string__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = 'key/two',
                body      = body
            )

            # Different cache_keys should produce different cache_ids
            cache_id1 = result1.get('cache_id')
            cache_id2 = result2.get('cache_id')

            assert is_guid(cache_id1) is True
            assert is_guid(cache_id2) is True

            # Depending on strategy, these might be the same or different
            # For KEY_BASED strategy, they should be different
            if strategy == Enum__Cache__Store__Strategy.KEY_BASED:
                assert cache_id1 != cache_id2


    def test_storage__store__versioning_with_temporal_versioned(self):
        """Test that TEMPORAL_VERSIONED creates multiple versions"""
        with self.fast_api_client.store() as _:
            strategy  = Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED
            namespace = 'pytests'
            cache_key = 'versioned/test/key'

            # Store multiple versions of the same cache_key
            versions = []
            for i in range(3):
                body = f'version {i} content'
                result = _.store__string__cache_key(
                    namespace = namespace,
                    strategy  = strategy,
                    cache_key = cache_key,
                    body      = body
                )
                versions.append(result.get('cache_id'))

            # All versions should have unique cache_ids
            assert len(set(versions)) == 3

            # Verify each version can be retrieved
            for i, cache_id in enumerate(versions):
                retrieved = self.fast_api_client.retrieve().retrieve__cache_id__string(
                    cache_id=cache_id,
                    namespace=namespace
                )
                assert retrieved == f'version {i} content'

    def test_storage__store__string__cache_key__with_file_id(self):
        """Test storing string with both cache_key and file_id parameters"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'test/cache/key'
            file_id    = 'custom-file-id-string'
            body       = 'test string with custom file_id'

            result = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body,
                file_id    = file_id
            )

            cache_id   = result.get('cache_id')
            cache_hash = result.get('cache_hash')
            paths      = result.get('paths', {})

            # Verify basic response structure
            assert is_guid(cache_id) is True
            assert result.get('namespace') == namespace
            assert result.get('size') > 0

            # Verify that the file_id is used in the data path instead of cache_id
            data_paths = paths.get('data', [])
            assert len(data_paths) == 3  # .json, .config, .metadata

            # Check that file_id appears in the data paths
            assert any(file_id in path for path in data_paths)
            assert f'{cache_key}/{file_id}.json' in data_paths[0]

            # Verify retrieval works
            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__string(
                cache_id=cache_id,
                namespace=namespace
            )
            assert retrieve_result == body


    def test_storage__store__json__cache_key__with_file_id(self):
        """Test storing JSON with both cache_key and file_id parameters"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'test/json/path'
            file_id    = 'my-custom-json-file-id'
            body       = {'answer': 42, 'test': 'file_id usage', 'random': random_string()}

            result = _.store__json__cache_key(namespace  = namespace,
                                              strategy   = strategy ,
                                              cache_key  = cache_key,
                                              body       = body     ,
                                              file_id    = file_id  )

            cache_id = result.get('cache_id')
            paths    = result.get('paths', {})

            assert is_guid(cache_id) is True

            # Verify file_id is used in paths
            data_paths = paths.get('data', [])
            assert any(file_id in path for path in data_paths)
            assert f'{cache_key}/{file_id}.json' in data_paths[0]

            # Verify retrieval
            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__json(
                cache_id=cache_id,
                namespace=namespace
            )
            assert retrieve_result == body


    def test_storage__store__binary__cache_key__with_file_id(self):
        """Test storing binary with both cache_key and file_id parameters"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'test/binary/path'
            file_id    = 'binary-custom-file-id'
            body       = random_bytes()

            result = _.store__binary__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body,
                file_id    = file_id
            )

            cache_id = result.get('cache_id')
            paths    = result.get('paths', {})

            assert is_guid(cache_id) is True

            # Verify file_id is used in paths
            data_paths = paths.get('data', [])
            assert any(file_id in path for path in data_paths)
            assert f'{cache_key}/{file_id}.bin' in data_paths[0]

            # Verify retrieval
            retrieve_result = self.fast_api_client.retrieve().retrieve__cache_id__binary(
                cache_id=cache_id,
                namespace=namespace
            )
            assert retrieve_result == body


    def test_storage__store__with_and_without_file_id__different_cache_ids(self):
        """Test that same content with and without file_id creates different cache_ids"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'test/comparison'
            body       = 'same content'

            # Store without file_id
            result_without_file_id = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body
            )

            # Store with file_id
            result_with_file_id = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body,
                file_id    = 'custom-id'
            )

            cache_id_without = result_without_file_id.get('cache_id')
            cache_id_with    = result_with_file_id.get('cache_id')
            cache_hash_without = result_without_file_id.get('cache_hash')
            cache_hash_with    = result_with_file_id.get('cache_hash')

            # Different cache_ids (different storage locations)
            assert cache_id_without != cache_id_with

            # Same cache_hash (same content)
            assert cache_hash_without == cache_hash_with

            # Verify both can be retrieved
            retrieved_without = self.fast_api_client.retrieve().retrieve__cache_id__string(
                cache_id=cache_id_without,
                namespace=namespace
            )
            retrieved_with = self.fast_api_client.retrieve().retrieve__cache_id__string(
                cache_id=cache_id_with,
                namespace=namespace
            )

            assert retrieved_without == body
            assert retrieved_with == body


    def test_storage__store__file_id__special_characters(self):
        """Test file_id with various valid characters"""
        with self.fast_api_client.store() as _:
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED
            namespace = 'pytests'
            cache_key = 'test/file-ids'

            test_file_ids = [
                'simple-id',
                'id_with_underscores',
                'id-with-dashes',
                'IdWithCamelCase',
                'id123with456numbers',
                'we-can_also_control_the-file-id',  # From your example
            ]

            for file_id in test_file_ids:
                body = f'content for file_id: {file_id}'
                result = _.store__string__cache_key(
                    namespace = namespace,
                    strategy  = strategy,
                    cache_key = cache_key,
                    body      = body,
                    file_id   = file_id
                )

                cache_id   = result.get('cache_id')
                data_paths = result.get('paths', {}).get('data', [])

                assert is_guid(cache_id) is True
                assert any(file_id in path for path in data_paths)

                # Verify retrieval works
                retrieved = self.fast_api_client.retrieve().retrieve__cache_id__string(
                    cache_id=cache_id,
                    namespace=namespace
                )
                assert retrieved == body


    def test_storage__store__file_id__path_structure_verification(self):
        """Test that file_id creates expected path structure"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'my/cache/path'
            file_id    = 'controlled-file-name'
            body       = 'test content'

            result = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body,
                file_id    = file_id
            )

            cache_id = result.get('cache_id')
            paths    = result.get('paths', {})

            # Verify data paths use file_id
            data_paths = paths.get('data', [])
            expected_data_base = f'{namespace}/data/key-based/{cache_key}/{file_id}.json'
            assert expected_data_base in data_paths[0]
            assert f'{expected_data_base}.config' in data_paths[1]
            assert f'{expected_data_base}.metadata' in data_paths[2]

            # Verify by_id paths still use cache_id (first 2 and next 2 chars for sharding)
            by_id_paths = paths.get('by_id', [])
            cache_id_prefix = f'{cache_id[0:2]}/{cache_id[2:4]}'
            assert any(cache_id_prefix in path for path in by_id_paths)


    def test_storage__store__multiple_files_same_cache_key_different_file_ids(self):
        """Test storing multiple files under same cache_key with different file_ids"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'shared/cache/key'

            file_contents = {
                'file-one': 'content for file one',
                'file-two': 'content for file two',
                'file-three': 'content for file three',
            }

            results = {}

            for file_id, body in file_contents.items():
                result = _.store__string__cache_key(
                    namespace = namespace,
                    strategy  = strategy,
                    cache_key = cache_key,
                    body      = body,
                    file_id   = file_id
                )

                cache_id = result.get('cache_id')
                results[file_id] = {
                    'cache_id': cache_id,
                    'body': body
                }

                # Verify each file is stored with the correct file_id
                data_paths = result.get('paths', {}).get('data', [])
                assert any(file_id in path for path in data_paths)

            # All should have different cache_ids
            cache_ids = [r['cache_id'] for r in results.values()]
            assert len(set(cache_ids)) == len(file_contents)

            # Verify all can be retrieved correctly
            for file_id, info in results.items():
                retrieved = self.fast_api_client.retrieve().retrieve__cache_id__string(
                    cache_id=info['cache_id'],
                    namespace=namespace
                )
                assert retrieved == info['body']


    def test_storage__store__file_id__with_all_strategies(self):
        """Test that file_id works with different storage strategies"""
        strategies = [
            Enum__Cache__Store__Strategy.KEY_BASED,
            Enum__Cache__Store__Strategy.TEMPORAL,
            Enum__Cache__Store__Strategy.TEMPORAL_LATEST,
        ]

        namespace  = 'pytests'
        cache_key  = 'test/strategies'
        file_id    = 'strategy-test-file'
        body       = 'testing file_id across strategies'

        results = {}

        with self.fast_api_client.store() as _:
            for strategy in strategies:
                result = _.store__string__cache_key(
                    namespace = namespace,
                    strategy  = strategy,
                    cache_key = cache_key,
                    body      = body,
                    file_id   = file_id
                )

                cache_id = result.get('cache_id')
                results[strategy.value] = cache_id

                # Verify file_id is in the paths
                data_paths = result.get('paths', {}).get('data', [])
                assert any(file_id in path for path in data_paths)

                # Verify retrieval
                retrieved = self.fast_api_client.retrieve().retrieve__cache_id__string(
                    cache_id=cache_id,
                    namespace=namespace
                )
                assert retrieved == body

        # All strategies should create unique cache_ids
        assert len(set(results.values())) == len(strategies)


    def test_storage__store__file_id__empty_string_vs_none(self):
        """Test difference between empty string file_id and not providing file_id"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'test/empty-vs-none'
            body       = 'test content'

            # Store with empty string file_id (default)
            result_empty = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body,
                file_id    = ''
            )

            # Store without providing file_id at all (should use default empty string)
            result_default = _.store__string__cache_key(
                namespace  = namespace,
                strategy   = strategy,
                cache_key  = cache_key,
                body       = body
            )

            cache_id_empty   = result_empty.get('cache_id')
            cache_id_default = result_default.get('cache_id')

            # Both should create valid cache entries
            assert is_guid(cache_id_empty) is True
            assert is_guid(cache_id_default) is True

            # They will be different cache_ids (different storage instances)
            assert cache_id_empty != cache_id_default

            # But same content hash
            assert result_empty.get('cache_hash') == result_default.get('cache_hash')


    def test_storage__store__file_id__json_and_binary_types(self):
        """Comprehensive test of file_id with JSON and binary types"""
        with self.fast_api_client.store() as _:
            strategy   = Enum__Cache__Store__Strategy.KEY_BASED
            namespace  = 'pytests'
            cache_key  = 'multi-type/test'

            # JSON test
            json_file_id = 'config-data'
            json_body    = {'config': 'value', 'number': 123, 'random': random_string()}

            json_result = _.store__json__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = cache_key,
                body      = json_body,
                file_id   = json_file_id
            )

            json_cache_id = json_result.get('cache_id')
            json_paths    = json_result.get('paths', {}).get('data', [])

            assert is_guid(json_cache_id) is True
            assert any(json_file_id in path for path in json_paths)
            assert f'{json_file_id}.json' in json_paths[0]

            # Binary test
            binary_file_id = 'binary-data'
            binary_body    = random_bytes()

            binary_result = _.store__binary__cache_key(
                namespace = namespace,
                strategy  = strategy,
                cache_key = cache_key,
                body      = binary_body,
                file_id   = binary_file_id
            )

            binary_cache_id = binary_result.get('cache_id')
            binary_paths    = binary_result.get('paths', {}).get('data', [])

            assert is_guid(binary_cache_id) is True
            assert any(binary_file_id in path for path in binary_paths)
            assert f'{binary_file_id}.bin' in binary_paths[0]

            # Verify retrievals
            json_retrieved = self.fast_api_client.retrieve().retrieve__cache_id__json(
                cache_id=json_cache_id,
                namespace=namespace
            )
            assert json_retrieved == json_body

            binary_retrieved = self.fast_api_client.retrieve().retrieve__cache_id__binary(
                cache_id=binary_cache_id,
                namespace=namespace
            )
            assert binary_retrieved == binary_body