from unittest                                                                                      import TestCase
from osbot_utils.testing.__                                                                        import __
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                     import type_safe
from osbot_utils.utils.Objects                                                                     import base_classes
from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe
from mgraph_ai_service_cache_client.client.decorator.Cache__Decorator__Key__Generator              import Cache__Decorator__Key__Generator
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config      import Schema__Cache__Decorator__Config


class test_Cache__Decorator__Key__Generator(TestCase):

    @classmethod
    def setUpClass(cls):                                                    # ONE-TIME setup for all tests
        cls.generator = Cache__Decorator__Key__Generator()

    def test__init__(self):                                                 # Test generator initialization
        with self.generator as _:
            assert type(_)         is Cache__Decorator__Key__Generator
            assert base_classes(_) == [Type_Safe, object]

    def test_generate__basic(self):                                         # Test basic key generation with class and method
        config = Schema__Cache__Decorator__Config(namespace="test", use_class_name=True, use_method_name=True)
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" )
        
        assert cache_key == "TestClass/test_method"                         # No hash when no key_fields

    def test_generate__with_key_fields(self):                               # Test key generation with parameter hashing
        config = Schema__Cache__Decorator__Config(namespace="test", key_fields=["param1", "param2"])
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" ,
                                            param1      = "value1"      ,
                                            param2      = "value2"      )
        
        parts = cache_key.split("/")
        assert parts[0]         == "TestClass"
        assert parts[1]         == "test_method"
        assert len(parts[2])    == 10                                          # Hash is 10 chars
        assert parts            == ['TestClass', 'test_method', 'b9fd29c8b0']

    def test_generate__without_class_name(self):                            # Test key generation without class name
        config = Schema__Cache__Decorator__Config(namespace       = "test",
                                                  use_class_name  = False,
                                                  use_method_name = True)
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" )
        
        assert cache_key == "test_method"                                   # Only method name

    def test_generate__without_method_name(self):                           # Test key generation without method name
        config = Schema__Cache__Decorator__Config(namespace="test", use_class_name=True, use_method_name=False)
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" )
        
        assert cache_key == "TestClass"                                     # Only class name

    def test_generate__flat_namespace(self):                                # Test flat namespace (no class or method)
        config = Schema__Cache__Decorator__Config(namespace="test", use_class_name=False, use_method_name=False, key_fields=["param1"])
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" ,
                                            param1      = "value1"      )
        
        assert len(cache_key) == 10                                         # Only hash (10 chars)
        assert cache_key      == '6ce38f6a45'

    def test_generate__deterministic_hashing(self):                         # Test that same params generate same hash
        config = Schema__Cache__Decorator__Config(namespace="test", key_fields=["param1", "param2"])
        
        key1 = self.generator.generate(config      = config       ,
                                       class_name  = "TestClass"   ,
                                       method_name = "test_method" ,
                                       param1      = "value1"      ,
                                       param2      = "value2"      )
        
        key2 = self.generator.generate(config      = config       ,
                                       class_name  = "TestClass"   ,
                                       method_name = "test_method" ,
                                       param1      = "value1"      ,
                                       param2      = "value2"      )

        assert key1 == key2                                                 # Same params = same key
        assert key1 =="TestClass/test_method/b9fd29c8b0"


    def test__generate__different_params_different_keys(self):               # Test different params generate different keys
        config = Schema__Cache__Decorator__Config(namespace="test", key_fields=["param1"])
        assert config.obj() == __(enabled               = True                            ,
                                  mode                  = 'enabled'                       ,
                                  strategy              = 'key_based'                     ,
                                  use_class_name        = True                            ,
                                  use_method_name       = True                            ,
                                  file_id               = 'response'                      ,
                                  cache_attr_name       = 'decorator__cache'         ,
                                  ttl_seconds           = None                            ,
                                  invalidate_on_error   = False                           ,
                                  namespace             = 'test'                          ,
                                  key_fields            = ['param1']                      )

        assert config.key_fields == ["param1"]
        assert "param1" in config.key_fields

        key1 = self.generator.generate(config      = config       ,
                                       class_name  = "TestClass"   ,
                                       method_name = "test_method" ,
                                       param1      = "value1"      )

        key2 = self.generator.generate(config      = config       ,
                                       class_name  = "TestClass"   ,
                                       method_name = "test_method" ,
                                       param1      = "value2"      )

        assert key2 == 'TestClass/test_method/eac1ca90bb'
        assert key1 == 'TestClass/test_method/6ce38f6a45'
        assert key1 != key2                                                 # Different params = different keys

    def test__extract_key_data__single_field(self):                         # Test extracting single field from params
        params     = {"param1": "value1", "param2": "value2", "param3": "value3"}
        key_fields = ["param1"]
        
        key_data = self.generator._extract_key_data(params, key_fields)
        
        assert key_data == {"param1": "value1"}                             # Only requested field

    def test__extract_key_data__multiple_fields(self):                      # Test extracting multiple fields
        params     = {"param1": "value1", "param2": "value2", "param3": "value3"}
        key_fields = ["param1", "param3"]
        
        key_data = self.generator._extract_key_data(params, key_fields)
        
        assert key_data == {"param1": "value1", "param3": "value3"}         # Only requested fields

    def test__extract_key_data__missing_field(self):                        # Test handling missing field
        params     = {"param1": "value1", "param2": "value2"}
        key_fields = ["param1", "missing_param"]
        
        key_data = self.generator._extract_key_data(params, key_fields)
        
        assert key_data == {"param1": "value1"}                             # Ignores missing field

    def test__serialize_value__primitives(self):                            # Test serialization of primitive types
        assert self.generator._serialize_value("string")   == "string"
        assert self.generator._serialize_value(123     )   == 123
        assert self.generator._serialize_value(45.67   )   == 45.67
        assert self.generator._serialize_value(True    )   == True
        assert self.generator._serialize_value(False   )   == False

    def test__serialize_value__type_safe_object(self):                      # Test serialization of Type_Safe objects
        class TestSchema(Type_Safe):
            field1: str = "value1"
            field2: int = 42
        
        schema = TestSchema()
        serialized = self.generator._serialize_value(schema)
        
        assert serialized == {"field1": "value1", "field2": 42}             # Converted to dict via .obj()

    def test__serialize_value__dict(self):                                  # Test serialization of dictionaries
        test_dict = {"key1": "value1", "key2": 123}
        serialized = self.generator._serialize_value(test_dict)
        
        assert serialized == {"key1": "value1", "key2": 123}

    def test__serialize_value__list(self):                                  # Test serialization of lists
        test_list = ["item1", 123, True]
        serialized = self.generator._serialize_value(test_list)
        
        assert serialized == ["item1", 123, True]

    def test__serialize_value__nested_structures(self):                     # Test serialization of nested data structures
        nested = {
            "outer": {
                "inner": ["value1", "value2"],
                "number": 123
            }
        }
        serialized = self.generator._serialize_value(nested)
        
        assert serialized == nested                                         # Deep structures preserved

    def test__hash_data__deterministic(self):                               # Test hash generation is deterministic
        data = {"param1": "value1", "param2": "value2"}
        
        hash1 = self.generator._hash_data(data)
        hash2 = self.generator._hash_data(data)
        
        assert hash1      == hash2                                           # Same data = same hash
        assert len(hash1) == 10                                              # Hash is 10 chars
        assert hash1      == "b9fd29c8b0"

    def test__hash_data__different_data(self):                              # Test different data produces different hash
        data1 = {"param1": "value1"}
        data2 = {"param1": "value2"}
        
        hash1 = self.generator._hash_data(data1)
        hash2 = self.generator._hash_data(data2)
        
        assert hash1 != hash2                                               # Different data = different hash
        assert hash1 == "6ce38f6a45"
        assert hash2 == "eac1ca90bb"

    def test__hash_data__order_independent(self):                           # Test hash is independent of key order
        data1 = {"param1": "value1", "param2": "value2"}
        data2 = {"param2": "value2", "param1": "value1"}                    # Different order
        
        hash1 = self.generator._hash_data(data1)
        hash2 = self.generator._hash_data(data2)
        
        assert hash1 == hash2                                               # Order doesn't matter (sorted keys)
        assert hash1 == "b9fd29c8b0"

    def test_generate__complex_type_safe_params(self):                      # Test with complex Type_Safe parameters
        class RequestSchema(Type_Safe):
            field1: str = "test"
            field2: int = 123
        
        config  = Schema__Cache__Decorator__Config(namespace="test", key_fields=["request"])
        request = RequestSchema()
        
        key1 = self.generator.generate(config      = config       ,
                                       class_name  = "Service"     ,
                                       method_name = "transform"   ,
                                       request     = request       )
        
        key2 = self.generator.generate(config      = config       ,
                                       class_name  = "Service"     ,
                                       method_name = "transform"   ,
                                       request     = request       )
        
        assert key1 == key2                                                 # Same Type_Safe object = same key
        assert key1 == "Service/transform/00ce41cfbb"
        assert key2 == "Service/transform/00ce41cfbb"

    def test_generate__empty_key_fields(self):                              # Test with empty key_fields (no hashing)
        config = Schema__Cache__Decorator__Config(namespace="test", key_fields=[])
        
        cache_key = self.generator.generate(config      = config       ,
                                            class_name  = "TestClass"   ,
                                            method_name = "test_method" ,
                                            param1      = "value1"      ,
                                            param2      = "value2"      )
        
        assert cache_key == "TestClass/test_method"                         # No hash without key_fields


    def test__regression__type_safe__decorator__params_value(self):

        @type_safe
        def an_method( **params):
            return params

        assert an_method()     == {}
        assert an_method(a=42) == {'a': 42}

        @type_safe
        def an_method_2( **params_2):
            return params_2

        assert an_method_2()     == {}
        assert an_method_2(a=42) == {'a': 42}