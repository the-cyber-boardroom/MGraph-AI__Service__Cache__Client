from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                import type_safe
from osbot_utils.decorators.methods.cache_on_self                                             import cache_on_self
from mgraph_ai_service_cache_client.client.Client__Cache__Service                             import Client__Cache__Service
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Operations       import Cache__Operations
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Serializer       import Cache__Serializer
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Key__Builder     import Cache__Key__Builder


class Decorator__Cache(Type_Safe):
    """
    Helper class that service instances can use as their decorator__cache attribute.
    
    This class provides all the components needed for cache decoration:
    - Client for cache service communication
    - Operations for cache management
    - Serializer for Type_Safe aware serialization
    - Key builder for cache key generation
    
    Usage:
        class MyService(Type_Safe):
            decorator__cache: Decorator__Cache  # Injected or configured
            
            @cache_response(config)
            def my_method(self, ...):
                pass
    """
    
    client_cache_service : Client__Cache__Service = None
    _operations         : Cache__Operations      = None
    _serializer         : Cache__Serializer      = None
    _key_builder        : Cache__Key__Builder     = None

    @cache_on_self
    def operations(self) -> Cache__Operations:
        """Get or create cache operations handler"""
        if not self._operations:
            self._operations = Cache__Operations(
                client_cache_service = self.client_cache_service,
                serializer          = self.serializer()
            )
        return self._operations

    @cache_on_self
    def serializer(self) -> Cache__Serializer:
        """Get or create serializer"""
        if not self._serializer:
            self._serializer = Cache__Serializer()
        return self._serializer

    @cache_on_self
    def key_builder(self) -> Cache__Key__Builder:
        """Get or create key builder"""
        if not self._key_builder:
            self._key_builder = Cache__Key__Builder()
        return self._key_builder

    @type_safe
    def is_available(self) -> bool:
        """Check if cache is available and configured"""
        return self.client_cache_service is not None

    @type_safe
    def get_status(self) -> dict:
        """Get cache status information"""
        if not self.is_available():
            return {
                "available": False,
                "reason": "No cache service configured"
            }
        
        return self.operations().get_client_status()

    @type_safe
    def clear_cache_for_namespace(self, namespace: str) -> bool:
        """
        Clear all cache entries in a namespace.
        
        Note: This is a utility method and might not be available
        in all cache service implementations.
        
        Args:
            namespace: Namespace to clear
            
        Returns:
            True if cleared successfully
        """
        if not self.is_available():
            return False
        
        try:
            # This would require admin operations
            # For now, return False as this needs service support
            return False
        except Exception:
            return False
