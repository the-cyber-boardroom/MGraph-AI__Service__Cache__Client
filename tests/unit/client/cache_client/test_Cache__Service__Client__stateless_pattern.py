# ═══════════════════════════════════════════════════════════════════════════════
# Pattern Tests - Stateless Client
# ═══════════════════════════════════════════════════════════════════════════════
from unittest                                                                   import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client  import Cache__Service__Client
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service import register_cache_service__in_memory
from osbot_fast_api.services.registry.Fast_API__Service__Registry               import Fast_API__Service__Registry, fast_api__service__registry


class test_Cache__Service__Client__stateless_pattern(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.registry = Fast_API__Service__Registry()
        register_cache_service__in_memory(registry=cls.registry)

        cls.original_configs = dict(fast_api__service__registry.configs)
        fast_api__service__registry.configs.clear()
        fast_api__service__registry.configs.update(cls.registry.configs)

    @classmethod
    def tearDownClass(cls):
        fast_api__service__registry.configs.clear()
        fast_api__service__registry.configs.update(cls.original_configs)

    def test__multiple_client_instances__all_work(self):                        # Multiple clients all work
        client_1 = Cache__Service__Client()
        client_2 = Cache__Service__Client()
        client_3 = Cache__Service__Client()

        assert client_1.health() is True
        assert client_2.health() is True
        assert client_3.health() is True

    def test__multiple_client_instances__same_config(self):                     # All get same config from registry
        client_1 = Cache__Service__Client()
        client_2 = Cache__Service__Client()

        config_1 = client_1.requests().config()
        config_2 = client_2.requests().config()

        assert config_1 is config_2                                             # Same config object

    def test__client_created_inline(self):                                      # Client can be created on the fly
        def some_business_logic():
            client = Cache__Service__Client()                                   # Create inline
            return client.info().health()

        result = some_business_logic()
        assert result.get('status') == 'ok'

    def test__client_in_loop(self):                                             # Client works in loops
        for _ in range(5):
            client = Cache__Service__Client()
            assert client.health() is True
