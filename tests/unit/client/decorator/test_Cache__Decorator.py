from unittest                                                                                       import TestCase
from typing                                                                                         import Optional
from osbot_utils.testing.__                                                                         import __
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Misc                                                                         import random_string
from mgraph_ai_service_cache_client.client.decorator.Cache__Decorator                               import cache_response, disable_cache_for_method, get_cache_config, is_cache_decorated
from mgraph_ai_service_cache_client.client.decorator.Decorator__Cache                               import Decorator__Cache
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config       import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy                import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.client.decorator.exceptions.Cache__Decorator__Exceptions        import Cache__Invalid__Config
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                   import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                import Enum__Client__Mode
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                       import Cache_Service__Fast_API
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                import Serverless__Fast_API__Config


class test_Cache__Decorator(TestCase):                                                              # Test Cache__Decorator functionality with real cache service

    @classmethod
    def setUpClass(cls):                                                                            # Set up in-memory cache service
        serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)                # Create in-memory cache service
        cache_service__fast_api = Cache_Service__Fast_API(config=serverless_config).setup()
        cls.fast_api_app        = cache_service__fast_api.app()

        client_config            = Cache__Service__Fast_API__Client__Config(mode         = Enum__Client__Mode.IN_MEMORY,    # Create client
                                                                            fast_api_app = cls.fast_api_app            )

        cls.client_cache_service = Client__Cache__Service(config=client_config)
        cls.decorator_cache      = Decorator__Cache(client_cache_service=cls.client_cache_service)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Configuration Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_invalid_config__none(self):                                                            # Test that None config raises appropriate error
        with self.assertRaises(Cache__Invalid__Config) as context:
            @cache_response(None)
            def test_method():
                pass

        assert "Configuration cannot be None" in str(context.exception)

    def test_invalid_config__no_namespace(self):                                                    # Test that missing namespace raises error
        with self.assertRaises(Cache__Invalid__Config) as context:
            config = Schema__Cache__Decorator__Config(namespace=None)

            @cache_response(config)
            def test_method():
                pass

    def test_valid_config__minimal(self):                                                           # Test minimal valid configuration
        config = Schema__Cache__Decorator__Config(namespace="test")

        @cache_response(config)
        def test_method():
            return "test"

        assert hasattr(test_method, '_cache_config')                                                # Should decorate without error
        assert test_method._cache_config == config

    # ═══════════════════════════════════════════════════════════════════════════════
    # Decorator Metadata Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_decorator_adds_metadata(self):                                                         # Test that decorator adds metadata attributes
        config = Schema__Cache__Decorator__Config(namespace="test-metadata")

        @cache_response(config)
        def test_method():
            return "test"

        assert hasattr(test_method, '_cache_config'  )                                              # Check metadata attributes
        assert hasattr(test_method, '_cache_enabled' )
        assert hasattr(test_method, '_original_func' )

        assert test_method._cache_config  == config
        assert test_method._cache_enabled is True
        assert test_method._original_func is not None

    def test_functools_wraps_preserves_attributes(self):                                            # Test that @functools.wraps preserves original function attributes
        config = Schema__Cache__Decorator__Config(namespace="test-wraps")

        def original_function():
            """This is the docstring"""
            return "test"

        original_function.custom_attr = "custom_value"

        decorated = cache_response(config)(original_function)

        assert decorated.__name__    == "original_function"                                         # Original attributes preserved
        assert decorated.__doc__     == "This is the docstring"
        assert decorated.custom_attr == "custom_value"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_disable_cache_for_method(self):                                                        # Test disable_cache_for_method helper
        config = Schema__Cache__Decorator__Config(namespace="test-disable")

        @cache_response(config)
        def test_method():
            return "test"

        assert test_method._cache_enabled is True                                                   # Initially enabled

        disable_cache_for_method(test_method)

        assert test_method._cache_enabled is False                                                  # Now disabled

    def test_get_cache_config(self):                                                                # Test get_cache_config helper
        config = Schema__Cache__Decorator__Config(namespace="test-get-config")

        @cache_response(config)
        def test_method():
            return "test"

        retrieved_config = get_cache_config(test_method)

        assert retrieved_config == config

    def test_get_cache_config__not_decorated(self):                                                 # Test get_cache_config on non-decorated function
        def regular_function():
            return "test"

        retrieved_config = get_cache_config(regular_function)

        assert retrieved_config is None

    def test_is_cache_decorated(self):                                                              # Test is_cache_decorated helper
        config = Schema__Cache__Decorator__Config(namespace="test-is-decorated")

        @cache_response(config)
        def decorated_method():
            return "test"

        def regular_function():
            return "test"

        assert is_cache_decorated(decorated_method)  is True
        assert is_cache_decorated(regular_function)  is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Case Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_method_with_no_arguments(self):                                                        # Test caching method with no arguments except self
        call_count = 0

        config = Schema__Cache__Decorator__Config(namespace  = f"test-no-args-{random_string()}",
                                                  key_fields = []                                )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def no_args_method(self) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{call_count}"

        service = TestService()

        result1 = service.no_args_method()                                                          # Multiple calls should hit cache
        result2 = service.no_args_method()
        result3 = service.no_args_method()

        assert result1    == "result_1"
        assert result2    == "result_1"
        assert result3    == "result_1"
        assert call_count == 1

    def test_method_with_kwargs(self):                                                              # Test caching method called with kwargs
        call_count = 0

        config = Schema__Cache__Decorator__Config(namespace  = f"test-kwargs-{random_string()}",
                                                  key_fields = ["param1", "param2"]             )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def kwargs_method(self, param1: str, param2: int = 10) -> str:
                nonlocal call_count
                call_count += 1
                return f"{param1}_{param2}_{call_count}"

        service = TestService()

        result1 = service.kwargs_method("test", 20)                                                 # Call with positional args
        assert result1 == "test_20_1"

        result2 = service.kwargs_method(param1="test", param2=20)                                   # Call with kwargs - should hit cache
        assert result2    == "test_20_1"
        assert call_count == 1

        result3 = service.kwargs_method("test")                                                     # Call with default value
        assert result3    == "test_10_2"
        assert call_count == 2

    def test_method_with_mixed_args_kwargs(self):                                                   # Test caching with mixed positional and keyword arguments
        call_count = 0

        config = Schema__Cache__Decorator__Config(namespace  = f"test-mixed-{random_string()}",
                                                  key_fields = ["pos1", "kw1"]                  )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def mixed_method(self, pos1, pos2="default", *, kw1, kw2="kwdefault"):
                nonlocal call_count
                call_count += 1
                return f"{pos1}_{pos2}_{kw1}_{kw2}_{call_count}"

        service = TestService()

        result1 = service.mixed_method("a", kw1="b")                                                # First call
        assert result1 == "a_default_b_kwdefault_1"

        result2 = service.mixed_method("a", "different", kw1="b", kw2="different")                  # Same key fields - should hit cache
        assert result2    == "a_default_b_kwdefault_1"
        assert call_count == 1

    def test_non_method_decoration(self):                                                           # Test decorating a regular function (not a method)
        config = Schema__Cache__Decorator__Config(namespace="test-function")

        @cache_response(config)
        def regular_function(param: str) -> str:
            return f"result_{param}"

        result = regular_function("test")                                                           # Should work but without caching (no self)
        assert result == "result_test"

    def test_static_method_decoration(self):                                                        # Test decorating a static method
        config = Schema__Cache__Decorator__Config(namespace="test-static")

        class TestService(Type_Safe):
            @staticmethod
            @cache_response(config)
            def static_method(param: str) -> str:
                return f"static_{param}"

        result = TestService.static_method("test")                                                  # Should work but without caching (no self)
        assert result == "static_test"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Return Type Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_return_type_preservation__string(self):                                                # Test that string return types are preserved
        config = Schema__Cache__Decorator__Config(namespace  = f"test-return-str-{random_string()}",
                                                  key_fields = ["value"]                           )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def string_method(self, value: str) -> str:
                return f"string_{value}"

        service = TestService()

        result1 = service.string_method("test")
        result2 = service.string_method("test")                                                     # Cached

        assert isinstance(result1, str)
        assert isinstance(result2, str)
        assert result1 == result2

    def test_return_type_preservation__dict(self):                                                  # Test that dict return types are preserved
        config = Schema__Cache__Decorator__Config(namespace  = f"test-return-dict-{random_string()}",
                                                  key_fields = ["value"]                            )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def dict_method(self, value: str) -> dict:
                return {"key": value, "number": 42}

        service = TestService()

        result1 = service.dict_method("test")
        result2 = service.dict_method("test")                                                       # Cached

        assert isinstance(result1, dict)
        assert isinstance(result2, dict)
        assert result1 == result2
        assert result1 == {'key': 'test', 'number': 42}

    def test_return_type_preservation__type_safe(self):                                             # Test that Type_Safe return types are preserved

        config = Schema__Cache__Decorator__Config(namespace  = f"test-return-ts-{random_string()}",
                                                  key_fields = ["value"]                          )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def schema_method(self, value: str) -> ResultSchema:
                return ResultSchema(message=value, count=len(value))

        service = TestService()

        result1 = service.schema_method("test")
        result2 = service.schema_method("test")                                                     # Cached

        assert isinstance(result1, ResultSchema)
        assert isinstance(result2, ResultSchema)
        assert result1.message == result2.message
        assert result1.count   == result2.count
        assert result1.message == "test"
        assert result1.count   == 4

    def test_return_type_preservation__optional(self):                                              # Test that Optional return types are handled correctly
        config = Schema__Cache__Decorator__Config(namespace  = f"test-optional-{random_string()}",
                                                  key_fields = ["value"]                         )

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def optional_method(self, value: str) -> Optional[str]:
                if value == "none":
                    return None
                return f"result_{value}"

        service = TestService()

        result1 = service.optional_method("test")                                                   # Test non-None
        result2 = service.optional_method("test")                                                   # Cached
        assert result1 == "result_test"
        assert result2 == "result_test"

        result3 = service.optional_method("none")                                                   # Test None
        result4 = service.optional_method("none")                                                   # Cached
        assert result3 is None
        assert result4 is None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Storage Strategy Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_all_storage_strategies(self):                                                          # Test that all storage strategies work
        strategies = [Enum__Cache__Store__Strategy.DIRECT            ,
                      Enum__Cache__Store__Strategy.TEMPORAL          ,
                      Enum__Cache__Store__Strategy.TEMPORAL_LATEST   ,
                      Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED,
                      Enum__Cache__Store__Strategy.KEY_BASED         ]

        for strategy in strategies:
            config = Schema__Cache__Decorator__Config(namespace  = f"test-{strategy.value}-{random_string()}",
                                                      strategy   = strategy                                  ,
                                                      key_fields = ["value"]                                 )

            call_count = 0

            class TestService(Type_Safe):
                decorator__cache = self.decorator_cache

                @cache_response(config)
                def process(self, value: str) -> str:
                    nonlocal call_count
                    call_count += 1
                    return f"{strategy.value}_{value}_{call_count}"

            service = TestService()

            result1 = service.process("test")                                                       # Test caching works with this strategy
            result2 = service.process("test")

            assert result1    == f"{strategy.value}_test_1"
            assert result2    == f"{strategy.value}_test_1"                                         # Cached
            assert call_count == 1

    # ═══════════════════════════════════════════════════════════════════════════════
    # Class and Method Name Options Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_without_class_name_in_key(self):                                                       # Test cache key generation without class name
        namespace = f"test-no-class-{random_string()}"

        config = Schema__Cache__Decorator__Config(namespace       = namespace,
                                                  use_class_name  = False    ,
                                                  use_method_name = True     ,
                                                  key_fields      = ["value"])

        class Service1(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def method(self, value: str) -> str:
                return f"service1_{value}"

        class Service2(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def method(self, value: str) -> str:
                return f"service2_{value}"

        service1 = Service1()
        service2 = Service2()

        result1 = service1.method("test")                                                           # Both should share cache (no class name differentiation)
        result2 = service2.method("test")                                                           # Should hit cache from Service1

        assert result1 == "service1_test"
        assert result2 == "service1_test"                                                           # Same cached value!

    def test_without_method_name_in_key(self):                                                      # Test cache key generation without method name
        namespace = f"test-no-method-{random_string()}"

        config = Schema__Cache__Decorator__Config(namespace       = namespace,
                                                  use_class_name  = True     ,
                                                  use_method_name = False    ,
                                                  key_fields      = ["value"])

        class TestService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def method1(self, value: str) -> str:
                return f"method1_{value}"

            @cache_response(config)
            def method2(self, value: str) -> str:
                return f"method2_{value}"

        service = TestService()

        result1 = service.method1("test")                                                           # Both methods should share cache (no method name differentiation)
        result2 = service.method2("test")                                                           # Should hit cache from method1

        assert result1 == "method1_test"
        assert result2 == "method1_test"                                                            # Same cached value!

    # ═══════════════════════════════════════════════════════════════════════════════
    # Real-world Scenario Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_api_response_caching_scenario(self):                                                   # Test realistic API response caching scenario
        api_calls = 0

        config = Schema__Cache__Decorator__Config(namespace  = f"test-api-{random_string()}"          ,
                                                  strategy   = Enum__Cache__Store__Strategy.KEY_BASED ,
                                                  key_fields = ["request.endpoint", "request.params"] ,     # Nested fields
                                                  file_id    = "api-response"                         )

        class APIService(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def fetch(self, request: APIRequest) -> APIResponse:
                nonlocal api_calls
                api_calls += 1

                return APIResponse(status = 200                                       ,             # Simulate API call
                                   data   = {"result": f"data_for_{request.endpoint}"},
                                   cached = False                                     )

        service = APIService()

        req1 = APIRequest(endpoint = "/users"        ,                                              # First request
                          params   = {"id": 123}     ,
                          headers  = {"Auth": "token1"})                                            # Not in key_fields

        resp1 = service.fetch(req1)
        assert resp1.status == 200
        assert api_calls    == 1

        req2 = APIRequest(endpoint = "/users"         ,                                             # Same endpoint/params, different headers - should cache
                          params   = {"id": 123}      ,
                          headers  = {"Auth": "token2"})                                            # Different but ignored

        resp2 = service.fetch(req2)
        assert resp2.data == resp1.data                                                             # Same cached response
        assert api_calls  == 1

        req3 = APIRequest(endpoint = "/posts"         ,                                             # Different endpoint - new call
                          params   = {"id": 123}      ,
                          headers  = {"Auth": "token1"})

        resp3 = service.fetch(req3)
        assert resp3.data != resp1.data
        assert api_calls  == 2

        assert resp1.obj() == __(cached=False, status=200, data=__(result='data_for_/users'))
        assert resp2.obj() == __(cached=False, status=200, data=__(result='data_for_/users'))
        assert resp3.obj() == __(cached=False, status=200, data=__(result='data_for_/posts'))

    def test_data_transformation_pipeline(self):                                                    # Test caching in a data transformation pipeline
        class TransformConfig(Type_Safe):
            normalize: bool = True
            uppercase: bool = False
            trim     : bool = True


        transform_calls = 0

        config = Schema__Cache__Decorator__Config(namespace  = f"test-pipeline-{random_string()}"    ,
                                                  strategy   = Enum__Cache__Store__Strategy.KEY_BASED,
                                                  key_fields = ["data", "config"]                    )

        class DataPipeline(Type_Safe):
            decorator__cache = self.decorator_cache

            @cache_response(config)
            def transform(self, data: str, config: TransformConfig) -> str:
                nonlocal transform_calls
                transform_calls += 1

                result = data
                if config.trim:
                    result = result.strip()
                if config.normalize:
                    result = " ".join(result.split())
                if config.uppercase:
                    result = result.upper()

                return result

        pipeline = DataPipeline()

        config1 = TransformConfig(normalize=True, uppercase=True)                                   # First transformation
        result1 = pipeline.transform("  hello   world  ", config1)
        assert result1         == "HELLO WORLD"
        assert transform_calls == 1

        result2 = pipeline.transform("  hello   world  ", config1)                                  # Same data and config - cached
        assert result2         == "HELLO WORLD"
        assert transform_calls == 1

        config2 = TransformConfig(normalize=False, uppercase=False)                                 # Different config - new transformation
        result3 = pipeline.transform("  hello   world  ", config2)
        assert result3         == "hello   world"
        assert transform_calls == 2

# classes used in test

class ResultSchema(Type_Safe):
    message: str
    count  : int

class APIRequest(Type_Safe):
    endpoint: str
    params  : dict
    headers : dict

class APIResponse(Type_Safe):
    status: int
    data  : dict
    cached: bool = False
