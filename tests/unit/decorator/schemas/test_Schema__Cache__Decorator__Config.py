from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from mgraph_ai_service_cache_client.decorator.schemas.Schema__Cache__Decorator__Config      import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.decorator.schemas.enums.Enum__Cache__Decorator__Mode    import Enum__Cache__Decorator__Mode
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy


class test_Schema__Cache__Decorator__Config(TestCase):

    def test__init__(self):                                                 # Test auto-initialization and defaults
        with Schema__Cache__Decorator__Config(namespace="test-namespace") as _:
            assert type(_)                      is Schema__Cache__Decorator__Config
            assert base_classes(_)              == [Type_Safe, object]
            
            # Verify Type_Safe attribute types
            assert type(_.namespace)            is Safe_Str__Id
            assert type(_.enabled)              is bool
            assert type(_.mode)                 is Enum__Cache__Decorator__Mode
            assert type(_.strategy)             is Enum__Cache__Store__Strategy
            assert type(_.key_fields)           is Type_Safe__List
            assert type(_.use_class_name)       is bool
            assert type(_.use_method_name)      is bool
            assert type(_.file_id)              is str
            assert type(_.cache_attr_name)      is str
            assert _.ttl_seconds                is None                     # Optional field
            assert type(_.cache_none_results)   is bool
            assert type(_.invalidate_on_error)  is bool

    def test__init__defaults(self):                                         # Test default values match specification
        with Schema__Cache__Decorator__Config(namespace="test") as _:
            assert _.namespace              == "test"                       # Required field
            assert _.enabled                == True                         # Default: enabled
            assert _.mode                   == Enum__Cache__Decorator__Mode.ENABLED
            assert _.strategy               == Enum__Cache__Store__Strategy.KEY_BASED
            assert _.key_fields             == []                           # Default: empty list
            assert _.use_class_name         == True                         # Default: include class
            assert _.use_method_name        == True                         # Default: include method
            assert _.file_id                == "response"                   # Default file_id
            assert _.cache_attr_name        == "decorator__cache"       # Default cache client name
            assert _.ttl_seconds            is None                         # Default: no expiry
            assert _.cache_none_results     == False                        # Default: don't cache None
            assert _.invalidate_on_error    == False                        # Default: keep cache on error

    def test__obj(self):                                                    # Test .obj() serialization
        with Schema__Cache__Decorator__Config(namespace="test-namespace") as _:
            assert _.obj() == __(namespace            = "test-namespace"                        ,
                                 enabled              = True                                    ,
                                 mode                 = Enum__Cache__Decorator__Mode.ENABLED    ,
                                 strategy             = Enum__Cache__Store__Strategy.KEY_BASED  ,
                                 key_fields           = []                                      ,
                                 use_class_name       = True                                    ,
                                 use_method_name      = True                                    ,
                                 file_id              = "response"                              ,
                                 cache_attr_name      = "decorator__cache"                  ,
                                 ttl_seconds          = None                                    ,
                                 cache_none_results   = False                                   ,
                                 invalidate_on_error  = False                                   )

    def test__with_custom_values(self):                                     # Test setting custom configuration values
        with Schema__Cache__Decorator__Config(namespace             = "custom-namespace"                   ,
                                              enabled               = False                                ,
                                              mode                  = Enum__Cache__Decorator__Mode.DISABLED,
                                              key_fields            = ["field1", "field2"]                 ,
                                              use_class_name        = False                                ,
                                              use_method_name       = False                                ,
                                              file_id               = "custom-response"                    ,
                                              cache_attr_name       = "my_cache"                           ,
                                              ttl_seconds           = Safe_UInt(3600)                      ,
                                              cache_none_results    = True                                 ,
                                              invalidate_on_error   = True                                 ) as _:
            
            assert _.namespace              == "custom-namespace"
            assert _.enabled                == False
            assert _.mode                   == Enum__Cache__Decorator__Mode.DISABLED
            assert _.key_fields             == ["field1", "field2"]
            assert _.use_class_name         == False
            assert _.use_method_name        == False
            assert _.file_id                == "custom-response"
            assert _.cache_attr_name        == "my_cache"
            assert _.ttl_seconds            == 3600
            assert _.cache_none_results     == True
            assert _.invalidate_on_error    == True

    def test__namespace_validation(self):                                   # Test namespace type safety
        # Valid namespace formats
        config1 = Schema__Cache__Decorator__Config(namespace="semantic-text")
        assert config1.namespace == "semantic-text"
        
        config2 = Schema__Cache__Decorator__Config(namespace="semantic-text/transformations")               # namespace is Safe_Str__Id
        assert config2.namespace == "semantic-text_transformations"
        
        config3 = Schema__Cache__Decorator__Config(namespace="semantic-text/transformations/v1")        # namespace is Safe_Str__Id
        assert config3.namespace == "semantic-text_transformations_v1"

    def test__key_fields_variations(self):                                  # Test various key_fields configurations
        # Empty key_fields (default)
        config1 = Schema__Cache__Decorator__Config(namespace="test", key_fields=[])
        assert config1.key_fields == []
        
        # Single field
        config2 = Schema__Cache__Decorator__Config(namespace="test", key_fields=["param1"])
        assert config2.key_fields == ["param1"]
        
        # Multiple fields
        config3 = Schema__Cache__Decorator__Config(namespace="test", key_fields=["param1", "param2", "param3"])
        assert config3.key_fields == ["param1", "param2", "param3"]

    def test__mode_configurations(self):                                    # Test all cache decorator modes
        # ENABLED mode
        config1 = Schema__Cache__Decorator__Config(namespace="test", mode=Enum__Cache__Decorator__Mode.ENABLED)
        assert config1.mode == Enum__Cache__Decorator__Mode.ENABLED
        
        # DISABLED mode
        config2 = Schema__Cache__Decorator__Config(namespace="test", mode=Enum__Cache__Decorator__Mode.DISABLED)
        assert config2.mode == Enum__Cache__Decorator__Mode.DISABLED
        
        # READ_ONLY mode
        config3 = Schema__Cache__Decorator__Config(namespace="test", mode=Enum__Cache__Decorator__Mode.READ_ONLY)
        assert config3.mode == Enum__Cache__Decorator__Mode.READ_ONLY

    def test__ttl_configurations(self):                                     # Test TTL (time-to-live) settings
        # No TTL (None)
        config1 = Schema__Cache__Decorator__Config(namespace="test", ttl_seconds=None)
        assert config1.ttl_seconds is None
        
        # 1 hour TTL
        config2 = Schema__Cache__Decorator__Config(namespace="test", ttl_seconds=Safe_UInt(3600))
        assert config2.ttl_seconds == 3600
        
        # 1 day TTL
        config3 = Schema__Cache__Decorator__Config(namespace="test", ttl_seconds=Safe_UInt(86400))
        assert config3.ttl_seconds == 86400
        
        # 1 week TTL
        config4 = Schema__Cache__Decorator__Config(namespace="test", ttl_seconds=Safe_UInt(604800))
        assert config4.ttl_seconds == 604800

    def test__json_roundtrip(self):                                         # Test JSON serialization and deserialization
        original = Schema__Cache__Decorator__Config(namespace              = "test-roundtrip"                      ,
                                enabled                = False                                 ,
                                mode                   = Enum__Cache__Decorator__Mode.READ_ONLY,
                                key_fields             = ["field1", "field2"]                  ,
                                ttl_seconds            = Safe_UInt(7200)                       ,
                                cache_none_results     = True                                  )
        
        json_data = original.json()                                         # Serialize to JSON
        restored  = Schema__Cache__Decorator__Config.from_json(json_data)                      # Deserialize from JSON
        
        # Verify all fields preserved
        assert restored.namespace           == original.namespace
        assert restored.enabled             == original.enabled
        assert restored.mode                == original.mode
        assert restored.key_fields          == original.key_fields
        assert restored.ttl_seconds         == original.ttl_seconds
        assert restored.cache_none_results  == original.cache_none_results
        assert restored.json()              == json_data
        assert restored.obj ()              == original.obj()

    def test__path_generation_flags(self):                                  # Test cache path generation configuration
        # Both enabled (default)
        config1 = Schema__Cache__Decorator__Config(namespace="test", use_class_name=True, use_method_name=True)
        assert config1.use_class_name   == True
        assert config1.use_method_name  == True
        
        # Only class name
        config2 = Schema__Cache__Decorator__Config(namespace="test", use_class_name=True, use_method_name=False)
        assert config2.use_class_name   == True
        assert config2.use_method_name  == False
        
        # Only method name
        config3 = Schema__Cache__Decorator__Config(namespace="test", use_class_name=False, use_method_name=True)
        assert config3.use_class_name   == False
        assert config3.use_method_name  == True
        
        # Neither (flat namespace)
        config4 = Schema__Cache__Decorator__Config(namespace="test", use_class_name=False, use_method_name=False)
        assert config4.use_class_name   == False
        assert config4.use_method_name  == False
