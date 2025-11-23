from unittest                                                                import TestCase
from typing                                                                  import Optional
from osbot_utils.testing.__                                                  import __
from osbot_utils.utils.Objects                                               import base_classes
from osbot_utils.type_safe.Type_Safe                                         import Type_Safe
from mgraph_ai_service_cache_client.client.decorator.cache_operations.Cache__Serializer import Cache__Serializer


class test_Cache__Serializer(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.serializer = Cache__Serializer()
    
    def test__init__(self):
        with self.serializer as _:
            assert type(_)         is Cache__Serializer
            assert base_classes(_) == [Type_Safe, object]
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_serialize__none(self):
        result = self.serializer.serialize(None)
        assert result is None
    
    def test_serialize__primitives(self):
        assert self.serializer.serialize("hello")     == "hello"
        assert self.serializer.serialize(42)          == 42
        assert self.serializer.serialize(3.14)        == 3.14
        assert self.serializer.serialize(True)        == True
        assert self.serializer.serialize(False)       == False
    
    def test_serialize__dict(self):
        test_dict = {"key1": "value1", "key2": 42}
        result = self.serializer.serialize(test_dict)
        assert result == test_dict
    
    def test_serialize__list(self):
        test_list = ["item1", 42, True]
        result = self.serializer.serialize(test_list)
        assert result == test_list
    
    def test_serialize__bytes(self):
        test_bytes = b"hello world"
        result = self.serializer.serialize(test_bytes)
        assert result == test_bytes
    
    def test_serialize__type_safe_object(self):
        class TestSchema(Type_Safe):
            field1: str = "value1"
            field2: int = 42
        
        obj = TestSchema()
        result = self.serializer.serialize(obj)
        
        assert result == {"field1": "value1", "field2": 42}
    
    def test_serialize__nested_type_safe(self):
        class InnerSchema(Type_Safe):
            inner_field: str = "inner"
        
        class OuterSchema(Type_Safe):
            outer_field: str = "outer"
            inner: InnerSchema
        
        obj = OuterSchema(
            outer_field = "test",
            inner       = InnerSchema(inner_field="nested")
        )
        
        result = self.serializer.serialize(obj)
        
        assert result == {
            "outer_field": "test",
            "inner": {
                "inner_field": "nested"
            }
        }
    
    def test_serialize__custom_object_with_dict(self):
        class CustomObject:
            def __init__(self):
                self.field1 = "value1"
                self.field2 = 42
        
        obj = CustomObject()
        result = self.serializer.serialize(obj)
        
        assert result == {"field1": "value1", "field2": 42}
    
    def test_serialize__callable_returns_string(self):
        def test_function():
            pass
        
        result = self.serializer.serialize(test_function)
        assert isinstance(result, str)
        assert "test_function" in result
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Deserialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_deserialize__none(self):
        result = self.serializer.deserialize(None, None)
        assert result is None
    
    def test_deserialize__no_type_hint(self):
        data = {"key": "value"}
        result = self.serializer.deserialize(data, None)
        assert result == data
    
    def test_deserialize__primitives(self):
        assert self.serializer.deserialize("42", int)   == 42
        assert self.serializer.deserialize(42, str)     == "42"
        assert self.serializer.deserialize("3.14", float) == 3.14
        assert self.serializer.deserialize(1, bool)     == True
        assert self.serializer.deserialize(0, bool)     == False
    
    def test_deserialize__already_correct_type(self):
        data = {"key": "value"}
        result = self.serializer.deserialize(data, dict)
        assert result == data
    
    def test_deserialize__type_safe_from_dict(self):
        class TestSchema(Type_Safe):
            field1: str
            field2: int
        
        data = {"field1": "value1", "field2": 42}
        result = self.serializer.deserialize(data, TestSchema)
        
        assert isinstance(result, TestSchema)
        assert result.field1 == "value1"
        assert result.field2 == 42
    
    def test_deserialize__optional_type(self):
        result1 = self.serializer.deserialize("value", Optional[str])
        assert result1 == "value"
        
        result2 = self.serializer.deserialize(None, Optional[str])
        assert result2 is None
    
    def test_deserialize__json_string_to_dict(self):
        json_str = '{"key": "value", "number": 42}'
        result = self.serializer.deserialize(json_str, dict)
        
        assert result == {"key": "value", "number": 42}
    
    def test_deserialize__json_string_to_list(self):
        json_str = '["item1", "item2", 42]'
        result = self.serializer.deserialize(json_str, list)
        
        assert result == ["item1", "item2", 42]
    
    def test_deserialize__type_safe_from_json_string(self):
        class TestSchema(Type_Safe):
            field1: str
            field2: int
        
        json_str = '{"field1": "value1", "field2": 42}'
        result = self.serializer.deserialize(json_str, TestSchema)
        
        assert isinstance(result, TestSchema)
        assert result.field1 == "value1"
        assert result.field2 == 42
    
    def test_deserialize__error_handling(self):
        # This should raise Cache__Serialization__Error
        from mgraph_ai_service_cache_client.client.decorator.exceptions.Cache__Decorator__Exceptions import Cache__Serialization__Error
        
        with self.assertRaises(Cache__Serialization__Error) as context:
            self.serializer.deserialize("not_a_number", int)
        
        assert "Failed to deserialize" in str(context.exception)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Hint Extraction Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_extract_type_hint__no_annotation(self):
        def func_no_hint():
            pass
        
        result = self.serializer.extract_type_hint(func_no_hint)
        assert result is None
    
    def test_extract_type_hint__with_return_type(self):
        def func_with_hint() -> str:
            return "test"
        
        result = self.serializer.extract_type_hint(func_with_hint)
        assert result is str
    
    def test_extract_type_hint__type_safe_return(self):
        class ResponseSchema(Type_Safe):
            message: str
        
        def func_returns_schema() -> ResponseSchema:
            return ResponseSchema(message="test")
        
        result = self.serializer.extract_type_hint(func_returns_schema)
        assert result is ResponseSchema
    
    def test_extract_type_hint__optional_return(self):
        def func_optional() -> Optional[str]:
            return None
        
        result = self.serializer.extract_type_hint(func_optional)
        assert result == Optional[str]
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Method Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_is_type_safe_object(self):
        class TestSchema(Type_Safe):
            field: str = "test"
        
        obj = TestSchema()
        regular_dict = {"field": "test"}
        
        assert self.serializer.is_type_safe_object(obj) is True
        assert self.serializer.is_type_safe_object(regular_dict) is False
        assert self.serializer.is_type_safe_object("string") is False
    
    def test_get_object_size__bytes(self):
        test_bytes = b"hello world"
        size = self.serializer.get_object_size(test_bytes)
        assert size == len(test_bytes)
    
    def test_get_object_size__string(self):
        test_str = "hello world"
        size = self.serializer.get_object_size(test_str)
        assert size == len(test_str.encode('utf-8'))
    
    def test_get_object_size__dict(self):
        test_dict = {"key": "value"}
        size = self.serializer.get_object_size(test_dict)
        assert size > 0
    
    def test_get_object_size__type_safe(self):
        class TestSchema(Type_Safe):
            field: str = "test"
        
        obj = TestSchema()
        size = self.serializer.get_object_size(obj)
        assert size > 0
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Round-trip Tests
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def test_round_trip__type_safe_object(self):
        class ComplexSchema(Type_Safe):
            str_field: str
            int_field: int
            list_field: list
            dict_field: dict
        
        original = ComplexSchema(
            str_field  = "test",
            int_field  = 42,
            list_field = [1, 2, 3],
            dict_field = {"nested": "value"}
        )
        
        # Serialize then deserialize
        serialized = self.serializer.serialize(original)
        deserialized = self.serializer.deserialize(serialized, ComplexSchema)
        
        assert isinstance(deserialized, ComplexSchema)
        assert deserialized.str_field == original.str_field
        assert deserialized.int_field == original.int_field
        assert deserialized.list_field == original.list_field
        assert deserialized.dict_field == original.dict_field
