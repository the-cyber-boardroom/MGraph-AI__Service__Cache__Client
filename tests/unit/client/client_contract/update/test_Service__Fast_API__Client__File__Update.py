from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash                    import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now                            import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from osbot_utils.utils.Objects                                                                              import base_classes
from mgraph_ai_service_cache_client.client.client_contract.update.Service__Fast_API__Client__File__Update   import Service__Fast_API__Client__File__Update
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Update__Response                           import Schema__Cache__Update__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy                        import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__File__Refs                            import Schema__Cache__File__Refs
from tests.unit.Cache_Client__Fast_API__Test_Objs                                                           import client_cache_service


class test_Service__Fast_API__Client__File__Update(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # ONE-TIME expensive setup
        #cls.test_objs      = setup__service__fast_api_client__test_objs()           # Setup test objects
        #cls.client         = cls.test_objs.client                                    # Main API client
        cls.client_cache_service, cls.cache_service = client_cache_service()
        cls.update_client   = cls.client_cache_service.update()
        cls.store_client    = cls.client_cache_service.store()                                 # Store client for creating test entries
        cls.retrieve_client = cls.client_cache_service.retrieve()
        cls.test_namespace  = Safe_Str__Id("test-client-update")

        # Test data versions
        cls.test_string_v1 = "original string data"
        cls.test_string_v2 = "updated string data"
        cls.test_json_v1   = {"version": 1, "status": "original"}
        cls.test_json_v2   = {"version": 2, "status": "updated"}
        cls.test_binary_v1 = bytes(range(10))
        cls.test_binary_v2 = bytes(range(20, 30))

    def _create_test_entry(self, data, strategy=Enum__Cache__Store__Strategy.TEMPORAL):  # Helper to create initial test entries
        if isinstance(data, bytes):                                                  # Store based on data type
            result = self.store_client.store__binary(
                strategy  = strategy,
                namespace = self.test_namespace,
                body      = data
            )
        elif isinstance(data, dict):
            result = self.store_client.store__json(
                strategy  = strategy,
                namespace = self.test_namespace,
                body      = data
            )
        else:
            result = self.store_client.store__string(
                strategy  = strategy,
                namespace = self.test_namespace,
                body      = data
            )
        return result

    def test__init__(self):                                                          # Test initialization
        with self.update_client as _:
            assert type(_) is Service__Fast_API__Client__File__Update
            assert base_classes(_) == [Type_Safe, object]
            assert _._client is self.client_cache_service

            assert _.obj() == __(_client = __SKIP__)                                # _client is the main client reference

    def test_requests(self):                                                         # Test requests property
        with self.update_client as _:
            requests = _.requests

            assert requests is not None
            assert callable(requests.execute)                                        # Has execute method

    def test_update__string(self):                                                   # Test string update
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_string_v1)           # Create initial entry
            cache_id      = create_result.cache_id
            cache_hash    = create_result.cache_hash

            update_result = _.update__string(cache_id  = cache_id             ,    # Update entry
                                            namespace = self.test_namespace   ,
                                            body      = self.test_string_v2   )

            assert type(update_result) is Schema__Cache__Update__Response
            assert update_result.cache_id         == cache_id                       # Same ID
            assert update_result.cache_hash       == cache_hash                     # V1: hash unchanged
            assert type(update_result.cache_hash) is Safe_Str__Cache_Hash
            assert update_result.namespace        == self.test_namespace
            assert update_result.updated_content  == True                           # Content updated
            assert update_result.updated_hash     == False                          # V1: hash not updated
            assert update_result.updated_metadata == False                          # V1: metadata not updated
            assert update_result.updated_id_ref   == False                          # V1: ID ref not updated

            # Verify content actually updated
            retrieve_result = self.retrieve_client.retrieve__cache_id(cache_id  = str(cache_id),
                                                                      namespace = str(self.test_namespace))
            assert retrieve_result.data == self.test_string_v2

    def test_update__json(self):                                                     # Test JSON update
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_json_v1)             # Create initial entry
            cache_id      = create_result.cache_id
            cache_hash    = create_result.cache_hash

            update_result = _.update__json(cache_id  = cache_id             ,      # Update entry
                                          namespace = self.test_namespace   ,
                                          body      = self.test_json_v2     )

            assert type(update_result) is Schema__Cache__Update__Response
            assert update_result.cache_id   == cache_id                             # Same ID
            assert update_result.cache_hash == cache_hash                           # V1: hash unchanged
            assert update_result.namespace  == self.test_namespace
            assert update_result.updated_content == True

            # Verify content actually updated
            retrieve_result = self.retrieve_client.retrieve__cache_id(cache_id  = str(cache_id),
                                                                      namespace = str(self.test_namespace))
            assert retrieve_result.data == self.test_json_v2

    def test_update__binary(self):                                                   # Test binary update
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_binary_v1)           # Create initial entry
            cache_id      = create_result.cache_id
            cache_hash    = create_result.cache_hash

            update_result = _.update__binary(cache_id  = cache_id             ,    # Update entry
                                            namespace = self.test_namespace   ,
                                            body      = self.test_binary_v2   )

            assert type(update_result) is Schema__Cache__Update__Response
            assert update_result.cache_id   == cache_id                             # Same ID
            assert update_result.cache_hash == cache_hash                           # V1: hash unchanged
            assert update_result.namespace  == self.test_namespace
            assert update_result.size       == len(self.test_binary_v2)
            assert update_result.updated_content == True

            # Verify content actually updated
            retrieve_result = self.retrieve_client.retrieve__cache_id__binary(
                cache_id  = str(cache_id),
                namespace = str(self.test_namespace)
            )
            assert retrieve_result == self.test_binary_v2

    def test_update__string__empty_data(self):                                       # Test update with empty string
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_string_v1)
            cache_id      = create_result.cache_id

            try:                                                                    # Should raise error for empty data
                _.update__string(cache_id  = cache_id             ,
                                namespace = self.test_namespace   ,
                                body      = ""                    )
                assert False, "Should have raised exception for empty data"
            except Exception as e:
                assert "empty" in str(e).lower() or "invalid" in str(e).lower()

    def test_update__binary__empty_data(self):                                       # Test update with empty binary
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_binary_v1)
            cache_id      = create_result.cache_id

            try:                                                                    # Should raise error for empty data
                _.update__binary(cache_id  = cache_id             ,
                                namespace = self.test_namespace   ,
                                body      = b""                   )
                assert False, "Should have raised exception for empty data"
            except Exception as e:
                assert "empty" in str(e).lower() or "invalid" in str(e).lower()

    def test_update__nonexistent_entry(self):                                        # Test updating non-existent entry
        with self.update_client as _:
            nonexistent_id = Cache_Id(Random_Guid())


            result = _.update__string(cache_id  = nonexistent_id       ,
                                      namespace = self.test_namespace   ,
                                      body      = "some data"           )
            assert type(result) is Schema__Cache__Update__Response
            assert result.obj() == __( cache_id=__SKIP__,                           # todo: BUG at least this should be the cache_id provided, but look at a better way to handle this (maybe add the status and message variables)
                                       cache_hash='',
                                       namespace='',
                                       paths=[],
                                       size=0,
                                       timestamp=__SKIP__,
                                       updated_content=False,
                                       updated_hash=False,
                                       updated_metadata=False,
                                       updated_id_ref=False)

            assert result.cache_id != nonexistent_id                                # todo: BUG: see why this is happening


    def test_update__multiple_sequential_updates(self):                              # Test multiple updates on same entry
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_string_v1)           # Create initial entry
            cache_id      = create_result.cache_id
            cache_hash    = create_result.cache_hash

            # First update
            update_1 = _.update__string(cache_id  = cache_id             ,
                                       namespace = self.test_namespace   ,
                                       body      = "second version"      )
            assert update_1.cache_id   == cache_id
            assert update_1.cache_hash == cache_hash                                # V1: hash unchanged

            # Second update
            update_2 = _.update__string(cache_id  = cache_id             ,
                                       namespace = self.test_namespace   ,
                                       body      = "third version"       )
            assert update_2.cache_id   == cache_id
            assert update_2.cache_hash == cache_hash                                # V1: hash still unchanged

            # Verify final content
            retrieve_result = self.retrieve_client.retrieve__cache_id(
                cache_id  = str(cache_id),
                namespace = str(self.test_namespace)
            )
            assert retrieve_result.data == "third version"

    def test_update__preserves_strategy(self):                                       # Test that update preserves storage strategy
        with self.update_client as _:
            # Create with specific strategy
            create_result = self._create_test_entry(data     = self.test_json_v1,
                                                    strategy = Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED)
            cache_id = create_result.cache_id

            # Update entry
            update_result = _.update__json(cache_id  = cache_id             ,
                                           namespace = self.test_namespace  ,
                                           body      = self.test_json_v2    )

            assert update_result.cache_id == cache_id

            # Verify strategy preserved via config
            refs = self.retrieve_client.retrieve__cache_id__refs(cache_id  = str(cache_id),
                                                                   namespace = str(self.test_namespace))
            assert type(refs) is Schema__Cache__File__Refs
            assert refs.strategy == 'temporal_versioned'

    def test_update__all_strategies(self):                                           # Test updates work with all strategies
        strategies = [  Enum__Cache__Store__Strategy.DIRECT             ,
                        Enum__Cache__Store__Strategy.TEMPORAL           ,
                        Enum__Cache__Store__Strategy.TEMPORAL_LATEST    ,
                        Enum__Cache__Store__Strategy.TEMPORAL_VERSIONED ]

        with self.update_client as _:
            for strategy in strategies:
                namespace = Safe_Str__Id(f"upd-client-{strategy.value}")

                # Create with strategy
                if isinstance(self.test_string_v1, bytes):
                    create_result = self.store_client.store__binary(
                        strategy  = strategy,
                        namespace = namespace,
                        body      = self.test_string_v1
                    )
                else:
                    create_result = self.store_client.store__string(
                        strategy  = strategy,
                        namespace = namespace,
                        body      = self.test_string_v1
                    )
                cache_id = create_result.cache_id

                # Update via client
                update_result = _.update__string(cache_id  = cache_id          ,
                                                namespace = namespace          ,
                                                body      = self.test_string_v2)

                assert update_result.cache_id  == cache_id
                assert update_result.namespace == namespace

                # Verify strategy preserved
                refs = self.retrieve_client.retrieve__cache_id__refs(cache_id  = str(cache_id),
                                                                     namespace = str(namespace))
                assert refs.strategy == strategy.value

    def test_update__response_structure(self):                                       # Test response has all expected fields
        with self.update_client as _:
            create_result = self._create_test_entry(self.test_json_v1)
            cache_id      = create_result.cache_id

            update_result = _.update__json(cache_id  = cache_id             ,
                                          namespace = self.test_namespace   ,
                                          body      = self.test_json_v2     )

            # Verify all response fields present
            assert hasattr(update_result, 'cache_id')
            assert hasattr(update_result, 'cache_hash')
            assert hasattr(update_result, 'namespace')
            assert hasattr(update_result, 'paths')
            assert hasattr(update_result, 'size')
            assert hasattr(update_result, 'timestamp')
            assert hasattr(update_result, 'updated_content')
            assert hasattr(update_result, 'updated_hash')
            assert hasattr(update_result, 'updated_metadata')
            assert hasattr(update_result, 'updated_id_ref')

            # Verify field types
            assert type(update_result.cache_id)         is Cache_Id
            assert type(update_result.cache_hash)       is Safe_Str__Cache_Hash
            assert type(update_result.namespace)        is Safe_Str__Id
            assert type(update_result.size)             is Safe_UInt
            assert type(update_result.timestamp)        is Timestamp_Now
            assert type(update_result.updated_content)  is bool
            assert type(update_result.updated_hash)     is bool
            assert type(update_result.updated_metadata) is bool
            assert type(update_result.updated_id_ref)   is bool