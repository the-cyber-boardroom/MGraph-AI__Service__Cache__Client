from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                         import __
from osbot_utils.utils.Objects                                                                      import base_classes
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                   import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier     import Safe_Str__Python__Identifier
from osbot_utils.utils.Misc                                                                         import random_string
from mgraph_ai_service_cache_client.client.decorator.Decorator__Cache                               import Decorator__Cache, _extract_type_hint, _determine_cache_data_type
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config       import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                   import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                import Enum__Client__Mode
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                      import Enum__Cache__Data_Type
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                       import Cache_Service__Fast_API
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                import Serverless__Fast_API__Config
from mgraph_ai_service_cache_client.utils.Version                                                   import version__mgraph_ai_service_cache_client


class test_Decorator__Cache(TestCase):                                                              # Test Decorator__Cache helper class using actual in-memory cache service

    @classmethod
    def setUpClass(cls):                                                                            # Set up in-memory cache service for all tests
        cls.serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)                # Create in-memory cache service
        cls.cache_service__fast_api = Cache_Service__Fast_API(config=cls.serverless_config).setup()
        cls.fast_api_app            = cls.cache_service__fast_api.app()
        cls.cache_service           = cls.cache_service__fast_api.cache_service
        cls.client_config           = Cache__Service__Fast_API__Client__Config(mode         = Enum__Client__Mode.IN_MEMORY,   # Create client config for in-memory mode
                                                                               fast_api_app = cls.fast_api_app            ,
                                                                               service_name = "test-decorator-cache"      )
        cls.client_cache_service = Client__Cache__Service(config=cls.client_config)                     # Create cache client
        cls.decorator_cache      = Decorator__Cache(client_cache_service = cls.client_cache_service)# Create Decorator__Cache instance

    def test__init__(self):                                                                         # Test Decorator__Cache initialization
        with self.decorator_cache as _:
            assert type(_)                 is Decorator__Cache
            assert base_classes(_)         == [Type_Safe, object]
            assert _.client_cache_service  is not None
            assert _._operations           is None                                                  # Lazy loaded
            assert _._key_builder          is None                                                  # Lazy loaded

    # ═══════════════════════════════════════════════════════════════════════════════
    # Component Lazy Loading Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_operations__lazy_loading(self):                                                        # Test that operations is created on first access
        decorator = Decorator__Cache(client_cache_service = self.client_cache_service)              # Create fresh instance

        assert decorator._operations is None                                                        # Initially None

        operations = decorator.operations()                                                         # Access operations

        assert operations              is not None                                                  # Now created
        assert decorator._operations   is not None

        operations2 = decorator.operations()                                                        # Same instance on subsequent calls (cached)
        assert operations2 is operations

    def test_key_builder__lazy_loading(self):                                                       # Test that key_builder is created on first access
        decorator = Decorator__Cache(client_cache_service = self.client_cache_service)              # Create fresh instance

        assert decorator._key_builder is None                                                       # Initially None

        key_builder = decorator.key_builder()                                                       # Access key_builder

        assert key_builder              is not None                                                 # Now created
        assert decorator._key_builder   is not None

        key_builder2 = decorator.key_builder()                                                      # Same instance on subsequent calls (cached)
        assert key_builder2 is key_builder

    # ═══════════════════════════════════════════════════════════════════════════════
    # Availability Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_is_available__with_client(self):                                                       # Test availability check when client is configured
        assert self.decorator_cache.is_available() is True

    def test_is_available__without_client(self):                                                    # Test availability check when no client is configured
        decorator_no_client = Decorator__Cache(client_cache_service = None)

        assert decorator_no_client.is_available() is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Status Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_status__with_client(self):                                                         # Test getting status when client is configured
        status = self.decorator_cache.get_status()

        assert status["available"] is True
        assert "mode" in status
        assert status["mode"] == str(Enum__Client__Mode.IN_MEMORY)                                  # Compare with enum string value
        assert "info" in status

    def test_get_status__without_client(self):                                                      # Test getting status when no client is configured
        decorator_no_client = Decorator__Cache(client_cache_service = None)

        status = decorator_no_client.get_status()

        assert status["available"] is False
        assert status["reason"]    == "No cache service configured"


    # ═══════════════════════════════════════════════════════════════════════════════
    # Component Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_all_components_work_together(self):                                                    # Test that all components can be accessed and work together
        operations  = self.decorator_cache.operations()                                             # Access all components
        key_builder = self.decorator_cache.key_builder()

        assert operations  is not None                                                              # Verify they exist
        assert key_builder is not None

        config = Schema__Cache__Decorator__Config(namespace  = "test-integration",                  # Build a cache key
                                                  key_fields = ["param1"]        )

        cache_key = key_builder.build_cache_key(config      = config                                    ,
                                                class_name  = Safe_Str__Python__Identifier("TestClass") ,
                                                method_name = Safe_Str__Python__Identifier("test_method"),
                                                params      = {"param1": "value1"}                      )

        assert cache_key is not None

        class TestData(Type_Safe):                                                                  # Store using operations
            field: str = "test"

        test_data = TestData()
        namespace = Safe_Str__Id("test-integration")
        stored    = operations.store(namespace = namespace                                   ,
                                     cache_key = Safe_Str__File__Path(f"integration/{random_string()}"),
                                     data      = test_data                                   ,
                                     config    = config                                      )

        assert stored is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type_Safe Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_decorator_cache_as_attribute(self):                                                    # Test using Decorator__Cache as an attribute in another Type_Safe class
        class ServiceWithCache(Type_Safe):
            decorator__cache: Decorator__Cache
            service_name    : str = "test-service"

        service = ServiceWithCache(decorator__cache = self.decorator_cache)

        assert service.decorator__cache                is not None
        assert service.decorator__cache.is_available() is True
        assert service.service_name                    == "test-service"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Error Handling Tests
    # ═══════════════════════════════════════════════════════════════════════════════


    def test_status_with_exception(self):                                                           # Test status handling when operations raise exceptions
        decorator = Decorator__Cache(client_cache_service = self.client_cache_service)

        status = decorator.get_status()

        assert isinstance(status, dict)                                                             # Should still return a valid status dict
        assert "available" in status

    # ═══════════════════════════════════════════════════════════════════════════════
    # Real Cache Operations Through Decorator__Cache
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_real_cache_operations(self):                                                           # Test performing real cache operations through Decorator__Cache
        namespace = "test-real-ops"
        cache_key = f"test/{random_string()}"
        data      = {"test": "data", "value": 42}

        config    = Schema__Cache__Decorator__Config(namespace = namespace                             ,
                                                     file_id   = "test-real"                           )

        stored    = self.decorator_cache.operations().store(namespace = namespace,                     # Store data
                                                            cache_key = cache_key,
                                                            data      = data     ,
                                                            config    = config   )

        cache_hash = self.decorator_cache.key_builder().build_cache_hash(cache_key)                              # Build cache hash
        retrieved = self.decorator_cache.operations().retrieve(namespace  = namespace             ,         # Retrieve data
                                                               cache_hash = cache_hash            )

        exists_before = self.decorator_cache.operations().exists(namespace  = namespace ,                   # Check exists
                                                                 cache_hash = cache_hash)

        invalidated   = self.decorator_cache.operations().invalidate(namespace  = namespace ,               # Invalidate
                                                                     cache_hash = cache_hash)
        exists_after  = self.decorator_cache.operations().exists(namespace  = namespace ,                   # Verify gone
                                                                 cache_hash = cache_hash)

        assert stored           is True
        assert retrieved        == data
        assert exists_before    is True
        assert invalidated      is True
        assert exists_after     is False


    # ═══════════════════════════════════════════════════════════════════════════════
    # execute_cached Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_execute_cached__basic(self):                                                           # Test execute_cached method with basic function
        call_count = 0

        class TestService(Type_Safe):
            def test_method(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{value}_{call_count}"

        service = TestService()
        config  = Schema__Cache__Decorator__Config(namespace  = f"test-exec-{random_string()}",
                                                   key_fields = ["value"]                     )

        result1 = self.decorator_cache.execute_cached(func   = TestService.test_method,             # First call
                                                      args   = (service, "test")      ,
                                                      kwargs = {}                     ,
                                                      config = config                 )

        assert result1    == "result_test_1"
        assert call_count == 1

        result2 = self.decorator_cache.execute_cached(func   = TestService.test_method,             # Second call - should hit cache
                                                      args   = (service, "test")      ,
                                                      kwargs = {}                     ,
                                                      config = config                 )

        assert result2    == "result_test_1"                                                        # Cached result
        assert call_count == 1                                                                      # Function not called again



    def test_execute_cached__different_params(self):                                                # Test execute_cached with different parameters
        call_count = 0

        class TestService(Type_Safe):
            def test_method(self, value: str) -> str:
                nonlocal call_count
                call_count += 1
                return f"result_{value}_{call_count}"

        service = TestService()
        config  = Schema__Cache__Decorator__Config(namespace  = f"test-exec-diff-{random_string()}",
                                                   key_fields = ["value"]                          )

        result1 = self.decorator_cache.execute_cached(func   = TestService.test_method,
                                                      args   = (service, "value1")    ,
                                                      kwargs = {}                     ,
                                                      config = config                 )

        result2 = self.decorator_cache.execute_cached(func   = TestService.test_method,
                                                      args   = (service, "value2")    ,
                                                      kwargs = {}                     ,
                                                      config = config                 )

        assert result1    == "result_value1_1"
        assert result2    == "result_value2_2"
        assert call_count == 2                                                                      # Both called (different params)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Function Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__extract_type_hint__with_return_type(self):                                            # Test _extract_type_hint with annotated function
        def func_with_hint() -> str:
            return "test"

        result = _extract_type_hint(func_with_hint)
        assert result is str

    def test__extract_type_hint__without_return_type(self):                                         # Test _extract_type_hint without annotation
        def func_no_hint():
            return "test"

        result = _extract_type_hint(func_no_hint)
        assert result is None

    def test__extract_type_hint__type_safe_return(self):                                            # Test _extract_type_hint with Type_Safe return
        class MySchema(Type_Safe):
            field: str

        def func_type_safe() -> MySchema:
            return MySchema(field="test")

        result = _extract_type_hint(func_type_safe)
        assert result is MySchema

    def test__determine_cache_data_type__string(self):                                              # Test _determine_cache_data_type for str
        data_type, type_safe_class = _determine_cache_data_type(str)

        assert data_type       == Enum__Cache__Data_Type.STRING
        assert type_safe_class is None

    def test__determine_cache_data_type__bytes(self):                                               # Test _determine_cache_data_type for bytes
        data_type, type_safe_class = _determine_cache_data_type(bytes)

        assert data_type       == Enum__Cache__Data_Type.BINARY
        assert type_safe_class is None

    def test__determine_cache_data_type__dict(self):                                                # Test _determine_cache_data_type for dict
        data_type, type_safe_class = _determine_cache_data_type(dict)

        assert data_type       == Enum__Cache__Data_Type.JSON
        assert type_safe_class is None

    def test__determine_cache_data_type__type_safe(self):                                           # Test _determine_cache_data_type for Type_Safe subclass
        class MySchema(Type_Safe):
            field: str

        data_type, type_safe_class = _determine_cache_data_type(MySchema)

        assert data_type       == Enum__Cache__Data_Type.TYPE_SAFE
        assert type_safe_class is MySchema

    def test__determine_cache_data_type__none(self):                                                # Test _determine_cache_data_type for None
        data_type, type_safe_class = _determine_cache_data_type(None)

        assert data_type       == Enum__Cache__Data_Type.JSON                                       # Default to JSON
        assert type_safe_class is None

    def test__determine_cache_data_type__optional(self):                                            # Test _determine_cache_data_type for Optional type
        from typing import Optional

        data_type, type_safe_class = _determine_cache_data_type(Optional[str])

        assert data_type       == Enum__Cache__Data_Type.STRING                                     # Should unwrap Optional
        assert type_safe_class is None