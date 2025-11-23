from unittest                                                                                       import TestCase

import pytest
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                import Serverless__Fast_API__Config
from osbot_utils.helpers.cache.Cache__Hash__Generator                                               import Cache__Hash__Generator
from osbot_utils.utils.Objects                                                                      import base_classes
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash            import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                   import Safe_Str__File__Path
from osbot_utils.utils.Misc                                                                         import random_string, random_bytes
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                       import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Operations             import Cache__Operations
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Serializer             import Cache__Serializer
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config       import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Data_Type                      import Enum__Cache__Data_Type
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy                import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.client.Client__Cache__Service                                   import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                import Enum__Client__Mode


class test_Cache__Operations(TestCase):             # Test Cache__Operations using actual in-memory cache service

    @classmethod
    def setUpClass(cls):                            # Set up in-memory cache service for all tests

        serverless_config       = Serverless__Fast_API__Config(enable_api_key=False)                # Create in-memory cache service
        cache_service__fast_api = Cache_Service__Fast_API(config=serverless_config).setup()
        cls.fast_api_app        = cache_service__fast_api.app()
        cls.cache_service       = cache_service__fast_api.cache_service

        client_config            = Cache__Service__Fast_API__Client__Config(mode         = Enum__Client__Mode.IN_MEMORY,           # Create client config for in-memory mode
                                                                            fast_api_app = cls.fast_api_app            ,
                                                                            service_name = "test-cache-service"        )
        cls.client_cache_service = Client__Cache__Service(config=client_config)                                         # Create cache client
        cls.cache_operations     = Cache__Operations(client_cache_service = cls.client_cache_service,                   # Create Cache__Operations instance
                                                     serializer           = Cache__Serializer()     )                   # Test namespace
        cls.test_namespace       = Safe_Str__Id("test-operations")
        cls.hash_generator       = Cache__Hash__Generator()     # todo: see if we shouldn't move this to the Cache__Operations

    def test__init__(self):
        with self.cache_operations as _:
            assert type(_)                   is Cache__Operations
            assert base_classes(_)           == [Type_Safe, object]
            assert _.client_cache_service    is not None
            assert _.serializer              is not None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Store and Retrieve Tests (using real cache)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_store_and_retrieve__string(self):              # Test storing and retrieving a string value
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/string/{random_string()}")
        data      = "test string value"

                                           # Get the cache hash for retrieval
        cache_hash     = self.hash_generator.from_string(data)
        assert cache_hash == "f29e1de1c8ce2f8e"
        
        config = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                  strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                  file_id   = "test-string"                         )

        stored = self.cache_operations.store(namespace = namespace,                 # Store data
                                             cache_key = cache_key,
                                             data      = data,
                                             config    = config)

        retrieved = self.cache_operations.retrieve(namespace   = namespace                    ,       # Retrieve data from Cache Operations
                                                   cache_hash  = cache_hash                   ,       # for this hash
                                                   data_type   = Enum__Cache__Data_Type.STRING)       # as string

        direct    = (self.client_cache_service.client ()                            # Retrieve data directly from cache
                                             .retrieve()
                                             .retrieve__hash__cache_hash__string(cache_hash=cache_hash, namespace=namespace))
        assert stored    is True
        assert retrieved == data
        assert retrieved == direct



    def test_store_and_retrieve__dict(self):                        # Test storing and retrieving a dictionary
        namespace  = self.test_namespace
        cache_key  = Safe_Str__File__Path(f"test/dict/{random_string()}")
        data       = {"key1": "value1", "key2": 42, "nested": {"inner": "value"}}
        cache_hash = self.hash_generator.from_json(data)                                    # Get the cache hash
        config     = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-dict"                           )

        stored = self.cache_operations.store(namespace = namespace,                                 # Store data
                                             cache_key = cache_key,
                                             data      = data,
                                             config    = config)


        retrieved = self.cache_operations.retrieve(namespace   = namespace                      ,       # Retrieve data
                                                   cache_hash  = cache_hash                     ,       # from this hash
                                                   data_type   = Enum__Cache__Data_Type.JSON)         # as json
        direct    = (self.client_cache_service.client ()                                        # Retrieve data directly from cache
                                             .retrieve()
                                             .retrieve__hash__cache_hash__json(cache_hash=cache_hash, namespace=namespace))
        assert stored           is True
        assert type(retrieved)  is dict
        assert type(data     )  is dict
        assert type(direct   )  is dict
        assert retrieved        == data                                                         # retrieved data matches the original data stored
        assert retrieved        == direct                                                       # retrieved data matches the data we get from directly from the cache service

    def test_store_and_retrieve__type_safe_object(self):        # Test storing and retrieving a Type_Safe object
        class TestSchema(Type_Safe):
            field1: str
            field2: int
            field3: dict
        
        namespace  = self.test_namespace
        cache_key  = Safe_Str__File__Path(f"test/typesafe/{random_string()}")

        data       = TestSchema(field1 = "test"             ,
                                field2 = 42                 ,
                                field3 = {"nested": "value"})
        cache_hash = self.hash_generator.from_json(data.json())
        config     = Schema__Cache__Decorator__Config(namespace = namespace                             ,
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-typesafe"                       )

        stored      = self.cache_operations.store(namespace = namespace  ,                               # Store data using the Cache Operations
                                                  cache_key = cache_key  ,
                                                  data      = data       ,
                                                  config    = config     )
        retrieved   = self.cache_operations.retrieve(namespace       = namespace                       ,   # Retrieve data via cache_operations
                                                     cache_hash      = cache_hash                      ,      # for this hash
                                                     data_type       = Enum__Cache__Data_Type.TYPE_SAFE,      # as Type_Safe
                                                     type_safe_class = TestSchema                      )      # as TestSchema instance
        direct_json = (self.client_cache_service.client ()                                          # Retrieve data directly from cache
                                                .retrieve()
                                                .retrieve__hash__cache_hash__json(cache_hash=cache_hash, namespace=namespace))

        assert stored is True
        assert isinstance(retrieved, Type_Safe)
        assert type(data     )   is TestSchema
        assert type(retrieved)   is TestSchema                                                      # the data we retrieve from the cache is already in the correct type
        assert type(direct_json) is dict                                                            # the data we retrieve directly is json/dict
        assert retrieved.obj ()  == data.obj()
        assert retrieved.json()  == data.json()
        assert retrieved.json()  == direct_json                                                     # confirm that the direct_json matches the new object created

    def test_store_and_retrieve__bytes(self):                                                       # Test storing and retrieving binary data
        namespace  = self.test_namespace
        cache_key  = f"test/binary/{random_string()}"
        data       = b"test binary data " + random_bytes()
        cache_hash = self.hash_generator.from_bytes(data)
        config     = Schema__Cache__Decorator__Config(namespace = namespace                             ,
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-binary"                         )
        
        # Store data
        stored = self.cache_operations.store(namespace = namespace,
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )
        


        retrieved = self.cache_operations.retrieve(namespace   = namespace                    ,
                                                   cache_hash  = cache_hash                   ,
                                                   data_type   = Enum__Cache__Data_Type.BINARY)
        direct_bytes = (self.client_cache_service.client ()                                          # Retrieve data directly from cache
                                        .retrieve()
                                        .retrieve__hash__cache_hash__binary(cache_hash=cache_hash, namespace=namespace))

        assert stored             is True
        assert type(retrieved)    is bytes
        assert type(direct_bytes) is bytes
        assert retrieved          == data
        assert direct_bytes       == data

    def test_retrieve__not_found(self):                         # Test retrieving non-existent data
        namespace = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("aaaaa12345")

        for data_type in Enum__Cache__Data_Type.__members__:
            retrieved = self.cache_operations.retrieve(namespace   = namespace  ,
                                                       cache_hash  = cache_hash ,
                                                       data_type   = data_type )
        
            assert retrieved is None

    def test_store__none_value(self):                       # Test that None values are not cached
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/none/{random_string()}")
        data = None

        config = Schema__Cache__Decorator__Config(namespace          = namespace                             ,
                                                  strategy           = Enum__Cache__Store__Strategy.KEY_BASED)

        error_message = "Parameter 'data' is not optional but got None"
        with pytest.raises(ValueError, match=error_message) as e:
            self.cache_operations.store(namespace = namespace,
                                        cache_key = cache_key,
                                        data      = data     ,      # @type_safe will raise exception here
                                        config    = config   )


    # TODO: Fix from here based on the pattern above

    # ═══════════════════════════════════════════════════════════════════════════════
    # Invalidation Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_invalidate__existing_entry(self):  # Test invalidating an existing cache entry
        namespace  = self.test_namespace
        cache_key  = f"test/invalidate/{random_string()}"
        data       = "data to invalidate"
        cache_hash = self.hash_generator.from_string(data)
        config     = Schema__Cache__Decorator__Config(namespace = str(namespace),
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-invalidate")
        stored     = self.cache_operations.store(namespace = namespace,                     # First, store data
                                                 cache_key = cache_key,
                                                 data      = data     ,
                                                 config    = config   )
        assert stored is True

        retrieved = self.cache_operations.retrieve(namespace  = namespace                    ,             # Verify it exists
                                                   cache_hash = cache_hash                   ,
                                                   data_type  = Enum__Cache__Data_Type.STRING)
        assert retrieved == data

        # Invalidate it
        invalidated = self.cache_operations.invalidate(namespace  = namespace,
                                                       cache_hash = cache_hash)
        assert invalidated is True
        return
        # Verify it's gone
        retrieved_after = self.cache_operations.retrieve(
            namespace   = namespace,
            cache_hash  = cache_hash,
            target_type = str
        )
        assert retrieved_after is None

    def test_invalidate__nonexistent_entry(self):
        """Test invalidating a non-existent cache entry"""
        namespace = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("nonexistent_for_invalidate")
        
        invalidated = self.cache_operations.invalidate(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert invalidated is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Exists Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_exists__existing_entry(self):
        """Test checking if an existing entry exists"""
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/exists/{random_string()}")
        data = "data for exists test"
        
        config = Schema__Cache__Decorator__Config(
            namespace = str(namespace),
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
            file_id   = "test-exists"
        )
        
        # Store data
        stored = self.cache_operations.store(
            namespace = namespace,
            cache_key = cache_key,
            data      = data,
            config    = config
        )
        assert stored is True
        
        # Get the cache hash
        from osbot_utils.helpers.cache.Cache__Hash__Generator import Cache__Hash__Generator
        hash_generator = Cache__Hash__Generator()
        cache_hash = Safe_Str__Cache_Hash(hash_generator.from_string(str(cache_key)))
        
        # Check existence
        exists = self.cache_operations.exists(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert exists is True

    def test_exists__nonexistent_entry(self):
        """Test checking if a non-existent entry exists"""
        namespace = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("nonexistent_for_exists")
        
        exists = self.cache_operations.exists(
            namespace  = namespace,
            cache_hash = cache_hash
        )
        
        assert exists is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Status Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_get_client_status(self):
        """Test getting client status"""
        status = self.cache_operations.get_client_status()
        
        assert status["available"] is True
        assert status["mode"] == "IN_MEMORY"
        assert "info" in status

    def test_get_client_status__no_client(self):
        """Test getting status when no client is configured"""
        operations_no_client = Cache__Operations(
            client_cache_service = None
        )
        
        status = operations_no_client.get_client_status()
        
        assert status["available"] is False
        assert status["reason"] == "No client configured"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Different Storage Strategies Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_store_with_direct_strategy(self):
        """Test storing with DIRECT strategy"""
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/direct/{random_string()}")
        data = {"strategy": "direct"}
        
        config = Schema__Cache__Decorator__Config(
            namespace = str(namespace),
            strategy  = Enum__Cache__Store__Strategy.DIRECT,
            file_id   = "test-direct"
        )
        
        stored = self.cache_operations.store(
            namespace = namespace,
            cache_key = cache_key,
            data      = data,
            config    = config
        )
        
        assert stored is True

    def test_store_with_temporal_strategy(self):
        """Test storing with TEMPORAL strategy"""
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/temporal/{random_string()}")
        data = {"strategy": "temporal"}
        
        config = Schema__Cache__Decorator__Config(
            namespace = str(namespace),
            strategy  = Enum__Cache__Store__Strategy.TEMPORAL,
            file_id   = "test-temporal"
        )
        
        stored = self.cache_operations.store(
            namespace = namespace,
            cache_key = cache_key,
            data      = data,
            config    = config
        )
        
        assert stored is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Complex Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_multiple_operations_sequence(self):
        """Test a sequence of store, retrieve, invalidate operations"""
        namespace = self.test_namespace
        
        # Create multiple entries
        entries = []
        for i in range(3):
            cache_key = Safe_Str__File__Path(f"test/sequence/{i}")
            data = f"data_{i}"
            
            config = Schema__Cache__Decorator__Config(
                namespace = str(namespace),
                strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                file_id   = f"test-seq-{i}"
            )
            
            stored = self.cache_operations.store(
                namespace = namespace,
                cache_key = cache_key,
                data      = data,
                config    = config
            )
            
            assert stored is True
            
            from osbot_utils.helpers.cache.Cache__Hash__Generator import Cache__Hash__Generator
            hash_generator = Cache__Hash__Generator()
            cache_hash = Safe_Str__Cache_Hash(hash_generator.from_string(str(cache_key)))
            
            entries.append((cache_hash, data))
        
        # Retrieve all entries
        for cache_hash, expected_data in entries:
            retrieved = self.cache_operations.retrieve(
                namespace   = namespace,
                cache_hash  = cache_hash,
                target_type = str
            )
            assert retrieved == expected_data
        
        # Invalidate middle entry
        invalidated = self.cache_operations.invalidate(
            namespace  = namespace,
            cache_hash = entries[1][0]
        )
        assert invalidated is True
        
        # Verify first and last still exist, middle is gone
        assert self.cache_operations.exists(namespace, entries[0][0]) is True
        assert self.cache_operations.exists(namespace, entries[1][0]) is False
        assert self.cache_operations.exists(namespace, entries[2][0]) is True

    def test_nested_type_safe_objects(self):
        """Test storing and retrieving nested Type_Safe objects"""
        class InnerSchema(Type_Safe):
            inner_value: str = "inner"
            inner_number: int = 42
        
        class OuterSchema(Type_Safe):
            outer_value: str
            inner: InnerSchema
            list_data: list
        
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/nested/{random_string()}")
        data = OuterSchema(
            outer_value = "outer",
            inner       = InnerSchema(inner_value="nested", inner_number=100),
            list_data   = [1, 2, 3]
        )
        
        config = Schema__Cache__Decorator__Config(
            namespace = str(namespace),
            strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
            file_id   = "test-nested"
        )
        
        # Store
        stored = self.cache_operations.store(
            namespace = namespace,
            cache_key = cache_key,
            data      = data,
            config    = config
        )
        assert stored is True
        
        # Retrieve
        from osbot_utils.helpers.cache.Cache__Hash__Generator import Cache__Hash__Generator
        hash_generator = Cache__Hash__Generator()
        cache_hash = Safe_Str__Cache_Hash(hash_generator.from_string(str(cache_key)))
        
        retrieved = self.cache_operations.retrieve(
            namespace   = namespace,
            cache_hash  = cache_hash,
            target_type = OuterSchema
        )
        
        assert isinstance(retrieved, OuterSchema)
        assert retrieved.outer_value == "outer"
        assert isinstance(retrieved.inner, InnerSchema)
        assert retrieved.inner.inner_value == "nested"
        assert retrieved.inner.inner_number == 100
        assert retrieved.list_data == [1, 2, 3]
