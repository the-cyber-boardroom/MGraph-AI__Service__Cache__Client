"""
Cache Response Decorator - Refactored

This module provides a decorator for transparently caching method responses.
It has been refactored to follow single responsibility principles with specialized
classes handling different aspects of caching.

The decorator is now a thin orchestration layer that delegates to:
- Cache__Operations: Handles storage/retrieval
- Cache__Serializer: Handles Type_Safe serialization
- Cache__Key__Builder: Generates cache keys
- Decorator__Cache: Helper class for instances
"""

import functools
import inspect
import logging
from typing                                                                                     import Any, Callable
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config   import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.decorator.schemas.enums.Enum__Cache__Decorator__Mode import Enum__Cache__Decorator__Mode
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Operations         import Cache__Operations
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Serializer         import Cache__Serializer
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Key__Builder       import Cache__Key__Builder
from mgraph_ai_service_cache_client.client.decorator.Decorator__Cache                           import Decorator__Cache
from mgraph_ai_service_cache_client.client.decorator.exceptions.Cache__Decorator__Exceptions    import (
    Cache__Client__Not__Found,
    Cache__Invalid__Config
)

logger = logging.getLogger(__name__)


def cache_response(config: Schema__Cache__Decorator__Config) -> Callable:
    """
    Decorator that caches method responses transparently.
    
    This decorator intercepts method calls, checks for cached results,
    and stores results when not cached. It leverages Type_Safe serialization
    and supports various caching strategies.
    
    Usage:
        from mgraph_ai_service_cache_client.client.decorator.Cache__Decorator__Configs import (
            CACHE_CONFIG__TRANSFORMATION
        )
        
        class MyService(Type_Safe):
            decorator__cache: Decorator__Cache  # Must be set before calling cached methods
            
            @cache_response(CACHE_CONFIG__TRANSFORMATION)
            def transform(self, request: Request) -> Response:
                # Method logic here
                return Response(...)
    
    Args:
        config: Cache configuration object defining namespace, strategy, etc.
        
    Returns:
        Decorated function with caching behavior
        
    Raises:
        Cache__Invalid__Config: If configuration is invalid
        Cache__Client__Not__Found: If cache client not found on instance (logged, not raised)
    """
    # Validate configuration
    if not config:
        raise Cache__Invalid__Config("config", "Configuration cannot be None")
    
    if not config.namespace:
        raise Cache__Invalid__Config("namespace", "Namespace must be specified")
    
    # Create shared instances for the decorator
    key_builder = Cache__Key__Builder()
    serializer = Cache__Serializer()
    
    def decorator(func: Callable) -> Callable:
        """Inner decorator function"""
        
        # Extract return type hint once at decoration time
        return_type = serializer.extract_type_hint(func)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Wrapper function that implements caching logic"""
            
            # Quick exit if caching is disabled
            if not config.enabled or config.mode == Enum__Cache__Decorator__Mode.DISABLED:
                return func(*args, **kwargs)
            
            # Extract 'self' from args (first positional argument for methods)
            if not args:
                # Not a method call, execute without caching
                logger.debug(f"No 'self' argument found for {func.__name__}, executing without cache")
                return func(*args, **kwargs)
            
            self_instance = args[0]
            
            # Check if it's actually an instance method
            if not isinstance(self_instance, object) or not hasattr(self_instance.__class__, func.__name__):
                # Not an instance method, execute without caching
                return func(*args, **kwargs)
            
            # Get the cache helper from the instance
            cache_helper = None
            
            # First try to get Decorator__Cache instance
            if hasattr(self_instance, config.cache_attr_name):
                cache_attr = getattr(self_instance, config.cache_attr_name)
                
                # Check if it's a Decorator__Cache instance
                if isinstance(cache_attr, Decorator__Cache):
                    cache_helper = cache_attr
                # Check if it's a Client__Cache__Service (legacy support)
                elif hasattr(cache_attr, 'client'):
                    # Wrap it in a Decorator__Cache
                    from mgraph_ai_service_cache_client.client.Client__Cache__Service import Client__Cache__Service
                    if isinstance(cache_attr, Client__Cache__Service):
                        cache_helper = Decorator__Cache(client_cache_service=cache_attr)
            
            if not cache_helper or not cache_helper.is_available():
                # No cache available, execute without caching
                class_name = type(self_instance).__name__
                logger.debug(
                    f"Cache not available on {class_name}.{config.cache_attr_name}, "
                    f"executing {func.__name__} without cache"
                )
                return func(*args, **kwargs)
            
            # Build cache key from parameters
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Extract class and method names
            class_name = type(self_instance).__name__
            method_name = func.__name__
            
            # Remove 'self' from parameters
            params_dict = dict(bound_args.arguments)
            params_dict.pop('self', None)
            
            # Generate cache key and hash
            cache_key = cache_helper.key_builder().build_cache_key(
                config      = config,
                class_name  = class_name,
                method_name = method_name,
                params      = params_dict
            )
            
            cache_hash = cache_helper.key_builder().build_cache_hash(cache_key)
            
            # Try to retrieve from cache (unless in WRITE_ONLY mode)
            if config.mode != Enum__Cache__Decorator__Mode.READ_ONLY:
                try:
                    cached_result = cache_helper.operations().retrieve(
                        namespace   = config.namespace,
                        cache_hash  = cache_hash,
                        target_type = return_type
                    )
                    
                    if cached_result is not None:
                        logger.info(
                            f"Cache HIT: {class_name}.{method_name} "
                            f"[key: {cache_key}, hash: {cache_hash[:8]}...]"
                        )
                        return cached_result
                    
                except Exception as e:
                    # Log but don't fail on retrieval errors
                    logger.warning(f"Cache retrieval error (continuing without cache): {e}")
            
            logger.info(
                f"Cache MISS: {class_name}.{method_name} "
                f"[key: {cache_key}, hash: {cache_hash[:8]}...]"
            )
            
            # Execute the actual method
            try:
                result = func(*args, **kwargs)
                
                # Store result in cache (only in ENABLED mode, not READ_ONLY)
                if config.mode == Enum__Cache__Decorator__Mode.ENABLED:
                    try:
                        stored = cache_helper.operations().store(
                            namespace = config.namespace,
                            cache_key = cache_key,
                            data      = result,
                            config    = config
                        )
                        
                        if stored:
                            logger.debug(f"Result cached successfully for key: {cache_key}")
                        else:
                            logger.debug(f"Result not cached (store returned False) for key: {cache_key}")
                            
                    except Exception as e:
                        # Log but don't fail on storage errors
                        logger.warning(f"Cache storage error (result returned without caching): {e}")
                
                return result
                
            except Exception as e:
                # Handle execution errors
                if config.invalidate_on_error and config.mode == Enum__Cache__Decorator__Mode.ENABLED:
                    try:
                        # Try to invalidate the cache entry
                        cache_helper.operations().invalidate(
                            namespace  = config.namespace,
                            cache_hash = cache_hash
                        )
                        logger.debug(f"Cache invalidated due to execution error: {e}")
                    except Exception as inv_error:
                        logger.warning(f"Failed to invalidate cache after error: {inv_error}")
                
                # Re-raise the original exception
                raise
        
        # Add metadata to the wrapper for introspection
        wrapper._cache_config = config
        wrapper._cache_enabled = True
        wrapper._original_func = func
        
        return wrapper
    
    return decorator


def disable_cache_for_method(func: Callable) -> Callable:
    """
    Decorator to explicitly disable caching for a method.
    
    This is useful when you want to temporarily disable caching
    for debugging or testing purposes.
    
    Usage:
        @disable_cache_for_method
        @cache_response(config)
        def my_method(self, ...):
            pass
    """
    if hasattr(func, '_cache_enabled'):
        func._cache_enabled = False
    return func


def get_cache_config(func: Callable) -> Schema__Cache__Decorator__Config:
    """
    Get the cache configuration from a decorated method.
    
    Args:
        func: Decorated method
        
    Returns:
        Cache configuration or None if not cached
    """
    if hasattr(func, '_cache_config'):
        return func._cache_config
    return None


def is_cache_decorated(func: Callable) -> bool:
    """
    Check if a method has cache decoration.
    
    Args:
        func: Method to check
        
    Returns:
        True if decorated with @cache_response
    """
    return hasattr(func, '_cache_enabled') and func._cache_enabled
