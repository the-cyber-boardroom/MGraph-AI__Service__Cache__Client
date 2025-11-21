from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.decorator.schemas.enums.Enum__Cache__Decorator__Mode    import Enum__Cache__Decorator__Mode


class test_Enum__Cache__Decorator__Mode(TestCase):

    def test__init__(self):                                                 # Test enum values and structure
        # Verify all expected modes exist
        assert Enum__Cache__Decorator__Mode.ENABLED   == 'enabled'
        assert Enum__Cache__Decorator__Mode.DISABLED  == 'disabled'
        assert Enum__Cache__Decorator__Mode.READ_ONLY == 'read-only'

    def test__enum_behavior(self):                                          # Test enum comparison and identity
        mode1 = Enum__Cache__Decorator__Mode.ENABLED
        mode2 = Enum__Cache__Decorator__Mode.ENABLED
        mode3 = Enum__Cache__Decorator__Mode.DISABLED

        assert mode1 == mode2                                               # Same enum values are equal
        assert mode1 is mode2                                               # Enums are singletons
        assert mode1 != mode3                                               # Different modes not equal
        
        assert mode1.value == 'enabled'                                     # Can access string value
        assert str(mode1)  == 'Enum__Cache__Decorator__Mode.ENABLED'        # String representation

    def test__string_conversion(self):                                      # Test string value compatibility
        # Enums should be usable in string contexts
        assert Enum__Cache__Decorator__Mode.ENABLED   == 'enabled'
        assert Enum__Cache__Decorator__Mode.DISABLED  == 'disabled'
        assert Enum__Cache__Decorator__Mode.READ_ONLY == 'read-only'
        
        # Can be used in dictionaries
        mode_dict = {Enum__Cache__Decorator__Mode.ENABLED: 'active'}
        assert mode_dict[Enum__Cache__Decorator__Mode.ENABLED] == 'active'

    def test__all_modes(self):                                              # Test all defined modes
        all_modes = list(Enum__Cache__Decorator__Mode)
        
        assert len(all_modes) == 3                                          # Exactly 3 modes
        assert Enum__Cache__Decorator__Mode.ENABLED   in all_modes
        assert Enum__Cache__Decorator__Mode.DISABLED  in all_modes
        assert Enum__Cache__Decorator__Mode.READ_ONLY in all_modes
