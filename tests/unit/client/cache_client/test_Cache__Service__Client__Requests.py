# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Service__Client__Requests
# Tests for Cache service transport layer
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                          import Cache__Service__Client
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client__Requests                import Cache__Service__Client__Requests
from osbot_fast_api.services.registry.Fast_API__Client__Requests                                        import Fast_API__Client__Requests
from osbot_utils.utils.Objects                                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe


class test_Cache__Service__Client__Requests(TestCase):

    def test__init__(self):                                                     # Test auto-initialization
        with Cache__Service__Client__Requests() as _:
            assert type(_)         is Cache__Service__Client__Requests
            assert base_classes(_) == [Fast_API__Client__Requests, Type_Safe, object]

    def test__inherits_from_Fast_API__Client__Requests(self):                   # Test inheritance
        requests = Cache__Service__Client__Requests()
        assert isinstance(requests, Fast_API__Client__Requests)

    def test__service_type__default_is_none(self):                              # Test default service_type
        with Cache__Service__Client__Requests() as _:
            assert _.service_type is None

    def test__service_type__can_be_set(self):                                   # Test service_type assignment
        with Cache__Service__Client__Requests() as _:
            _.service_type = Cache__Service__Client
            assert _.service_type is Cache__Service__Client

    def test__config__raises_when_not_registered(self):                         # Test error when not registered
        requests              = Cache__Service__Client__Requests()
        requests.service_type = Cache__Service__Client

        with self.assertRaises(ValueError) as context:
            requests.config()

        assert "Cache__Service__Client not registered" in str(context.exception)
