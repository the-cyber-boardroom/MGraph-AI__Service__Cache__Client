# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Service__Client__integration
# Integration tests for Cache service client with actual FastAPI app
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                         import register_cache_service__in_memory
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                       import fast_api__service__registry
from osbot_fast_api.services.schemas.registry.enums.Enum__Fast_API__Service__Registry__Client__Mode     import Enum__Fast_API__Service__Registry__Client__Mode


class test_Cache__Service__Client__integration(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup once for all tests
        fast_api__service__registry.configs__save()
        cls.cache_service_client = register_cache_service__in_memory(return_client=True)


    @classmethod
    def tearDownClass(cls):                                                     # Restore global registry
        fast_api__service__registry.configs__restore()

    # ───────────────────────────────────────────────────────────────────────────
    # Health Check Tests
    # ───────────────────────────────────────────────────────────────────────────

    def test__health__returns_true(self):                                       # Test health() method
        with self.cache_service_client as _:
            assert _.health() is True

    def test__info__health__returns_ok(self):                                   # Test info().health() endpoint
        with self.cache_service_client as _:
            result = _.info().health()
            assert result.get('status') == 'ok'

    # ───────────────────────────────────────────────────────────────────────────
    # Config Lookup Tests
    # ───────────────────────────────────────────────────────────────────────────

    def test__requests__config__returns_registered_config(self):                # Test config lookup
        with self.cache_service_client as _:
            config = _.requests().config()

            assert config is not None
            assert config.mode == Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY

    def test__requests__config__has_fast_api_app(self):                         # Test config has app
        with self.cache_service_client as _:
            config = _.requests().config()

            assert config.fast_api_app is not None

    # ───────────────────────────────────────────────────────────────────────────
    # Store Operations Tests
    # ───────────────────────────────────────────────────────────────────────────

    def test__store__json__cache_key(self):                                     # Test store JSON with cache key
        with self.cache_service_client as _:
            namespace = 'integration-test-namespace'
            cache_key = 'integration-test-key'
            test_data = {'message': 'hello from integration test',
                         'key'    : 'integration/test/key'        }

            result = _.store().store__json__cache_key(namespace       = namespace  ,
                                                      strategy        = 'direct'   ,
                                                      cache_key       = cache_key  ,
                                                      body            = test_data  ,
                                                      file_id         = 'test'     ,
                                                      json_field_path = 'key'      )

            assert result          is not None
            assert result.cache_id is not None

    def test__store__string(self):                                              # Test store string
        with self.cache_service_client as _:
            namespace = 'integration-test-namespace'
            test_data = 'Hello, World!'

            result = _.store().store__string(namespace = namespace,
                                             strategy  = 'direct' ,
                                             body      = test_data)

            assert result          is not None
            assert result.cache_id is not None

    def test__store__binary(self):                                              # Test store binary
        with self.cache_service_client as _:
            namespace = 'integration-test-namespace'
            test_data = b'binary data here'

            result = _.store().store__binary(namespace = namespace,
                                             strategy  = 'direct' ,
                                             body      = test_data)

            assert result          is not None
            assert result.cache_id is not None

    # ───────────────────────────────────────────────────────────────────────────
    # Retrieve Operations Tests
    # ───────────────────────────────────────────────────────────────────────────

    def test__store_and_retrieve__json(self):                                   # Test store then retrieve
        with self.cache_service_client as _:
            namespace = 'integration-test-namespace'
            cache_key = 'retrieve-test-key'
            test_data = {'message': 'retrieve test', 'key': 'retrieve/test'}

            # Store
            store_result = _.store().store__json__cache_key(namespace       = namespace  ,
                                                            strategy        = 'direct'   ,
                                                            cache_key       = cache_key  ,
                                                            body            = test_data  ,
                                                            file_id         = 'test'     ,
                                                            json_field_path = 'key'      )
            assert store_result is not None

            # Retrieve
            retrieved = _.retrieve().retrieve__cache_id(namespace = namespace             ,
                                                        cache_id  = store_result.cache_id )
            assert retrieved is not None

    # ───────────────────────────────────────────────────────────────────────────
    # Multiple Operations Tests
    # ───────────────────────────────────────────────────────────────────────────

    def test__multiple_store_operations(self):                                  # Test multiple stores
        with self.cache_service_client as _:
            namespace = 'integration-multi-test'

            for i in range(3):
                cache_key = f'multi-key-{i}'
                test_data = {'index': i, 'key': f'multi/{i}'}

                result = _.store().store__json__cache_key(namespace       = namespace   ,
                                                          strategy        = 'direct'    ,
                                                          cache_key       = cache_key   ,
                                                          body            = test_data   ,
                                                          file_id         = f'test-{i}' ,
                                                          json_field_path = 'key'       )
                assert result is not None