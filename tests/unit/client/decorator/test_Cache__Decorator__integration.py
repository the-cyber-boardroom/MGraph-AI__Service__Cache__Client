from unittest                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Env                                                                          import in_github_action
from osbot_utils.utils.Misc                                                                         import random_string
from mgraph_ai_service_cache_client.client.decorator.Cache__Decorator                               import cache_response, disable_cache_for_method, get_cache_config, is_cache_decorated
from mgraph_ai_service_cache_client.client.decorator.Decorator__Cache                               import Decorator__Cache
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config       import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.decorator.schemas.enums.Enum__Cache__Decorator__Mode     import Enum__Cache__Decorator__Mode
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy                import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                   import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                import Enum__Client__Mode
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                       import Cache_Service__Fast_API
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                import Serverless__Fast_API__Config


class test_Cache__Decorator__integration(TestCase):             # Integration tests for Cache__Decorator using real in-memory cache service

    @classmethod
    def setUpClass(cls):
        """Set up in-memory cache service for all tests"""
        # Create in-memory cache service
        serverless_config = Serverless__Fast_API__Config(enable_api_key=False)
        cache_service__fast_api = Cache_Service__Fast_API(config=serverless_config).setup()
        cls.fast_api_app = cache_service__fast_api.app()
        cls.cache_service = cache_service__fast_api.cache_service
        
        # Create client config for in-memory mode
        client_config = Cache__Service__Fast_API__Client__Config(
            mode         = Enum__Client__Mode.IN_MEMORY,
            fast_api_app = cls.fast_api_app,
            service_name = "test-decorator"
        )
        
        # Create cache client
        cls.client_cache_service = Client__Cache__Service(config=client_config)
        
        # Create Decorator__Cache instance for services
        cls.decorator_cache = Decorator__Cache(
            client_cache_service = cls.client_cache_service
        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Basic Cache Decorator Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_cache_decorator__basic_caching(self):
        """Test basic caching functionality with real cache service"""
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(namespace  = f"test-basic-{random_string()}",
                                                  enabled    = True         ,
                                                  key_fields = ["value"]    )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{value}_{call_count}"
        
        service = TestService()

        result1 = service.process("test")                           # First call - should execute
        assert result1    == "result_test_1"
        assert call_count == 1

        result2 = service.process("test")                           # Second call with same params - should hit cache
        assert result2 == "result_test_1"                           # Same result from cache
        assert call_count == 1                                      # Method not executed again

        result3 = service.process("different")                      # Third call with different params - should execute
        assert result3 == "result_different_2"
        assert call_count == 2

    def test_cache_decorator__type_safe_objects(self):
        """Test caching with Type_Safe request/response objects"""
        
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(
            namespace  = f"test-typesafe-{random_string()}",
            enabled    = True,
            key_fields = ["request"]
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def transform(self, request: RequestSchema) -> ResponseSchema_2:
                nonlocal call_count
                call_count += 1
                return ResponseSchema_2(message = f"{request.field1}_{request.field2}_{call_count}")
        
        service = TestService()
        request = RequestSchema(field1="test", field2=42)
        
        # First call
        result1 = service.transform(request)
        assert isinstance(result1, ResponseSchema_2)
        assert result1.message == "test_42_1"
        assert result1.processed is True
        assert call_count == 1
        
        # Second call - cached
        result2 = service.transform(request)
        assert isinstance(result2, ResponseSchema_2)
        assert result2.message == "test_42_1"  # Same from cache
        assert call_count == 1
        
        # Different request
        request2 = RequestSchema(field1="test", field2=100)
        result3 = service.transform(request2)
        assert result3.message == "test_100_2"
        assert call_count == 2

    def test_cache_decorator__disabled_mode(self):
        """Test that caching is bypassed when disabled"""
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(
            namespace = "test-disabled",
            enabled   = False,  # Disabled
            key_fields = ["value"]
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"
        
        service = TestService()
        
        # Multiple calls should all execute
        result1 = service.process("test")
        result2 = service.process("test")
        result3 = service.process("test")
        
        assert result1 == "result_1"
        assert result2 == "result_2"
        assert result3 == "result_3"
        assert call_count == 3

    def test_cache_decorator__read_only_mode(self):
        """Test READ_ONLY mode - reads but doesn't write"""
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(
            namespace = f"test-readonly-{random_string()}",
            enabled   = True,
            mode      = Enum__Cache__Decorator__Mode.READ_ONLY,
            key_fields = ["value"]
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"
        
        service = TestService()
        
        # Multiple calls should all execute (no storing)
        result1 = service.process("test")
        result2 = service.process("test")
        
        assert result1 == "result_1"
        assert result2 == "result_2"
        assert call_count == 2  # Both executed

    # ═══════════════════════════════════════════════════════════════════════════════
    # Multiple Methods Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_multiple_methods__separate_cache_keys(self):
        """Test that different methods get separate cache entries"""
        namespace = f"test-methods-{random_string()}"
        
        config = Schema__Cache__Decorator__Config(
            namespace  = namespace,
            enabled    = True,
            key_fields = ["value"]
        )
        
        method1_count = 0
        method2_count = 0
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def method1(self, value: str) -> str:
                nonlocal method1_count
                method1_count += 1
                return f"method1_{value}_{method1_count}"
            
            @cache_response(config)
            def method2(self, value: str) -> str:
                nonlocal method2_count
                method2_count += 1
                return f"method2_{value}_{method2_count}"
        
        service = TestService()
        
        # Call both methods with same param
        result1_1 = service.method1("test")
        result2_1 = service.method2("test")
        
        assert result1_1 == "method1_test_1"
        assert result2_1 == "method2_test_1"
        
        # Call again - should hit separate caches
        result1_2 = service.method1("test")
        result2_2 = service.method2("test")
        
        assert result1_2 == "method1_test_1"  # Cached
        assert result2_2 == "method2_test_1"  # Cached
        
        assert method1_count == 1
        assert method2_count == 1

    def test_different_configs_per_method(self):
        """Test different cache configurations for different methods"""
        namespace1 = f"namespace1-{random_string()}"
        namespace2 = f"namespace2-{random_string()}"
        
        config1 = Schema__Cache__Decorator__Config(
            namespace       = namespace1,
            strategy        = Enum__Cache__Store__Strategy.DIRECT,
            key_fields      = ["param"],
            use_class_name  = True,
            use_method_name = True
        )
        
        config2 = Schema__Cache__Decorator__Config(
            namespace       = namespace2,
            strategy        = Enum__Cache__Store__Strategy.KEY_BASED,
            key_fields      = ["param"],
            use_class_name  = False,  # Different
            use_method_name = True
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config1)
            def method1(self, param: str) -> str:
                return f"method1_{param}"
            
            @cache_response(config2)
            def method2(self, param: str) -> str:
                return f"method2_{param}"
        
        service = TestService()
        
        # Call both methods
        result1 = service.method1("test")
        result2 = service.method2("test")
        
        assert result1 == "method1_test"
        assert result2 == "method2_test"

        # todo: add internals check to confirm files were created correctly

    # ═══════════════════════════════════════════════════════════════════════════════
    # Exception Handling Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_exception_handling_with_invalidate(self):
        """Test cache invalidation on error with real cache"""
        namespace = f"test-exception-{random_string()}"
        
        config = Schema__Cache__Decorator__Config(namespace           = namespace,
                                                  enabled             = True,
                                                  key_fields          = ["value"])
        
        fail_next = True
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def maybe_failing_method(self, value: str) -> str:
                nonlocal fail_next
                if fail_next:
                    fail_next = False
                    raise ValueError("Test error")
                return f"success_{value}"
        
        service = TestService()
        
        # First call should fail
        with self.assertRaises(ValueError) as context:
            service.maybe_failing_method("test")
        assert str(context.exception) == "Test error"
        
        # Second call should succeed
        result = service.maybe_failing_method("test")
        assert result == "success_test"
        
        # Third call should be cached
        fail_next = True  # Would fail if executed
        result2 = service.maybe_failing_method("test")
        assert result2 == "success_test"  # From cache, not executed

    def test_exception_handling_without_invalidate(self):
        config = Schema__Cache__Decorator__Config(
            namespace           = f"test-no-invalidate-{random_string()}",
            enabled             = True,
            key_fields          = []
        )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def failing_method(self) -> str:
                raise ValueError("Always fails")

        service = TestService()

        # Should raise exception and not affect cache
        with self.assertRaises(ValueError):
            service.failing_method()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Key Fields Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_key_fields__only_specified_fields_matter(self):
        """Test that only specified key_fields affect cache key"""
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(
            namespace  = f"test-keyfields-{random_string()}",
            enabled    = True,
            key_fields = ["important"]  # Only this matters
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process(self, important: str, ignored: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"{important}_{ignored}_{call_count}"
        
        service = TestService()
        
        # First call
        result1 = service.process("value1", "ignored1")
        assert result1 == "value1_ignored1_1"
        assert call_count == 1
        
        # Same important, different ignored - should hit cache
        result2 = service.process("value1", "ignored2")
        assert result2 == "value1_ignored1_1"  # Same cached result
        assert call_count == 1
        
        # Different important - should execute
        result3 = service.process("value2", "ignored1")
        assert result3 == "value2_ignored1_2"
        assert call_count == 2

    def test_empty_key_fields(self):        # Test with empty key_fields (cache based on class/method only)"""
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(namespace  = f"test-empty-keys-{random_string()}",
                                                  enabled    = True ,
                                                  key_fields = []   ) # No parameter-based caching (means we will use all fields)
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process(self, param1: str, param2: int) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"
        
        service = TestService()
        
        # Multiple calls with different params should create new entries (unless called with same params
        result1         = service.process("a", 1)
        result1_cached  = service.process("a", 1)
        result2         = service.process("b", 2)
        result2_cached  = service.process("b", 2)
        result3         = service.process("c", 3)
        result3_cached  = service.process("c", 3)
        
        assert result1        == "result_1"
        assert result1_cached == "result_1"  # Same cached result
        assert result2        == "result_2"
        assert result2_cached == "result_2"  # Same cached result
        assert result3        == "result_3"
        assert result3_cached == "result_3"  # Same cached result

        assert call_count == 3

    # ═══════════════════════════════════════════════════════════════════════════════
    # Service Without Cache Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_service_without_cache_attribute(self):
        """Test that decorator works gracefully when service has no cache"""
        config = Schema__Cache__Decorator__Config(
            namespace = "test-no-cache",
            enabled   = True
        )
        
        call_count = 0
        
        class TestService(Type_Safe):
            # No decorator__cache attribute
            
            @cache_response(config)
            def process(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{value}_{call_count}"
        
        service = TestService()
        
        # Should execute normally without caching
        result1 = service.process("test")
        result2 = service.process("test")
        
        assert result1 == "result_test_1"
        assert result2 == "result_test_2"
        assert call_count == 2

    def test_legacy_client_cache_service(self):
        """Test backward compatibility with Client__Cache__Service directly"""
        config = Schema__Cache__Decorator__Config(
            namespace  = f"test-legacy-{random_string()}",
            enabled    = True,
            key_fields = ["value"]
        )
        
        call_count = 0
        
        class TestService(Type_Safe):
            # Use Client__Cache__Service directly (legacy)
            decorator__cache = self.client_cache_service
            
            @cache_response(config)
            def process(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"
        
        service = TestService()
        
        # Should work with legacy client
        result1 = service.process("test")
        result2 = service.process("test")
        
        assert result1 == "result_1"
        assert result2 == "result_1"  # Cached
        assert call_count == 1

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_get_cache_config(self):
        """Test getting cache config from decorated method"""
        config = Schema__Cache__Decorator__Config(
            namespace = "test-config",
            enabled   = True
        )
        
        class TestService(Type_Safe):
            @cache_response(config)
            def cached_method(self):
                pass
            
            def uncached_method(self):
                pass
        
        service = TestService()
        
        # Get config from cached method
        retrieved_config = get_cache_config(service.cached_method)
        assert retrieved_config is config
        
        # Get config from uncached method
        uncached_config = get_cache_config(service.uncached_method)
        assert uncached_config is None

    def test_is_cache_decorated(self):
        """Test checking if method is cache decorated"""
        config = Schema__Cache__Decorator__Config(namespace="test")
        
        class TestService(Type_Safe):
            @cache_response(config)
            def cached_method(self):
                pass
            
            def uncached_method(self):
                pass
        
        service = TestService()
        
        assert is_cache_decorated(service.cached_method) is True
        assert is_cache_decorated(service.uncached_method) is False

    def test_disable_cache_for_method(self):
        """Test disabling cache for a specific method"""
        config = Schema__Cache__Decorator__Config(namespace="test")
        
        @disable_cache_for_method
        @cache_response(config)
        def test_method():
            return "test"
        
        # Method should be marked as disabled
        assert hasattr(test_method, '_cache_enabled')
        assert test_method._cache_enabled is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Complex Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_nested_type_safe_objects_full_flow(self):
        """Test complete flow with nested Type_Safe objects"""
        
        call_count = 0
        
        config = Schema__Cache__Decorator__Config(
            namespace  = f"test-nested-{random_string()}",
            enabled    = True,
            key_fields = ["request"]
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def process_nested(self, request: OuterSchema) -> ResponseSchema_1:
                nonlocal call_count
                call_count += 1
                total = sum(request.list_data) + request.inner.inner_value
                return ResponseSchema_1(message         = f"{request.outer_field}_{call_count}",
                                        processed_inner = request.inner.inner_field.upper(),
                                        total           = total)
        
        service = TestService()
        
        request = OuterSchema(
            outer_field = "test",
            inner       = InnerSchema(inner_field="nested", inner_value=10),
            list_data   = [1, 2, 3]
        )
        
        # First call
        result1 = service.process_nested(request)
        assert isinstance(result1, ResponseSchema_1)
        assert result1.message == "test_1"
        assert result1.processed_inner == "NESTED"
        assert result1.total == 16
        assert call_count == 1
        
        # Second call - cached
        result2 = service.process_nested(request)
        assert result2.message == "test_1"  # Same
        assert result2.total == 16
        assert call_count == 1
        
        # Modify request slightly
        request2 = OuterSchema(
            outer_field = "test",
            inner       = InnerSchema(inner_field="different", inner_value=10),
            list_data   = [1, 2, 3]
        )
        
        result3 = service.process_nested(request2)
        assert result3.message == "test_2"
        assert result3.processed_inner == "DIFFERENT"
        assert call_count == 2


    def test_performance_with_real_cache(self):
        """Test that caching actually improves performance"""
        import time
        
        config = Schema__Cache__Decorator__Config(
            namespace  = f"test-performance-{random_string()}",
            enabled    = True,
            key_fields = ["value"]
        )
        
        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache
            
            @cache_response(config)
            def expensive_operation(self, value: str) -> str:
                # Simulate expensive operation
                time.sleep(0.01)  # 10ms
                return f"result_{value}"
        
        service = TestService()
        
        # First call - slow
        start1 = time.time()
        result1 = service.expensive_operation("test")
        time1 = time.time() - start1
        
        # Second call - fast (cached)
        start2 = time.time()
        result2 = service.expensive_operation("test")
        time2 = time.time() - start2
        
        assert result1 == result2
        assert time1 > 0.01  # At least 10ms
        if in_github_action():
            assert time2 < 0.05    # Much faster (but slower than locally)
        else:
            assert time2 < 0.008  # Much faster (cache hit)


# classes used in this project

class InnerSchema(Type_Safe):
    inner_field: str
    inner_value: int

class OuterSchema(Type_Safe):
    outer_field: str
    inner: InnerSchema
    list_data: list

class ResponseSchema_1(Type_Safe):
    message: str
    processed_inner: str = None
    total: int

class RequestSchema(Type_Safe):
    field1: str
    field2: int

class ResponseSchema_2(Type_Safe):
    message: str
    processed: bool = True