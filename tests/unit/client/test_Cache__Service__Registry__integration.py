from unittest                                                                                       import TestCase
from mgraph_ai_service_cache_client.client.Cache__Service__Registry__Client                         import Cache__Service__Registry__Client, service_registry__register__cache_service
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                   import Fast_API__Service__Registry
from osbot_fast_api.services.schemas.registry.enums.Enum__Fast_API__Service__Registry__Client__Mode import Enum__Fast_API__Service__Registry__Client__Mode

# ═══════════════════════════════════════════════════════════════════════════════
# Integration Tests - Full Registry Flow with IN_MEMORY Mode
# ═══════════════════════════════════════════════════════════════════════════════

class test_Cache__Service__Registry__integration(TestCase):

    # registry     : Fast_API__Service__Registry       = None
    # cache_client : Cache__Service__Registry__Client  = None

    @classmethod
    def setUpClass(cls):                                                        # Setup once for all tests
        cls.registry = Fast_API__Service__Registry()
        cls.cache_client = service_registry__register__cache_service(registry = cls.registry)

    def test__registry__client_registered(self):                                # Verify client is registered
        assert self.registry.is_registered(Cache__Service__Registry__Client) is True

    def test__registry__client_retrieval(self):                                 # Verify client retrieval
        client = self.registry.client(Cache__Service__Registry__Client)

        assert client                is self.cache_client
        assert type(client)          is Cache__Service__Registry__Client
        assert client.config.mode == Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY

    def test__health_check(self):                                               # Test health check via registry
        client = self.registry.client(Cache__Service__Registry__Client)

        assert client.health() is True

    def test__health_endpoint_directly(self):                                   # Test health endpoint response
        client = self.registry.client(Cache__Service__Registry__Client)
        health = client.cache_client.info().health()

        assert health == {'status': 'ok'}

    def test__store_and_retrieve(self):                                         # Test actual cache operations via registry
        client    = self.registry.client(Cache__Service__Registry__Client)
        namespace = 'registry-test-namespace'
        cache_key = 'registry-test-key'
        test_data = {'message': 'hello from registry',
                     'key'    : 'registry/test/key'   }

        # Store via registry client
        store_result = client.cache_client.store().store__json__cache_key(namespace       = namespace  ,
                                                                          strategy        = 'direct'   ,
                                                                          cache_key       = cache_key  ,
                                                                          body            = test_data  ,
                                                                          file_id         = 'test'     ,
                                                                          json_field_path = 'key'      )

        assert store_result          is not None
        assert store_result.cache_id is not None

        # Retrieve via registry client
        retrieved = client.cache_client.retrieve().retrieve__cache_id(namespace = namespace             ,
                                                                      cache_id  = store_result.cache_id )

        assert retrieved is not None

    def test__multiple_store_operations(self):                                  # Test multiple operations through registry
        client    = self.registry.client(Cache__Service__Registry__Client)
        namespace = 'registry-multi-test'

        for i in range(3):
            cache_key = f'multi-key-{i}'
            test_data = {'index': i, 'key': f'multi/{i}'}

            result = client.cache_client.store().store__json__cache_key(namespace       = namespace  ,
                                                                        strategy        = 'direct'   ,
                                                                        cache_key       = cache_key  ,
                                                                        body            = test_data  ,
                                                                        file_id         = f'test-{i}',
                                                                        json_field_path = 'key'      )
            assert result is not None