from unittest                                                                                   import TestCase
from mgraph_ai_service_cache_client.client.Cache__Service__Registry__Client                     import Cache__Service__Registry__Client
from osbot_fast_api.services.schemas.registry.Fast_API__Service__Registry__Client__Config       import Fast_API__Service__Registry__Client__Config
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                         import ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE


class test_Cache__Service__Registry__Client(TestCase):

    def test__init__(self):                                                     # Test auto-initialization
        with Cache__Service__Registry__Client() as _:
            assert type(_)              is Cache__Service__Registry__Client
            assert type(_.config)       is Fast_API__Service__Registry__Client__Config
            assert _.cache_client       is None

    def test__env_vars__returns_expected_vars(self):                            # Test env vars documentation
        env_vars = Cache__Service__Registry__Client.env_vars()

        assert len(env_vars) == 3
        assert env_vars[0].name     == ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE
        assert env_vars[0].required is True
        assert env_vars[1].required is False                                    # API key optional
        assert env_vars[2].required is False

    def test__client_name(self):                                                # Test client name
        assert Cache__Service__Registry__Client.client_name() == 'Cache__Service__Registry__Client'


