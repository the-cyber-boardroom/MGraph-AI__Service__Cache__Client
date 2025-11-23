from unittest                                                                                     import TestCase
from osbot_utils.testing.__                                                                       import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.utils.Objects                                                                    import base_classes
from osbot_utils.type_safe.Type_Safe                                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier   import Safe_Str__Python__Identifier
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Json__Field_Path     import Safe_Str__Json__Field_Path
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Key__Builder         import Cache__Key__Builder
from mgraph_ai_service_cache_client.client.decorator.schemas.Schema__Cache__Decorator__Config     import Schema__Cache__Decorator__Config


class test_Cache__Key__Builder(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_builder = Cache__Key__Builder()

    def test__init__(self):
        with self.key_builder as _:
            assert type(_)         is Cache__Key__Builder
            assert base_classes(_) == [Type_Safe, object]
            assert _.hash_generator is not None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Basic Key Building Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_build_cache_key__basic(self):
        config = Schema__Cache__Decorator__Config(namespace      = "test",
                                                 use_class_name  = True,
                                                 use_method_name = True)
        
        cache_key = self.key_builder.build_cache_key(config      = config,
                                                     class_name  = Safe_Str__Python__Identifier("TestClass"),
                                                     method_name = Safe_Str__Python__Identifier("test_method"),
                                                     params      = {}   )
        assert type(cache_key) is Safe_Str__File__Path
        assert cache_key       == "TestClass/test_method"

    def test_build_cache_key__with_key_fields(self):
        config = Schema__Cache__Decorator__Config(
            namespace  = "test",
            key_fields = ["param1", "param2"]
        )
        
        cache_key = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {"param1": "value1", "param2": "value2"}
        )
        assert type(cache_key) is Safe_Str__File__Path
        assert cache_key       == "TestClass/test_method/b9fd29c8b0"

        parts = str(cache_key).split("/")
        assert parts[0]      == "TestClass"
        assert parts[1]      == "test_method"
        assert len(parts[2]) == 10  # Hash is 10 chars
        assert parts         == ['TestClass', 'test_method', 'b9fd29c8b0']


    def test_build_cache_key__without_class_name(self):
        config = Schema__Cache__Decorator__Config(
            namespace       = "test",
            use_class_name  = False,
            use_method_name = True
        )
        
        cache_key = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {}
        )
        
        assert cache_key == "test_method"

    def test_build_cache_key__without_method_name(self):
        config = Schema__Cache__Decorator__Config(
            namespace       = "test",
            use_class_name  = True,
            use_method_name = False
        )
        
        cache_key = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {}
        )
        
        assert str(cache_key) == "TestClass"

    def test_build_cache_key__flat_namespace(self):
        config = Schema__Cache__Decorator__Config(
            namespace       = "test",
            use_class_name  = False,
            use_method_name = False,
            key_fields      = ["param1"]
        )
        
        cache_key = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {"param1": "value1"}
        )
        
        assert len(str(cache_key)) == 10  # Only hash
        assert cache_key           == "6ce38f6a45"

    def test_build_cache_key__deterministic(self):
        config = Schema__Cache__Decorator__Config(
            namespace  = "test",
            key_fields = ["param1", "param2"]
        )
        
        params = {"param1": "value1", "param2": "value2"}
        
        key1 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = params
        )
        
        key2 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = params
        )
        
        assert key1 == key2  # Same params = same key

        assert key1 == "TestClass/test_method/b9fd29c8b0"


    def test_build_cache_key__different_params_different_keys(self):
        config = Schema__Cache__Decorator__Config(
            namespace  = "test",
            key_fields = ["param1"]
        )
        
        key1 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {"param1": "value1"}
        )
        
        key2 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {"param1": "value2"}
        )
        
        assert key1 != key2  # Different params = different keys
        assert key1 == "TestClass/test_method/6ce38f6a45"
        assert key2 == "TestClass/test_method/eac1ca90bb"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cache Hash Building Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_build_cache_hash(self):
        
        cache_key = Safe_Str__File__Path("TestClass/test_method/abc123")
        cache_hash = self.key_builder.build_cache_hash(cache_key)
        
        assert cache_hash is not None
        assert len(str(cache_hash)) == 16
        assert type(cache_hash)     is Safe_Str__Cache_Hash
        assert cache_hash           == "236b009cbeda86d9"


    def test_build_cache_hash__deterministic(self):
        
        cache_key = Safe_Str__File__Path("TestClass/test_method/abc123")
        hash1     = self.key_builder.build_cache_hash(cache_key)
        hash2     = self.key_builder.build_cache_hash(cache_key)
        
        assert hash1 == hash2
        assert hash1 == "236b009cbeda86d9"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Nested Field Path Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test__extract_key_fields__nested_path(self):
        params = {
            "user": {
                "profile": {
                    "id": "user123"
                }
            },
            "other": "value"
        }
        key_fields = ["user.profile.id"]
        
        extracted = self.key_builder._extract_key_fields(params, key_fields)
        
        assert extracted == {"user.profile.id": "user123"}

    def test__get_nested_value__dict(self):
        obj = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            }
        }
        field_path = Safe_Str__Json__Field_Path("level1.level2.level3")
        
        result = self.key_builder.get_nested_value(obj, field_path)
        
        assert result == "value"

    def test__get_nested_value__type_safe(self):
        class Inner(Type_Safe):
            value: str = "inner_value"
        
        class Outer(Type_Safe):
            inner: Inner
        
        obj = Outer(inner=Inner())
        field_path = Safe_Str__Json__Field_Path("inner.value")
        
        result = self.key_builder.get_nested_value(obj, field_path)
        
        assert result == "inner_value"

    def test__get_nested_value__missing_path(self):
        obj = {"level1": {"level2": "value"}}
        field_path = Safe_Str__Json__Field_Path("level1.level3.missing")
        
        result = self.key_builder.get_nested_value(obj, field_path)
        
        assert result is None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Normalization Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test__normalize_for_hashing__primitives(self):
        assert self.key_builder._normalize_for_hashing("string") == "string"
        assert self.key_builder._normalize_for_hashing(123)      == 123
        assert self.key_builder._normalize_for_hashing(45.67)    == 45.67
        assert self.key_builder._normalize_for_hashing(True)     == True

    def test__normalize_for_hashing__type_safe(self):
        class TestSchema(Type_Safe):
            field1: str = "value1"
            field2: int = 42
        
        schema = TestSchema()
        normalized = self.key_builder._normalize_for_hashing(schema)
        
        assert normalized == {"field1": "value1", "field2": 42}

    def test__normalize_for_hashing__bytes(self):
        test_bytes = b"hello"
        normalized = self.key_builder._normalize_for_hashing(test_bytes)
        
        assert normalized == test_bytes.hex()

    def test__normalize_for_hashing__nested_structures(self):
        nested = {
            "outer": {
                "inner": ["value1", "value2"],
                "number": 123
            }
        }
        normalized = self.key_builder._normalize_for_hashing(nested)
        
        assert normalized == nested

    def test__normalize_for_hashing__custom_object(self):
        class CustomObject:
            def __init__(self):
                self.field1 = "value1"
                self.field2 = 42
        
        obj = CustomObject()
        normalized = self.key_builder._normalize_for_hashing(obj)
        
        assert normalized == {"field1": "value1", "field2": 42}

    # ═══════════════════════════════════════════════════════════════════════════════
    # Hash Generation Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test__generate_param_hash__deterministic(self):
        data = {"param1": "value1", "param2": "value2"}
        
        hash1 = self.key_builder._generate_param_hash(data)
        hash2 = self.key_builder._generate_param_hash(data)
        
        assert hash1      == hash2
        assert len(hash1) == 10
        assert hash1      == "b9fd29c8b0"

    def test__generate_param_hash__order_independent(self):
        data1 = {"param1": "value1", "param2": "value2"}
        data2 = {"param2": "value2", "param1": "value1"}
        
        hash1 = self.key_builder._generate_param_hash(data1)
        hash2 = self.key_builder._generate_param_hash(data2)
        
        assert hash1 == hash2  # Order doesn't matter
        assert hash1 == "b9fd29c8b0"

    def test__generate_param_hash__type_safe_objects(self):
        class RequestSchema(Type_Safe):
            field1: str = "test"
            field2: int = 123
        
        data = {"request": RequestSchema()}
        
        hash1 = self.key_builder._generate_param_hash(data)
        hash2 = self.key_builder._generate_param_hash(data)
        
        assert hash1 == hash2
        assert hash1 == "00ce41cfbb"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Namespace Key Building Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_build_namespace_key(self):
        from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
        
        namespace = "my-namespace"
        cache_key = Safe_Str__File__Path("TestClass/method/hash123")
        
        result = self.key_builder.build_namespace_key(namespace, cache_key)
        assert type(result) is Safe_Str__File__Path
        assert result       == "my-namespace/TestClass/method/hash123"

    # ═══════════════════════════════════════════════════════════════════════════════
    # Complex Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_build_cache_key__complex_type_safe_params(self):
        class RequestSchema(Type_Safe):
            field1: str = "test"
            field2: int = 123
            nested: dict
        
        config = Schema__Cache__Decorator__Config(
            namespace  = "test",
            key_fields = ["request"]
        )
        
        request = RequestSchema(nested= {"key": "value"})
        
        key1 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("Service"),
            method_name = Safe_Str__Python__Identifier("transform"),
            params      = {"request": request}
        )
        
        key2 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("Service"),
            method_name = Safe_Str__Python__Identifier("transform"),
            params      = {"request": request}
        )
        
        assert key1 == key2  # Same Type_Safe object = same key
        assert key1 == "Service/transform/75ba1a3d7a"

    def test_build_cache_key__with_ignored_params(self):
        config = Schema__Cache__Decorator__Config(
            namespace  = "test",
            key_fields = ["important"]  # Only this field matters
        )
        
        key1 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {
                "important": "value1",
                "ignored1": "different1",
                "ignored2": "different2"
            }
        )
        
        key2 = self.key_builder.build_cache_key(
            config      = config,
            class_name  = Safe_Str__Python__Identifier("TestClass"),
            method_name = Safe_Str__Python__Identifier("test_method"),
            params      = {
                "important": "value1",
                "ignored1": "changed1",
                "ignored2": "changed2"
            }
        )
        
        assert key1 == key2  # Ignored params don't affect key

    def test_build_cache_key__empty_key_fields(self):
        config = Schema__Cache__Decorator__Config(namespace  = "test",
                                                  key_fields = []    ) # when no fields to hash, use all fields
        
        cache_key = self.key_builder.build_cache_key(config      = config,
                                                     class_name  = Safe_Str__Python__Identifier("TestClass"),
                                                     method_name = Safe_Str__Python__Identifier("test_method"),
                                                     params      = {"param1": "value1", "param2": "value2"})
        
        assert str(cache_key) == "TestClass/test_method/b9fd29c8b0"  # all params used to calculate
