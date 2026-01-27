# ═══════════════════════════════════════════════════════════════════════════════
# test_register_cache_service
# Tests for Cache service registration helpers
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                          import Cache__Service__Client
from mgraph_ai_service_cache_client.client.cache_service.register_cache_service                         import register_cache_service__in_memory, register_cache_service__remote, register_cache_service__from_env
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                       import Fast_API__Service__Registry
from osbot_fast_api.services.schemas.registry.enums.Enum__Fast_API__Service__Registry__Client__Mode     import Enum__Fast_API__Service__Registry__Client__Mode
from osbot_utils.utils.Env                                                                              import set_env, del_env
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                                 import ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                                 import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                                 import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE


# ═══════════════════════════════════════════════════════════════════════════════
# register_cache_service__in_memory Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_register_cache_service__in_memory(TestCase):

    def test__registers_config(self):                                           # Test config is registered
        registry = Fast_API__Service__Registry()

        register_cache_service__in_memory(registry=registry)

        assert registry.is_registered(Cache__Service__Client) is True

    def test__config__mode_is_in_memory(self):                                  # Test mode is IN_MEMORY
        registry = Fast_API__Service__Registry()

        register_cache_service__in_memory(registry=registry)

        config = registry.config(Cache__Service__Client)
        assert config.mode == Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY

    def test__config__has_fast_api_app(self):                                   # Test config has FastAPI app
        registry = Fast_API__Service__Registry()

        register_cache_service__in_memory(registry=registry)

        config = registry.config(Cache__Service__Client)
        assert config.fast_api_app is not None

    def test__config__no_base_url(self):                                        # Test no base_url in IN_MEMORY
        registry = Fast_API__Service__Registry()

        register_cache_service__in_memory(registry=registry)

        config = registry.config(Cache__Service__Client)
        assert config.base_url is None or str(config.base_url) == ''


    # ═══════════════════════════════════════════════════════════════════════════════
    # register_cache_service__remote Tests
    # ═══════════════════════════════════════════════════════════════════════════════


    def test__registers_with_explicit_values(self):                             # Test explicit registration
        registry = Fast_API__Service__Registry()

        register_cache_service__remote(registry      = registry                    ,
                                       base_url      = 'https://cache.example.com' ,
                                       api_key_name  = 'X-API-KEY'                 ,
                                       api_key_value = 'secret-123'                )

        assert registry.is_registered(Cache__Service__Client) is True

    def test__config__mode_is_remote(self):                                     # Test mode is REMOTE
        registry = Fast_API__Service__Registry()

        register_cache_service__remote(registry = registry                    ,
                                       base_url = 'https://cache.example.com' )

        config = registry.config(Cache__Service__Client)
        assert config.mode == Enum__Fast_API__Service__Registry__Client__Mode.REMOTE

    def test__config__has_base_url(self):                                       # Test base_url is set
        registry = Fast_API__Service__Registry()

        register_cache_service__remote(registry = registry                    ,
                                       base_url = 'https://cache.example.com' )

        config = registry.config(Cache__Service__Client)
        assert str(config.base_url) == 'https://cache.example.com'

    def test__config__has_api_key(self):                                        # Test API key is set
        registry = Fast_API__Service__Registry()

        register_cache_service__remote(registry      = registry                    ,
                                       base_url      = 'https://cache.example.com' ,
                                       api_key_name  = 'X-API-KEY'                 ,
                                       api_key_value = 'secret-123'                )

        config = registry.config(Cache__Service__Client)
        assert str(config.api_key_name)  == 'x-api-key'
        assert str(config.api_key_value) == 'secret-123'

    def test__config__no_fast_api_app(self):                                    # Test no FastAPI app in REMOTE
        registry = Fast_API__Service__Registry()

        register_cache_service__remote(registry = registry                    ,
                                       base_url = 'https://cache.example.com' )

        config = registry.config(Cache__Service__Client)
        assert config.fast_api_app is None

    def test__raises_without_base_url(self):                                    # Test error without base_url
        registry = Fast_API__Service__Registry()

        with self.assertRaises(ValueError) as context:
            register_cache_service__remote(registry=registry)                   # No base_url

        assert "REMOTE mode requires base_url" in str(context.exception)

    def test__reads_from_env_vars(self):                                        # Test env var fallback
        registry = Fast_API__Service__Registry()

        # Set env vars
        set_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            , 'https://env.example.com')
        set_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME , 'x-env-key'              )
        set_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE, 'env-secret'             )

        try:
            register_cache_service__remote(registry=registry)

            config = registry.config(Cache__Service__Client)
            assert str(config.base_url)      == 'https://env.example.com'
            assert str(config.api_key_name)  == 'x-env-key'
            assert str(config.api_key_value) == 'env-secret'
        finally:
            del_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            )
            del_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME )
            del_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE)


# ═══════════════════════════════════════════════════════════════════════════════
# register_cache_service__from_env Tests
# ═══════════════════════════════════════════════════════════════════════════════

class test_register_cache_service__from_env(TestCase):

    def test__uses_in_memory_when_no_url(self):                                 # Test defaults to IN_MEMORY
        registry = Fast_API__Service__Registry()

        # Ensure env var is not set
        del_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE)

        register_cache_service__from_env(registry=registry)

        config = registry.config(Cache__Service__Client)
        assert config.mode == Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY

    def test__uses_remote_when_url_set(self):                                   # Test uses REMOTE when URL set
        registry = Fast_API__Service__Registry()

        set_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE, 'https://auto.example.com')

        try:
            register_cache_service__from_env(registry=registry)

            config = registry.config(Cache__Service__Client)
            assert config.mode           == Enum__Fast_API__Service__Registry__Client__Mode.REMOTE
            assert str(config.base_url)  == 'https://auto.example.com'
        finally:
            del_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE)
