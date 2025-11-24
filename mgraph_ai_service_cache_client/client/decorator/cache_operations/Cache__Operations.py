import logging
from typing                                                                                      import Union, Dict, Type
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                  import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash         import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                   import type_safe
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                import Client__Cache__Service
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config    import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Serializer          import Cache__Serializer
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                   import Enum__Cache__Data_Type

logger = logging.getLogger(__name__)


class Cache__Operations(Type_Safe):                                                 # Handles all cache operations for the decorator.
    
    client_cache_service: Client__Cache__Service
    serializer         : Cache__Serializer       = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.serializer:
            self.serializer = Cache__Serializer()

    @type_safe
    def retrieve(self                               ,                   # Retrieve data from cache and deserialize it.
                 namespace       : Safe_Str__Id           ,             # Cache namespace
                 cache_hash      : Safe_Str__Cache_Hash   ,             # Hash to retrieve
                 data_type       : Enum__Cache__Data_Type ,             # cache data type (string, json, binary or type-safe)
                 type_safe_class : Type[Type_Safe] = None               # if type-safe data type, this is the class to return via .from_json()
               ) -> Union[Type_Safe, Dict, str, bytes]:                 # Deserialized data or None if not found

        if not self.client_cache_service:
            return None

        with self.client_cache_service.client().retrieve() as _:                # Use the cache client to retrieve data
            result = None
            if   data_type == Enum__Cache__Data_Type.STRING:
                result     =  _.retrieve__hash__cache_hash__string (cache_hash = cache_hash, namespace=namespace)

            elif data_type == Enum__Cache__Data_Type.JSON:
                result     = _.retrieve__hash__cache_hash__json    (cache_hash = cache_hash, namespace=namespace)

            elif data_type == Enum__Cache__Data_Type.TYPE_SAFE:
                data_json  = _.retrieve__hash__cache_hash__json    (cache_hash = cache_hash, namespace=namespace)
                if type_safe_class:
                    result = type_safe_class.from_json(data_json)

            elif data_type == Enum__Cache__Data_Type.BINARY:
                result     = _.retrieve__hash__cache_hash__binary  (cache_hash = cache_hash, namespace=namespace)
        return result

    @type_safe
    def store(self,                                                 # Store data in cache after serialization.
             namespace : Safe_Str__Id                      ,        # Cache namespace
             cache_key : Safe_Str__File__Path              ,        # Cache key for storage
             data      : Union[Type_Safe, dict, bytes, str],        # Data to store (one of the 3 types supported by cache service and dict)
             config    : Schema__Cache__Decorator__Config           # Cache configuration
        ) -> bool:                                                  # returns True if stored successfully, False otherwise

        if not self.client_cache_service:
            return False

        with self.client_cache_service.client() as cache_client:
            if isinstance(data,Type_Safe):                                          # if we received a Type_Save object
                data = data.json()                                                  # convert it to a dict via .json()
            kwargs = dict(namespace  = namespace      ,
                          strategy   = config.strategy,
                          cache_key  = cache_key      ,
                          body       = data           ,
                          file_id    = config.file_id  )
            if type(data) is str:
                result = cache_client.store().store__string__cache_key(**kwargs)
            elif type(data) is dict:
                result = cache_client.store().store__json__cache_key  (**kwargs)
            elif type(data) is bytes:
                result = cache_client.store().store__binary__cache_key(**kwargs)

            if result and hasattr(result, 'cache_id'):
                return True
            else:
                return False

    @type_safe
    def invalidate(self,                                # Invalidate (delete) a cache entry.
                  namespace  : Safe_Str__Id        ,    # Cache namespace
                  cache_hash : Safe_Str__Cache_Hash     # Hash to invalidate
                 ) -> bool:                             # True if invalidated successfully, False otherwise

        if not self.client_cache_service:
            return False

        with self.client_cache_service.client() as cache_client:        # First, we need to get the cache_id from the hash

            result = cache_client.retrieve().retrieve__hash__cache_hash__cache_id(cache_hash = cache_hash,    # Try to retrieve to get the cache_id
                                                                                  namespace  = namespace )
            if not result:
                return False
            cache_id = result.get('cache_id')                                                           # found cache_id for this cache_hash

            delete_result = cache_client.delete().delete__cache_id(cache_id  = str(cache_id),           # Now delete using the cache_id
                                                                   namespace = str(namespace))

        if delete_result:
            return True
        else:
            return False


    @type_safe
    def exists(self,
              namespace  : Safe_Str__Id,
              cache_hash : Safe_Str__Cache_Hash
             ) -> bool:
        """
        Check if a cache entry exists.
        
        Args:
            namespace: Cache namespace
            cache_hash: Hash to check
            
        Returns:
            True if exists, False otherwise
        """
        if not self.client_cache_service:
            return False
        
        try:
            with self.client_cache_service.client() as cache_client:
                # The exists endpoint might not be available, try retrieve instead
                result = cache_client.retrieve().retrieve__hash__cache_hash(
                    cache_hash = str(cache_hash),
                    namespace  = str(namespace)
                )
            
            return result is not None
            
        except Exception as e:
            logger.debug(f"Error checking cache existence: {e}")
            return False

    @type_safe
    def get_client_status(self) -> dict:
        """
        Get status information about the cache client.
        
        Returns:
            Dictionary with status information
        """
        if not self.client_cache_service:
            return {"available": False, "reason": "No client configured"}
        
        try:
            with self.client_cache_service.client() as cache_client:
                # Try to get server info
                info = cache_client.info().status()
                return {
                    "available": True,
                    "mode": str(self.client_cache_service.config.mode),
                    "info": info
                }
        except Exception as e:
            return {
                "available": False,
                "reason": str(e)
            }
