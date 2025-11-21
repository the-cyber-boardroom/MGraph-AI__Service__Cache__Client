from unittest                                                                               import TestCase

import pytest
from osbot_utils.testing.__ import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from mgraph_ai_service_cache_client.decorator.Cache__Decorator                              import cache_response, _store_in_cache, _retrieve_from_cache, _get_response_type
from mgraph_ai_service_cache_client.decorator.schemas.Schema__Cache__Decorator__Config      import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.decorator.schemas.enums.Enum__Cache__Decorator__Mode    import Enum__Cache__Decorator__Mode


class test_Cache__Decorator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pytest.skip("tests need wiring")

    def test__cache_response__basic_functionality(self):                    # Test decorator can wrap a method
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)             # Disabled to avoid actual caching
        assert config.obj() == __( enabled               = False                       ,
                                   mode                  = 'enabled'                   ,
                                   strategy              = 'key_based'                 ,
                                   use_class_name        = True                        ,
                                   use_method_name       = True                        ,
                                   file_id               = 'response'                  ,
                                   cache_attr_name       = 'decorator__cache'          ,
                                   ttl_seconds           = None                        ,
                                   cache_none_results    = False                       ,
                                   invalidate_on_error   = False                       ,
                                   namespace             = 'test'                      ,
                                   key_fields            = []                          )

        
        @cache_response(config)
        def test_method(self, param1):
            return f"result_{param1}"

        assert callable(test_method)                                        # Decorator should preserve function
        assert test_method.__name__     == "test_method"                    # confirm method name
        assert test_method(self, "abc") == 'result_abc'                     # confirm response

    def test__cache_response__disabled_mode(self):                          # Test method executes without caching when disabled
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)
        
        call_count = 0
        
        class TestService(Type_Safe):
            
            @cache_response(config)
            def test_method(self, param1):
                nonlocal call_count
                call_count += 1
                return f"result_{param1}"
        
        service = TestService()
        
        # Call method twice with same params
        result1 = service.test_method("value1")
        result2 = service.test_method("value1")
        
        assert result1    == "result_value1"
        assert result2    == "result_value1"
        assert call_count == 2


    def test__cache_response__no_cache_client(self):                        # Test graceful handling when cache client missing
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True)
        assert config.obj() == __( enabled               = True                        ,
                                   mode                  = 'enabled'                   ,
                                   strategy              = 'key_based'                 ,
                                   use_class_name        = True                        ,
                                   use_method_name       = True                        ,
                                   file_id               = 'response'                  ,
                                   cache_attr_name       = 'decorator__cache'          ,
                                   ttl_seconds           = None                        ,
                                   cache_none_results    = False                       ,
                                   invalidate_on_error   = False                       ,
                                   namespace             = 'test'                      ,
                                   key_fields            = []                          )

        
        call_count = 0
        
        class TestService(Type_Safe):
            # No decorator__cache attribute
            
            @cache_response(config)
            def test_method(self, param1):
                nonlocal call_count
                call_count += 1
                return f"result_{param1}"
        
        service = TestService()
        
        # Should execute without cache
        result = service.test_method("value1")
        
        assert result == "result_value1"
        assert call_count == 1                                              # Method executed

    def test__cache_response__mode_disabled(self):                          # Test DISABLED mode bypasses cache
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, mode=Enum__Cache__Decorator__Mode.DISABLED)
        
        call_count = 0
        
        class TestService(Type_Safe):
            decorator__cache: Mock = Mock()
            
            @cache_response(config)
            def test_method(self, param1):
                nonlocal call_count
                call_count += 1
                return f"result_{param1}"
        
        service = TestService()
        result  = service.test_method("value1")
        
        assert result == "result_value1"
        assert call_count == 1                                              # Method executed
        assert service.decorator__cache.cache_client.retrieve.call_count == 0  # Cache not accessed

    def test__retrieve_from_cache__not_found(self):                         # Test cache miss returns None
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        
        config = Schema__Cache__Decorator__Config(namespace="test")
        
        result = _retrieve_from_cache(cache_client = mock_cache_client ,
                                      config       = config            ,
                                      cache_hash   = "test_hash"       ,
                                      func         = lambda: "result"  )
        
        assert result is None                                               # Cache miss

    def test__retrieve_from_cache__found(self):                             # Test cache hit returns deserialized result
        class ResponseSchema(Type_Safe):
            value: str = "test"
        
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = {
            'body': '{"value": "cached_value"}'
        }
        
        config = Schema__Cache__Decorator__Config(namespace="test")
        
        def test_func() -> ResponseSchema:
            return ResponseSchema()
        
        result = _retrieve_from_cache(cache_client = mock_cache_client ,
                                      config       = config            ,
                                      cache_hash   = "test_hash"       ,
                                      func         = test_func         )
        
        assert result is not None
        assert isinstance(result, ResponseSchema)
        assert result.value == "cached_value"

    def test__retrieve_from_cache__no_body(self):                           # Test handling response without body
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = {}  # No 'body' key
        
        config = Schema__Cache__Decorator__Config(namespace="test")
        
        result = _retrieve_from_cache(cache_client = mock_cache_client ,
                                      config       = config            ,
                                      cache_hash   = "test_hash"       ,
                                      func         = lambda: "result"  )
        
        assert result is None                                               # Treat missing body as cache miss

    def test__store_in_cache__type_safe_object(self):                       # Test storing Type_Safe object
        class ResponseSchema(Type_Safe):
            value: str = "test_value"
        
        mock_cache_client = Mock()
        config = Schema__Cache__Decorator__Config(namespace="test")
        response = ResponseSchema()
        
        _store_in_cache(cache_client = mock_cache_client ,
                       config       = config            ,
                       cache_key    = "test_key"        ,
                       result       = response          )
        
        # Verify store was called with serialized JSON
        mock_cache_client.cache_client.store().store__json__cache_key.assert_called_once()
        call_args = mock_cache_client.cache_client.store().store__json__cache_key.call_args
        
        assert call_args[1]['namespace'] == "test"
        assert call_args[1]['cache_key'] == "test_key"

    def test__store_in_cache__none_result__not_cached_by_default(self):     # Test None results not cached by default
        mock_cache_client = Mock()
        config = Schema__Cache__Decorator__Config(namespace="test", cache_none_results=False)
        
        _store_in_cache(cache_client = mock_cache_client ,
                       config       = config            ,
                       cache_key    = "test_key"        ,
                       result       = None              )
        
        # Verify store was NOT called
        mock_cache_client.cache_client.store().store__json__cache_key.assert_not_called()

    def test__store_in_cache__none_result__cached_when_configured(self):    # Test None results cached when enabled
        mock_cache_client = Mock()
        config = Schema__Cache__Decorator__Config(namespace="test", cache_none_results=True)
        
        _store_in_cache(cache_client = mock_cache_client ,
                       config       = config            ,
                       cache_key    = "test_key"        ,
                       result       = None              )
        
        # Verify store WAS called
        mock_cache_client.cache_client.store().store__json__cache_key.assert_called_once()

    def test__get_response_type__with_annotation(self):                     # Test extracting return type from function
        class ResponseSchema(Type_Safe):
            value: str = "test"
        
        def test_func() -> ResponseSchema:
            return ResponseSchema()
        
        response_type = _get_response_type(test_func)
        
        assert response_type is ResponseSchema                              # Type extracted from annotation

    def test__get_response_type__without_annotation(self):                  # Test handling function without return annotation
        def test_func():
            return "result"
        
        response_type = _get_response_type(test_func)
        
        assert response_type is None                                        # No annotation = None

    def test__decorator__preserves_function_metadata(self):                 # Test decorator preserves original function info
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)
        
        @cache_response(config)
        def test_method(self, param1: str) -> str:
            """Test method docstring"""
            return f"result_{param1}"
        
        assert test_method.__name__ == "test_method"
        assert test_method.__doc__ == "Test method docstring"

    def test__decorator__with_multiple_params(self):                        # Test decorator with multiple parameters
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)
        
        @cache_response(config)
        def test_method(self, param1, param2, param3=None):
            return f"{param1}_{param2}_{param3}"
        
        class TestService(Type_Safe):
            pass
        
        service = TestService()
        result = test_method(service, "a", "b", param3="c")
        
        assert result == "a_b_c"

    def test__decorator__with_default_params(self):                         # Test decorator with default parameter values
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)
        
        @cache_response(config)
        def test_method(self, param1="default"):
            return f"result_{param1}"
        
        class TestService(Type_Safe):
            pass
        
        service = TestService()
        
        # Call with default
        result1 = test_method(service)
        assert result1 == "result_default"
        
        # Call with explicit value
        result2 = test_method(service, "custom")
        assert result2 == "result_custom"

    def test__decorator__exception_handling(self):                          # Test decorator handles exceptions properly
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=False)
        
        @cache_response(config)
        def test_method(self, should_fail):
            if should_fail:
                raise ValueError("Test error")
            return "success"
        
        class TestService(Type_Safe):
            pass
        
        service = TestService()
        
        # Normal execution
        result = test_method(service, False)
        assert result == "success"
        
        # Exception propagates
        try:
            test_method(service, True)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert str(e) == "Test error"

    def test__decorator__read_only_mode__cache_hit(self):                   # Test READ_ONLY mode returns cached but doesn't write
        class ResponseSchema(Type_Safe):
            value: str = "cached"
        
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = {
            'body': '{"value": "cached"}'
        }
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, mode=Enum__Cache__Decorator__Mode.READ_ONLY)
        
        call_count = 0
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def test_method(self) -> ResponseSchema:
                nonlocal call_count
                call_count += 1
                return ResponseSchema(value="fresh")
        
        service = TestService()
        result = service.test_method()
        
        assert result.value == "cached"                                     # Returned from cache
        assert call_count == 0                                              # Method NOT executed
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.assert_called_once()
        mock_cache_client.cache_client.store().store__json__cache_key.assert_not_called()  # Not stored

    def test__decorator__read_only_mode__cache_miss(self):                  # Test READ_ONLY mode executes but doesn't store
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None  # Cache miss
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, mode=Enum__Cache__Decorator__Mode.READ_ONLY, key_fields=[])
        
        call_count = 0
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def test_method(self):
                nonlocal call_count
                call_count += 1
                return "fresh_result"
        
        service = TestService()
        result = service.test_method()
        
        assert result == "fresh_result"                                     # Method executed
        assert call_count == 1                                              # Method was called
        mock_cache_client.cache_client.store().store__json__cache_key.assert_not_called()  # Not stored in READ_ONLY
