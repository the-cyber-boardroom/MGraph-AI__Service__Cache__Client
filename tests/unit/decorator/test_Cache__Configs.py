from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.decorator.Cache__Decorator__Configs                     import CACHE_CONFIG__TRANSFORMATION, CACHE_CONFIG__GENERAL, CACHE_CONFIG__CLASSIFICATION
from mgraph_ai_service_cache_client.decorator.schemas.Schema__Cache__Decorator__Config      import Schema__Cache__Decorator__Config
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy


class test_Schema__Cache__Decorator__Configs(TestCase):                                        # Test pre-defined cache configurations

    def test__all_configs_are_cache_config_instances(self):                 # Test all configs are Schema__Cache__Decorator__Config instances
        assert isinstance(CACHE_CONFIG__TRANSFORMATION , Schema__Cache__Decorator__Config)
        assert isinstance(CACHE_CONFIG__CLASSIFICATION , Schema__Cache__Decorator__Config)
        assert isinstance(CACHE_CONFIG__GENERAL        , Schema__Cache__Decorator__Config)

    def test__text_transformation_config(self):                             # Test text transformation configuration
        config = CACHE_CONFIG__TRANSFORMATION
        
        assert config.namespace         == "cache-decorator__transformations"
        assert config.enabled           == True
        assert config.strategy          == Enum__Cache__Store__Strategy.KEY_BASED
        assert config.key_fields        == ["hash_mapping", "transformation_mode"]
        assert config.use_class_name    == True
        assert config.use_method_name   == True
        assert config.file_id           == "response"

    def test__semantic_classification_config(self):                         # Test semantic classification configuration
        config = CACHE_CONFIG__CLASSIFICATION
        
        assert config.namespace         == "cache-decorator__classifications"
        assert config.enabled           == True
        assert config.strategy          == Enum__Cache__Store__Strategy.KEY_BASED
        assert config.key_fields        == ["text"]
        assert config.use_class_name    == True
        assert config.use_method_name   == True
        assert config.file_id           == "classification"

    def test__general_config(self):                                         # Test general purpose configuration
        config = CACHE_CONFIG__GENERAL
        
        assert config.namespace         == "cache-decorator__general"
        assert config.enabled           == True
        assert config.strategy          == Enum__Cache__Store__Strategy.KEY_BASED
        assert config.key_fields        == []                               # No specific key fields
        assert config.use_class_name    == True
        assert config.use_method_name   == True
        assert config.file_id           == "response"

    def test__all_configs_enabled_by_default(self):                         # Test all configs are enabled by default
        assert CACHE_CONFIG__TRANSFORMATION.enabled  == True
        assert CACHE_CONFIG__CLASSIFICATION.enabled == True
        assert CACHE_CONFIG__GENERAL.enabled              == True

    def test__all_configs_use_key_based_strategy(self):                     # Test all configs use KEY_BASED strategy
        assert CACHE_CONFIG__TRANSFORMATION.strategy  == Enum__Cache__Store__Strategy.KEY_BASED
        assert CACHE_CONFIG__CLASSIFICATION.strategy == Enum__Cache__Store__Strategy.KEY_BASED
        assert CACHE_CONFIG__GENERAL.strategy              == Enum__Cache__Store__Strategy.KEY_BASED

    def test__configs_have_hierarchical_namespaces(self):                   # Test namespaces follow hierarchical structure
        # All should start with "cache-decorator__"
        assert CACHE_CONFIG__TRANSFORMATION.namespace.startswith("cache-decorator__")
        assert CACHE_CONFIG__CLASSIFICATION.namespace.startswith("cache-decorator__")
        assert CACHE_CONFIG__GENERAL.namespace.startswith("cache-decorator__")
        
        # Each should have unique sub-namespace
        assert CACHE_CONFIG__TRANSFORMATION.namespace.endswith("transformations")
        assert CACHE_CONFIG__CLASSIFICATION.namespace.endswith("classifications")
        assert CACHE_CONFIG__GENERAL.namespace.endswith("general")

    def test__transformation_config_key_fields(self):                       # Test transformation config caches correct fields
        config = CACHE_CONFIG__TRANSFORMATION
        
        # Should cache based on both hash_mapping AND transformation_mode
        assert "hash_mapping" in config.key_fields
        assert "transformation_mode" in config.key_fields
        assert len(config.key_fields) == 2

    def test__classification_config_key_fields(self):                       # Test classification config caches correct field
        config = CACHE_CONFIG__CLASSIFICATION
        
        # Should cache based on text only
        assert "text" in config.key_fields
        assert len(config.key_fields) == 1

    def test__general_config_no_key_fields(self):                           # Test general config has no specific key fields
        config = CACHE_CONFIG__GENERAL
        
        # Empty key_fields means cache key based on all params
        assert config.key_fields == []

    def test__all_configs_different_file_ids(self):                         # Test configs use appropriate file_ids
        # Transformation and general use "response"
        assert CACHE_CONFIG__TRANSFORMATION.file_id == "response"
        assert CACHE_CONFIG__GENERAL.file_id             == "response"
        
        # Classification uses specific file_id
        assert CACHE_CONFIG__CLASSIFICATION.file_id == "classification"

    def test__configs_immutability(self):                                   # Test configs can be modified if needed
        # Note: In Python, these are not immutable by default, but we can test they're independent
        config1 = CACHE_CONFIG__TRANSFORMATION
        config2 = CACHE_CONFIG__CLASSIFICATION
        
        # Modifying one shouldn't affect the other
        original_namespace = config1.namespace
        config1.enabled    = False
        
        assert config2.enabled == True                                      # Other config unaffected
        config1.enabled = True                                              # Restore original
        assert config1.namespace == original_namespace

        assert config1       != config2
        assert config1.obj() != config2.obj()
