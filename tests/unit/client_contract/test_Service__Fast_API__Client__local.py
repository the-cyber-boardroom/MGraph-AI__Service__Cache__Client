from unittest                                                                           import TestCase
from osbot_fast_api.utils.Fast_API_Server                                               import Fast_API_Server
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                    import Serverless__Fast_API__Config
from osbot_utils.helpers.duration.decorators.capture_duration                           import capture_duration
from osbot_utils.testing.__                                                             import __, __SKIP__
from osbot_utils.utils.Http                                                             import GET_json, url_join_safe
from osbot_utils.utils.Misc                                                             import list_set, is_guid, random_string, random_bytes
from osbot_utils.utils.Objects                                                          import obj
from mgraph_ai_service_cache.fast_api.Service__Fast_API                                 import Service__Fast_API
from mgraph_ai_service_cache.utils.Version                                              import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client           import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config   import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Requests import Service__Fast_API__Client__Requests, Service__Fast_API__Client__Requests__Result
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy    import Enum__Cache__Store__Strategy

from osbot_utils.utils.Dev import pprint


class test_Service__Fast_API__Client__local(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with capture_duration() as duration:
            cls.serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)
            cls.cache_service__fast_api = Service__Fast_API(config=cls.serverless_config).setup()
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
    <title>Service__Fast_API - Swagger UI</title>
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