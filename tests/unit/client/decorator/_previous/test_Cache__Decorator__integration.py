from unittest                                                                                      import TestCase
from unittest.mock                                                                                 import Mock, MagicMock
from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe
from mgraph_ai_service_cache_client.client.decorator.Cache__Decorator                              import cache_response
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config      import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.decorator.schemas.enums.Enum__Cache__Decorator__Mode    import Enum__Cache__Decorator__Mode


class test_Cache__Decorator__integration(TestCase):                                    # Integration tests for complete cache system

    def test__multiple_methods__separate_cache_keys(self):                  # Test multiple methods generate different cache keys
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, key_fields=["value"])
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def method1(self, value: str) -> str:
                return f"method1_{value}"
            
            @cache_response(config)
            def method2(self, value: str) -> str:
                return f"method2_{value}"
        
        service = TestService()
        
        # Call both methods with same param
        result1 = service.method1("test")
        result2 = service.method2("test")
        
        assert result1 == "method1_test"
        assert result2 == "method2_test"
        
        # Both methods should have checked cache
        assert mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.call_count == 2

    def test__exception_handling_with_invalidate(self):                     # Test cache invalidation on error
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        mock_delete = MagicMock()
        mock_cache_client.cache_client.delete.return_value = mock_delete
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, invalidate_on_error=True, key_fields=[])
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def failing_method(self):
                raise ValueError("Test error")
        
        service = TestService()
        
        # Method should raise exception
        try:
            service.failing_method()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert str(e) == "Test error"
        
        # Cache should be invalidated
        mock_delete.delete__hash__cache_hash.assert_called_once()

    def test__different_params__different_cache_keys(self):                 # Test different parameters generate different cache entries
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, key_fields=["param1"])
        
        call_count = 0
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def process(self, param1: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{param1}"
        
        service = TestService()
        
        # Call with different params
        result1 = service.process("value1")
        result2 = service.process("value2")
        result3 = service.process("value1")  # Same as first call
        
        assert result1 == "result_value1"
        assert result2 == "result_value2"
        assert result3 == "result_value1"
        assert call_count == 3                                              # All three called (no cache hits in this test)

    def test__nested_type_safe_objects(self):                               # Test caching with nested Type_Safe structures
        class InnerSchema(Type_Safe):
            inner_field: str = "inner"
        
        class OuterSchema(Type_Safe):
            outer_field: str = "outer"
            inner: InnerSchema
        
        class ResponseSchema(Type_Safe):
            message: str = "response"
        
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, key_fields=["request"])
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def process(self, request: OuterSchema) -> ResponseSchema:
                return ResponseSchema(message=f"{request.outer_field}_{request.inner.inner_field}")
        
        service = TestService()
        request = OuterSchema(outer_field="test", inner=InnerSchema(inner_field="nested"))
        
        result = service.process(request)
        
        assert result.message == "test_nested"
        
        # Verify store was called with proper serialization
        mock_cache_client.cache_client.store().store__json__cache_key.assert_called_once()

    def test__cache_config_per_method(self):                                # Test different cache configs for different methods
        mock_cache_client = Mock()
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.return_value = None
        
        config1 = Schema__Cache__Decorator__Config(namespace="namespace1", enabled=True, key_fields=["param"])
        config2 = Schema__Cache__Decorator__Config(namespace="namespace2", enabled=True, key_fields=["param"])
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config1)
            def method1(self, param: str) -> str:
                return f"method1_{param}"
            
            @cache_response(config2)
            def method2(self, param: str) -> str:
                return f"method2_{param}"
        
        service = TestService()
        
        result1 = service.method1("test")
        result2 = service.method2("test")
        
        assert result1 == "method1_test"
        assert result2 == "method2_test"
        
        # Verify both methods stored to their respective namespaces
        store_calls = mock_cache_client.cache_client.store().store__json__cache_key.call_args_list
        assert len(store_calls) == 2
        assert store_calls[0][1]['namespace'] == "namespace1"
        assert store_calls[1][1]['namespace'] == "namespace2"

    def test__service_without_cache_attribute(self):                        # Test service works without cache attribute
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True)
        
        class TestService(Type_Safe):
            # No decorator__cache attribute
            
            @cache_response(config)
            def process(self, value: str) -> str:
                return f"result_{value}"
        
        service = TestService()
        result = service.process("test")
        
        assert result == "result_test"                                      # Method executes normally

    def test__read_only_mode__full_flow(self):                              # Test READ_ONLY mode complete behavior
        mock_cache_client = Mock()
        
        # Simulate cache miss then cache hit
        mock_cache_client.cache_client.retrieve().retrieve__hash__cache_hash.side_effect = [
            None,  # First call: miss
            None   # Second call: still miss (READ_ONLY never stores)
        ]
        
        config = Schema__Cache__Decorator__Config(namespace="test", enabled=True, mode=Enum__Cache__Decorator__Mode.READ_ONLY, key_fields=[])
        
        call_count = 0
        
        class TestService(Type_Safe):
            decorator__cache = mock_cache_client
            
            @cache_response(config)
            def process(self) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"
        
        service = TestService()
        
        # Both calls should execute (no storing in READ_ONLY)
        result1 = service.process()
        result2 = service.process()
        
        assert result1 == "result_1"
        assert result2 == "result_2"
        assert call_count == 2                                              # Both executed
        
        # Verify store was never called
        mock_cache_client.cache_client.store().store__json__cache_key.assert_not_called()
