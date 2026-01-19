import pytest
from unittest                                                                                       import TestCase
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                                import Serverless__Fast_API__Config
from osbot_utils.helpers.cache.Cache__Hash__Generator                                               import Cache__Hash__Generator
from osbot_utils.testing.__                                                                         import __, __SKIP__
from osbot_utils.testing.__helpers                                                                  import obj
from osbot_utils.utils.Objects                                                                      import base_classes
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash            import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                   import Safe_Str__File__Path
from osbot_utils.utils.Misc                                                                         import random_string, random_bytes
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                       import Cache_Service__Fast_API
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Decorator__Operations  import Cache__Decorator__Operations
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config       import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Data         import Schema__Cache__Decorator__Data
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Metadata                           import Schema__Cache__Metadata
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
        cls.client_cache_service = Client__Cache__Service(config=client_config)                                           # Create cache client
        cls.cache_operations     = Cache__Decorator__Operations(client_cache_service = cls.client_cache_service)  # Create Cache__Operations instance
        cls.test_namespace       = Safe_Str__Id("test-operations")          # Test namespace
        cls.hash_generator       = Cache__Hash__Generator()     # todo: see if we shouldn't move this to the Cache__Operations

    def test__init__(self):
        with self.cache_operations as _:
            assert type(_) is Cache__Decorator__Operations
            assert base_classes(_)           == [Type_Safe, object]
            assert _.client_cache_service    is not None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Store and Retrieve Tests (using real cache)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_store_and_retrieve__string(self):              # Test storing and retrieving a string value
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/string/{random_string()}")
        data      = "test string value"

        cache_hash     = self.hash_generator.from_string(cache_key)                                          # Get the cache hash for retrieval
        
        config = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                  strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                  file_id   = "test-string"                         )

        stored = self.cache_operations.store(namespace = namespace,                 # Store data
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )

        retrieved = self.cache_operations.retrieve(namespace   = namespace                    ,       # Retrieve data from Cache Operations
                                                   cache_hash  = cache_hash                   )       # for this hash

        direct    = (self.client_cache_service.client ()                            # Retrieve data directly from cache
                                              .retrieve()
                                              .retrieve__hash__cache_hash__json(cache_hash=cache_hash, namespace=namespace))
        assert stored    is True
        assert retrieved == data
        assert retrieved == direct.get('data')

        # check metadata
        metadata    = (self.client_cache_service.client ()                            # Retrieve data directly from cache
                                                .retrieve()
                                                .retrieve__hash__cache_hash__metadata(cache_hash=cache_hash, namespace=namespace))
        cache_id = metadata.cache_id
        assert type(metadata) is Schema__Cache__Metadata
        assert metadata.obj() == __(cache_id    = cache_id,
                                    cache_hash  = cache_hash,
                                    cache_key   = cache_key,
                                    file_id     ='test-string',
                                    namespace   ='test-operations',
                                    strategy    ='key_based',
                                    stored_at   = __SKIP__,
                                    file_type   = 'json',
                                    content_encoding = None,
                                    content_size     = 0)

        # check refs_hash
        refs_hash = (self.client_cache_service.client ()                            # Retrieve data directly from cache
                                                .retrieve()
                                                .retrieve__hash__cache_hash__refs_hash(cache_hash=cache_hash, namespace=namespace))
        assert type(refs_hash) is dict
        assert obj(refs_hash) == __(cache_hash     = cache_hash,
                                    cache_ids      = [__(cache_id=cache_id,
                                                         timestamp=__SKIP__)],
                                    latest_id      = cache_id,
                                    total_versions = 1)

        # check cache_id
        cache_id_data = (self.client_cache_service.client ()                            # Retrieve data directly from cache
                                                  .retrieve()
                                                  .retrieve__hash__cache_hash__cache_id(cache_hash=cache_hash, namespace=namespace))
        assert type(cache_id_data) is dict
        assert obj(cache_id_data) == __(cache_hash     = cache_hash,
                                        cache_id      = cache_id,
                                        namespace = namespace)



    def test_store_and_retrieve__dict(self):                        # Test storing and retrieving a dictionary
        namespace  = self.test_namespace
        cache_key  = Safe_Str__File__Path(f"test/dict/{random_string()}")
        data       = {"key1": "value1", "key2": 42, "nested": {"inner": "value"}}
        cache_hash = self.hash_generator.from_string(cache_key)                                    # Get the cache hash
        config     = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-dict"                           )

        stored = self.cache_operations.store(namespace = namespace,                                 # Store data
                                             cache_key = cache_key,
                                             data      = data,
                                             config    = config)


        retrieved = self.cache_operations.retrieve(namespace   = namespace                      ,       # Retrieve data
                                                   cache_hash  = cache_hash                     )       # from this hash

        direct    = (self.client_cache_service.client ()                                        # Retrieve data directly from cache
                                             .retrieve()
                                             .retrieve__hash__cache_hash__json(cache_hash=cache_hash, namespace=namespace))
        assert stored           is True
        assert type(retrieved)  is dict
        assert type(data     )  is dict
        assert type(direct   )  is dict
        assert retrieved        == data                                                         # retrieved data matches the original data stored
        assert retrieved        == direct.get('data')                                           # retrieved data matches the data value from the object we get from directly from the cache service

        decorator_data = Schema__Cache__Decorator__Data.from_json(direct)
        assert decorator_data.json() == direct
        assert decorator_data.obj() == __( cache_key        = cache_key ,
                                           data             =__(key1 ='value1', key2=42, nested=__(inner='value')),
                                           type_safe_class  = None,
                                           data_type        = 'json',
                                           timestamp        = __SKIP__)

    def test_store_and_retrieve__type_safe_object(self):        # Test storing and retrieving a Type_Safe object

        namespace  = self.test_namespace
        cache_key  = Safe_Str__File__Path(f"test/typesafe/{random_string()}")

        data       = TestSchema(field1 = "test"             ,
                                field2 = 42                 ,
                                field3 = {"nested": "value"})
        cache_hash = self.hash_generator.from_string(cache_key)
        config     = Schema__Cache__Decorator__Config(namespace = namespace                             ,
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-typesafe"                       )

        stored      = self.cache_operations.store(namespace = namespace  ,                               # Store data using the Cache Operations
                                                  cache_key = cache_key  ,
                                                  data      = data       ,
                                                  config    = config     )
        retrieved   = self.cache_operations.retrieve(namespace       = namespace  ,   # Retrieve data via cache_operations
                                                     cache_hash      = cache_hash )      # for this hash

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
        assert retrieved.json()  == direct_json.get('data')                                         # confirm that the direct_json matches the new object created


    def test_retrieve__not_found(self):                         # Test retrieving non-existent data
        namespace = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("aaaaa12345")

        for data_type in Enum__Cache__Data_Type.__members__:
            retrieved = self.cache_operations.retrieve(namespace   = namespace  ,
                                                       cache_hash  = cache_hash )
        
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


    # ═══════════════════════════════════════════════════════════════════════════════
    # Invalidation Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_invalidate__existing_entry(self):  # Test invalidating an existing cache entry
        namespace  = self.test_namespace
        cache_key  = f"test/invalidate/{random_string()}"
        data       = "data to invalidate"
        cache_hash = self.hash_generator.from_string(cache_key)
        config     = Schema__Cache__Decorator__Config(namespace = str(namespace),
                                                      strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                      file_id   = "test-invalidate")
        stored     = self.cache_operations.store(namespace = namespace,                     # First, store data
                                                 cache_key = cache_key,
                                                 data      = data     ,
                                                 config    = config   )
        assert stored is True

        retrieved = self.cache_operations.retrieve(namespace  = namespace                    ,             # Verify it exists
                                                   cache_hash = cache_hash                   )
        assert retrieved == data

        # Invalidate it
        invalidated = self.cache_operations.invalidate(namespace  = namespace,
                                                       cache_hash = cache_hash)
        assert invalidated is True

        # Verify it's gone
        retrieved_after = self.cache_operations.retrieve(namespace   = namespace,
                                                         cache_hash  = cache_hash)
        assert retrieved_after is None

    def test_invalidate__nonexistent_entry(self):                                   # Test invalidating a non-existent cache entry
        namespace  = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("aaaaa12345")

        invalidated = self.cache_operations.invalidate(namespace  = namespace ,
                                                       cache_hash = cache_hash)

        assert invalidated is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Exists Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_exists__existing_entry(self):                                          # Test checking if an existing entry exists
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/exists/{random_string()}")
        data      = "data for exists test"
        config    = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                     strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                     file_id   = "test-exists"                         )

        stored = self.cache_operations.store(namespace = namespace,                                     # Store data
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )
        assert stored is True

        cache_hash = Safe_Str__Cache_Hash(self.hash_generator.from_string(cache_key))                        # Get the cache hash from DATA (not cache_key)

        exists = self.cache_operations.exists(namespace  = namespace ,                                  # Check existence
                                              cache_hash = cache_hash)

        assert exists is True

    def test_exists__nonexistent_entry(self):                                       # Test checking if a non-existent entry exists
        namespace  = self.test_namespace
        cache_hash = Safe_Str__Cache_Hash("aaaaa12345")
        exists     = self.cache_operations.exists(namespace  = namespace ,
                                                  cache_hash = cache_hash)

        assert exists is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Status Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_client_status(self):                                               # Test getting client status
        status = self.cache_operations.get_client_status()

        assert status["available"] is True
        assert status["mode"]      == str(Enum__Client__Mode.IN_MEMORY)             # Compare with enum string value
        assert "info" in status

    # ═══════════════════════════════════════════════════════════════════════════════
    # Different Storage Strategies Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_store_with_direct_strategy(self):                                      # Test storing with DIRECT strategy
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/direct/{random_string()}")
        data      = {"strategy": "direct"}

        config = Schema__Cache__Decorator__Config(namespace = str(namespace)                      ,
                                                  strategy  = Enum__Cache__Store__Strategy.DIRECT ,
                                                  file_id   = "test-direct"                       )

        stored = self.cache_operations.store(namespace = namespace,
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )

        assert stored is True

    def test_store_with_temporal_strategy(self):                                    # Test storing with TEMPORAL strategy
        namespace = self.test_namespace
        cache_key = Safe_Str__File__Path(f"test/temporal/{random_string()}")
        data      = {"strategy": "temporal"}

        config = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                  strategy  = Enum__Cache__Store__Strategy.TEMPORAL ,
                                                  file_id   = "test-temporal"                       )

        stored = self.cache_operations.store(namespace = namespace,
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )

        assert stored is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Complex Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_multiple_operations_sequence(self):                                    # Test a sequence of store, retrieve, invalidate operations
        namespace = self.test_namespace

        entries = []                                                                # Create multiple entries
        for i in range(3):
            cache_key = Safe_Str__File__Path(f"test/sequence/{i}")
            data      = f"data_{i}"
            config    = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                         strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                         file_id   = f"test-seq-{i}"                       )

            stored = self.cache_operations.store(namespace = namespace,
                                                 cache_key = cache_key,
                                                 data      = data     ,
                                                 config    = config   )

            assert stored is True

            cache_hash = Safe_Str__Cache_Hash(self.hash_generator.from_string(cache_key))                # Hash the DATA, not the cache_key

            entries.append((cache_hash, data))

        for cache_hash, expected_data in entries:                                                   # Retrieve all entries
            retrieved = self.cache_operations.retrieve(namespace  = namespace                    ,
                                                       cache_hash = cache_hash                   )
            assert retrieved == expected_data

        invalidated = self.cache_operations.invalidate(namespace  = namespace     ,                 # Invalidate middle entry
                                                       cache_hash = entries[1][0] )
        assert invalidated is True

        assert self.cache_operations.exists(namespace, entries[0][0]) is True                       # Verify first and last still exist, middle is gone
        assert self.cache_operations.exists(namespace, entries[1][0]) is False
        assert self.cache_operations.exists(namespace, entries[2][0]) is True

    def test_nested_type_safe_objects(self):                                        # Test storing and retrieving nested Type_Safe objects

        namespace = self.test_namespace
        cache_key = f"test/nested/{random_string()}"
        data      = OuterSchema(outer_value = "outer"                                         ,
                                inner       = InnerSchema(inner_value="nested", inner_number=100),
                                list_data   = [1, 2, 3]                                       )

        assert data.obj() == __(outer_value = 'outer',
                                inner       = __(inner_value='nested', inner_number=100),
                                list_data  = [1, 2, 3])

        config = Schema__Cache__Decorator__Config(namespace = str(namespace)                        ,
                                                  strategy  = Enum__Cache__Store__Strategy.KEY_BASED,
                                                  file_id   = "test-nested"                         )

        stored = self.cache_operations.store(namespace = namespace,                                 # Store
                                             cache_key = cache_key,
                                             data      = data     ,
                                             config    = config   )
        assert stored is True

        cache_hash = self.hash_generator.from_string(cache_key)

        retrieved = self.cache_operations.retrieve(namespace       = namespace                       ,  # Retrieve
                                                   cache_hash      = cache_hash                      )

        assert type(retrieved) is OuterSchema
        assert isinstance(retrieved, OuterSchema)
        assert retrieved.outer_value       == "outer"
        assert isinstance(retrieved.inner, InnerSchema)
        assert retrieved.inner.inner_value == "nested"
        assert retrieved.inner.inner_number == 100
        assert retrieved.list_data         == [1, 2, 3]


# test classes (need to put them here because they can't be inner classes)

class TestSchema(Type_Safe):
    field1: str
    field2: int
    field3: dict

class InnerSchema(Type_Safe):
    inner_value : str = "inner"
    inner_number: int = 42

class OuterSchema(Type_Safe):
    outer_value: str
    inner      : InnerSchema
    list_data  : list