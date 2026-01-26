from unittest                                                               import TestCase

from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client

from osbot_utils.testing.__ import __, __SKIP__
from osbot_fast_api.services.registry.Fast_API__Service__Registry           import Fast_API__Service__Registry
from mgraph_ai_service_cache_client.client.Cache__Service__Registry__Client import service_registry__register__cache_service, Cache__Service__Registry__Client


# ═══════════════════════════════════════════════════════════════════════════════
# Pattern Test - Service Consumer Using Registry
# Demonstrates how business logic should discover services
# ═══════════════════════════════════════════════════════════════════════════════

class test_Cache__Service__consumer_pattern(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.registry                       = Fast_API__Service__Registry()                                          # create registry for these tests
        cls.cache_service__registry_client = service_registry__register__cache_service(registry = cls.registry)     # register cache_service

    def test__setUpClass(self):
        assert type(self.registry                      ) is Fast_API__Service__Registry
        assert type(self.cache_service__registry_client) is Cache__Service__Registry__Client
        assert self.registry.obj()                       == __(clients=__(mgraph_ai_service_cache_client_client_Cache__Service__Registry__Client_Cache__Service__Registry__Client=__(cache_client=__SKIP__,
                                                                                                                                                                                     Cache__Service__Fast_API__Client=None,
                                                                                                                                                                                     config=__(mode='in_memory',
                                                                                                                                                                                               fast_api_app='FastAPI',
                                                                                                                                                                                               base_url=None,
                                                                                                                                                                                               api_key_name=None,
                                                                                                                                                                                               api_key_value=None))))
        assert self.cache_service__registry_client.obj() == __(cache_client=__SKIP__,
                                                               Cache__Service__Fast_API__Client=None,
                                                               config=__(mode='in_memory',
                                                                         fast_api_app='FastAPI',
                                                                         base_url=None,
                                                                         api_key_name=None,
                                                                         api_key_value=None))




    def test__consumer_pattern__discovers_cache_client(self):                                       # Pattern: How services discover dependencies

        cache_service__registry_client = self.registry.client(Cache__Service__Registry__Client)     # This is how a service (e.g., Html_Graph__Service) would discover cache

        assert type(cache_service__registry_client) is Cache__Service__Registry__Client
        assert cache_service__registry_client       == self.cache_service__registry_client


        with cache_service__registry_client as _:
            assert _.health()            is True
            assert  type(_.cache_client) is Cache__Service__Fast_API__Client
            health = _.cache_client.info().health()       # Now use the client
            assert health.get('status') == 'ok'

    def test__consumer_pattern__graceful_handling_of_missing_client(self):      # Pattern: Handle missing registration
        empty_registry = Fast_API__Service__Registry()                          # Fresh registry with nothing registered

        cache_client = empty_registry.client(Cache__Service__Registry__Client)

        assert cache_client is None                                             # Not registered = None


    # ═══════════════════════════════════════════════════════════════════════════════
    # Pattern Test - Multiple Registries for Test Isolation
    # Demonstrates test isolation with separate registry instances
    # ═══════════════════════════════════════════════════════════════════════════════



    def test__separate_registries__are_isolated(self):                          # Each registry instance is independent
        registry_1 = Fast_API__Service__Registry()
        registry_2 = Fast_API__Service__Registry()
        client_1 = service_registry__register__cache_service(registry = registry_1)
        client_2 = service_registry__register__cache_service(registry = registry_2)


        assert registry_1.client(Cache__Service__Registry__Client) is client_1              # Each registry has its own client
        assert registry_2.client(Cache__Service__Registry__Client) is client_2
        assert client_1 is not client_2

    def test__clear__isolates_tests(self):                                      # Clear method for test cleanup
        registry_1 = Fast_API__Service__Registry()
        client_1   = service_registry__register__cache_service(registry = registry_1)

        assert registry_1.is_registered(Cache__Service__Registry__Client) is True

        registry_1.clear()

        assert registry_1.is_registered(Cache__Service__Registry__Client) is False
        assert registry_1.client(Cache__Service__Registry__Client)        is None