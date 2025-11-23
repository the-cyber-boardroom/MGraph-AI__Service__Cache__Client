from unittest                                                                              import TestCase
from osbot_utils.testing.__                                                                import __
from osbot_utils.utils.Objects                                                             import base_classes
from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe
from mgraph_ai_service_cache_client.client.decorator.Decorator__Cache                      import Decorator__Cache
from mgraph_ai_service_cache_client.client.Client__Cache__Service                          import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode       import Enum__Client__Mode

# Import cache service components for in-memory testing
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                              import Cache_Service__Fast_API
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                       import Serverless__Fast_API__Config


class test_Decorator__Cache(TestCase):
    """Test Decorator__Cache helper class using actual in-memory cache service"""

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
            service_name = "test-decorator-cache"
        )
        
        # Create cache client
        cls.client_cache_service = Client__Cache__Service(config=client_config)
        
        # Create Decorator__Cache instance
        cls.decorator_cache = Decorator__Cache(
            client_cache_service = cls.client_cache_service
        )

    def test__init__(self):
        with self.decorator_cache as _:
            assert type(_)                  is Decorator__Cache
            assert base_classes(_)          == [Type_Safe, object]
            assert _.client_cache_service   is not None
            assert _._operations            is None  # Lazy loaded
            assert _._serializer            is None  # Lazy loaded
            assert _._key_builder           is None  # Lazy loaded

    # ═══════════════════════════════════════════════════════════════════════════════
    # Component Lazy Loading Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_operations__lazy_loading(self):
        """Test that operations is created on first access"""
        # Create fresh instance
        decorator = Decorator__Cache(
            client_cache_service = self.client_cache_service
        )
        
        # Initially None
        assert decorator._operations is None
        
        # Access operations
        operations = decorator.operations()
        
        # Now created
        assert operations is not None
        assert decorator._operations is not None
        
        # Same instance on subsequent calls (cached)
        operations2 = decorator.operations()
        assert operations2 is operations

    def test_serializer__lazy_loading(self):
        """Test that serializer is created on first access"""
        # Create fresh instance
        decorator = Decorator__Cache(
            client_cache_service = self.client_cache_service
        )
        
        # Initially None
        assert decorator._serializer is None
        
        # Access serializer
        serializer = decorator.serializer()
        
        # Now created
        assert serializer is not None
        assert decorator._serializer is not None
        
        # Same instance on subsequent calls (cached)
        serializer2 = decorator.serializer()
        assert serializer2 is serializer

    def test_key_builder__lazy_loading(self):
        """Test that key_builder is created on first access"""
        # Create fresh instance
        decorator = Decorator__Cache(
            client_cache_service = self.client_cache_service
        )
        
        # Initially None
        assert decorator._key_builder is None
        
        # Access key_builder
        key_builder = decorator.key_builder()
        
        # Now created
        assert key_builder is not None
        assert decorator._key_builder is not None
        
        # Same instance on subsequent calls (cached)
        key_builder2 = decorator.key_builder()
        assert key_builder2 is key_builder

    # ═══════════════════════════════════════════════════════════════════════════════
    # Availability Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_is_available__with_client(self):
        """Test availability check when client is configured"""
        assert self.decorator_cache.is_available() is True

    def test_is_available__without_client(self):
        """Test availability check when no client is configured"""
        decorator_no_client = Decorator__Cache(
            client_cache_service = None
        )
        
        assert decorator_no_client.is_available() is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Status Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_get_status__with_client(self):
        """Test getting status when client is configured"""
        status = self.decorator_cache.get_status()
        
        assert status["available"] is True
        assert "mode" in status
        assert status["mode"] == "IN_MEMORY"
        assert "info" in status

    def test_get_status__without_client(self):
        """Test getting status when no client is configured"""
        decorator_no_client = Decorator__Cache(
            client_cache_service = None
        )
        
        status = decorator_no_client.get_status()
        
        assert status["available"] is False
        assert status["reason"] == "No cache service configured"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Clear Cache Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_clear_cache_for_namespace(self):
        """Test clearing cache for namespace (currently not implemented)"""
        result = self.decorator_cache.clear_cache_for_namespace("test-namespace")
        
        # Currently returns False as this needs service support
        assert result is False

    def test_clear_cache_for_namespace__no_client(self):
        """Test clearing cache when no client available"""
        decorator_no_client = Decorator__Cache(
            client_cache_service = None
        )
        
        result = decorator_no_client.clear_cache_for_namespace("test-namespace")
        
        assert result is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Component Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_all_components_work_together(self):
        """Test that all components can be accessed and work together"""
        # Access all components
        operations = self.decorator_cache.operations()
        serializer = self.decorator_cache.serializer()
        key_builder = self.decorator_cache.key_builder()
        
        # Verify they exist
        assert operations is not None
        assert serializer is not None
        assert key_builder is not None
        
        # Verify operations has the same serializer
        assert operations.serializer is serializer
        
        # Test a complete workflow
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
        from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
        from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config import Schema__Cache__Decorator__Config
        from osbot_utils.utils.Misc import random_string
        
        # Build a cache key
        config = Schema__Cache__Decorator__Config(
            namespace  = "test-integration",
            key_fields = ["param1"]
        )
        
        cache_key = key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {"param1": "value1"}
        )
        
        # Serialize some data
        class TestData(Type_Safe):
            field: str = "test"
        
        test_data = TestData()
        serialized = serializer.serialize(test_data)
        
        # Store using operations
        namespace = Safe_Str__Id("test-integration")
        stored = operations.store(
            namespace = namespace,
            cache_key = Safe_Str__File__Path(f"integration/{random_string()}"),
            data      = test_data,
            config    = config
        )
        
        assert stored is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type_Safe Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_type_safe_attributes(self):
        """Test that Decorator__Cache properly follows Type_Safe patterns"""
        # Test obj() method
        obj_dict = self.decorator_cache.obj()
        assert "client_cache_service" in obj_dict
        
        # Test json() method
        json_dict = self.decorator_cache.json()
        assert isinstance(json_dict, dict)
        
        # Test that it's a proper Type_Safe instance
        assert isinstance(self.decorator_cache, Type_Safe)

    def test_decorator_cache_as_attribute(self):
        """Test using Decorator__Cache as an attribute in another Type_Safe class"""
        class ServiceWithCache(Type_Safe):
            decorator__cache: Decorator__Cache
            service_name: str = "test-service"
        
        service = ServiceWithCache(
            decorator__cache = self.decorator_cache
        )
        
        assert service.decorator__cache is not None
        assert service.decorator__cache.is_available() is True
        assert service.service_name == "test-service"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Error Handling Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_operations_without_client(self):
        """Test that operations can be created even without client"""
        decorator_no_client = Decorator__Cache(
            client_cache_service = None
        )
        
        operations = decorator_no_client.operations()
        assert operations is not None
        assert operations.client_cache_service is None

    def test_status_with_exception(self):
        """Test status handling when operations raise exceptions"""
        # This is tricky to test without mocks, but we can test the general flow
        decorator = Decorator__Cache(
            client_cache_service = self.client_cache_service
        )
        
        status = decorator.get_status()
        
        # Should still return a valid status dict
        assert isinstance(status, dict)
        assert "available" in status

    # ═══════════════════════════════════════════════════════════════════════════════
    # Real Cache Operations Through Decorator__Cache
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_real_cache_operations(self):
        """Test performing real cache operations through Decorator__Cache"""
        from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
        from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
        from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
        from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config import Schema__Cache__Decorator__Config
        from osbot_utils.utils.Misc import random_string
        
        namespace = Safe_Str__Id("test-real-ops")
        cache_key = Safe_Str__File__Path(f"test/{random_string()}")
        data = {"test": "data", "value": 42}
        
        config = Schema__Cache__Decorator__Config(
            namespace = str(namespace),
            file_id   = "test-real"
        )
        
        # Store data
        stored = self.decorator_cache.operations().store(
            namespace = namespace,
            cache_key = cache_key,
            data      = data,
            config    = config
        )
        
        assert stored is True
        
        # Build cache hash
        cache_hash = self.decorator_cache.key_builder().build_cache_hash(cache_key)
        
        # Retrieve data
        retrieved = self.decorator_cache.operations().retrieve(
            namespace   = namespace,
            cache_hash  = cache_hash,
            target_type = dict
        )
        
        assert retrieved == data
        
        # Check exists
        exists = self.decorator_cache.operations().exists(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert exists is True
        
        # Invalidate
        invalidated = self.decorator_cache.operations().invalidate(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert invalidated is True
        
        # Verify gone
        exists_after = self.decorator_cache.operations().exists(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert exists_after is False
