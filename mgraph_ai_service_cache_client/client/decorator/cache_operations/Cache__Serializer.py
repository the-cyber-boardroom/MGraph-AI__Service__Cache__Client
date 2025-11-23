import inspect
import json
import logging
from typing import Any, Callable, Optional, Union, get_args, get_origin, Type
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe              import type_safe
from mgraph_ai_service_cache_client.client.decorator.exceptions.Cache__Decorator__Exceptions import Cache__Serialization__Error

logger = logging.getLogger(__name__)


class Cache__Serializer(Type_Safe):             # Handles Type_Safe aware serialization/deserialization for cache operations

    @type_safe
    def serialize(self,                             # Serialize an object for caching
                  obj: Any                          # Object to serialize
             ) -> Union[dict, str, bytes, int,
                        float, list, tuple]:        #  Serialized representation (dict for Type_Safe objects, original for primitives)
        if obj is None:
            return None
            
        try:
            if isinstance(obj, Type_Safe):                                  # Type_Safe objects → dict via json()
                return obj.json()

            elif isinstance(obj, dict):                                     # Dict → return as-is (will be JSON serialized by storage)
                return obj

            elif isinstance(obj, (list, tuple)):                            # Lists/tuples → return as-is
                return obj

            elif isinstance(obj, bytes):                                    # Bytes → return as-is
                return obj

            elif isinstance(obj, (str, int, float, bool)):                  # Primitives (str, int, float, bool) → return as-is
                return obj

            elif hasattr(obj, '__dict__') and not callable(obj):            # Custom objects with __dict__ → convert to dict
                return obj.__dict__

            else:                                                           # Default: try to convert to string
                return str(obj)
                
        except Exception as e:
            type_name = type(obj).__name__
            raise Cache__Serialization__Error("serialize", type_name, str(e))

    @type_safe
    def deserialize(self,                                           # Deserialize cached data back to original type
                    data       : Any  = None,                       # Cached data to deserialize
                    target_type: Type = None                        # Expected type (from function signature)
                  ) -> Any:                                         # Deserialized object
        if data is None:
            return None
        
        if target_type is None:
            # No type hint, return as-is
            return data
            
        try:
            # Handle Optional types
            origin = get_origin(target_type)
            if origin is Union:
                args = get_args(target_type)
                # Check if it's Optional (Union[X, None])
                if len(args) == 2 and type(None) in args:
                    # Get the non-None type
                    actual_type = args[0] if args[1] is type(None) else args[1]
                    return self.deserialize(data, actual_type)
            
            # Type_Safe classes with from_json method
            if hasattr(target_type, 'from_json') and callable(target_type.from_json):
                if isinstance(data, dict):
                    return target_type.from_json(data)
                elif isinstance(data, str):
                    try:                                                    # Try to parse JSON string first
                        json_data = json.loads(data)
                        return target_type.from_json(json_data)
                    except:
                        # Not JSON, might be raw string
                        return data
            
            # Already the right type
            if isinstance(data, target_type):
                return data
            
            # Primitive type conversion
            if target_type in (str, int, float, bool, bytes):
                return target_type(data)
            
            # Dict type
            if target_type is dict or origin is dict:
                if isinstance(data, dict):
                    return data
                elif isinstance(data, str):
                    return json.loads(data)
            
            # List type
            if target_type is list or origin is list:
                if isinstance(data, list):
                    return data
                elif isinstance(data, str):
                    return json.loads(data)
            
            # Default: return as-is
            return data
            
        except Exception as e:
            type_name = target_type.__name__ if hasattr(target_type, '__name__') else str(target_type)
            raise Cache__Serialization__Error("deserialize", type_name, str(e))

    @type_safe
    def extract_type_hint(self, func: Callable) -> Optional[type]:
        """
        Extract the return type hint from a function signature
        
        Args:
            func: Function to inspect
            
        Returns:
            Return type annotation or None if not specified
        """
        try:
            sig = inspect.signature(func)
            
            if sig.return_annotation != inspect.Signature.empty:
                return sig.return_annotation
            
            return None
            
        except Exception as e:
            logger.debug(f"Could not extract type hint from {func.__name__}: {e}")
            return None

    @type_safe
    def is_type_safe_object(self, obj: Any) -> bool:
        """Check if object is a Type_Safe instance"""
        return isinstance(obj, Type_Safe)

    @type_safe
    def get_object_size(self, obj: Any) -> int:
        """
        Estimate the size of an object in bytes
        
        Args:
            obj: Object to measure
            
        Returns:
            Estimated size in bytes
        """
        import sys
        
        try:
            if isinstance(obj, bytes):
                return len(obj)
            elif isinstance(obj, str):
                return len(obj.encode('utf-8'))
            elif isinstance(obj, dict):
                return len(json.dumps(obj).encode('utf-8'))
            elif isinstance(obj, Type_Safe):
                return len(obj.json_bytes())
            else:
                return sys.getsizeof(obj)                               # Use sys.getsizeof for approximation
        except:
            return sys.getsizeof(obj)                                   # Fallback to basic size
