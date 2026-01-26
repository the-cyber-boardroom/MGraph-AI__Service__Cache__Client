from fastapi                                                                                         import FastAPI
from osbot_utils.utils.Env                                                                           import get_env
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client          import Cache__Service__Fast_API__Client
from osbot_fast_api.services.registry.Fast_API__Service__Registry                                    import Fast_API__Service__Registry
from osbot_fast_api.services.registry.Fast_API__Service__Registry__Client__Base                      import Fast_API__Service__Registry__Client__Base
from osbot_fast_api.services.schemas.registry.enums.Enum__Fast_API__Service__Registry__Client__Mode  import Enum__Fast_API__Service__Registry__Client__Mode
from osbot_fast_api.services.schemas.registry.collections.List__Fast_API__Registry__Env_Vars         import List__Fast_API__Registry__Env_Vars
from osbot_fast_api.services.schemas.registry.Schema__Fast_API__Registry__Env_Var                    import Schema__Fast_API__Registry__Env_Var
from mgraph_ai_service_cache.service.cache.in_memory.Cache__Service__In_Memory                       import Cache__Service__In_Memory
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                              import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                              import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                              import ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                       import type_safe



# ═══════════════════════════════════════════════════════════════════════════════
# Cache__Service__Registry__Client
# Registry-compatible wrapper for Cache__Service__Fast_API__Client
# Bridges existing client to Fast_API__Service__Registry pattern
# ═══════════════════════════════════════════════════════════════════════════════

class Cache__Service__Registry__Client(Fast_API__Service__Registry__Client__Base):
    cache_client = Cache__Service__Fast_API__Client = None

    #_test_client  : TestClient                       = None                            # TestClient for IN_MEMORY mode

    def setup_from_env(self) -> 'Cache__Service__Registry__Client':                     # Configure from environment variables
        key_name   = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME )
        key_value  = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE)
        target_url = get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            )

        if target_url:
            self.config.mode          = Enum__Fast_API__Service__Registry__Client__Mode.REMOTE
            self.config.base_url      = target_url
            self.config.api_key_name  = key_name
            self.config.api_key_value = key_value
        return self

    @type_safe
    def setup_in_memory(self                       ,                            # Configure for IN_MEMORY mode
                        fast_api_app : FastAPI     ,
                        cache_client : Cache__Service__Fast_API__Client
                   ) -> 'Cache__Service__Registry__Client':
        self.config.mode         = Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY
        self.config.fast_api_app = fast_api_app
        return self

    # def requests(self) -> Cache__Service__Fast_API__Client__Requests:           # Return the requests transport
    #     if self.cache_client():
    #         return self.cache_client.requests()
    #     return None

    def health(self) -> bool:                                                   # Health check via info endpoint
        try:
            result = self.cache_client.info().health()
            return result.get('status') == 'ok'
        except:                                                                 # todo: see if need this catch here (if this fails we have bigger issues)
            return False


    def setup(self) -> Cache__Service__Fast_API__Client:                 # Access the wrapped cache client

        self.cache_client = Cache__Service__Fast_API__Client()

        with self.cache_client.config as _:

            if self.config.mode == Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY:
                _.mode         = Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY
                _.fast_api_app = self.config.fast_api_app

            elif self.config.mode == Enum__Fast_API__Service__Registry__Client__Mode.REMOTE:
                _.mode           = Enum__Fast_API__Service__Registry__Client__Mode.REMOTE
                _.base_url       = self.config.base_url
                _.api_key_header = self.config.api_key_name
                _.api_key        = self.config.api_key_value

        return self

    # # these should not be needed since we should be using the Cache__Service__Fast_API__Client directly
    # # ───────────────────────────────────────────────────────────────────────────
    # # Delegated Cache Operations - Expose wrapped client's domain methods
    # # ───────────────────────────────────────────────────────────────────────────
    #
    # def store(self):                                                            # Access store operations
    #     return self.cache_client().store()
    #
    # def retrieve(self):                                                         # Access retrieve operations
    #     return self.cache_client().retrieve()
    #
    # def info(self):                                                             # Access info operations
    #     return self.cache_client().info()
    #
    # def exists(self):                                                           # Access exists operations
    #     return self.cache_client().exists()
    #
    # def delete(self):                                                           # Access delete operations
    #     return self.cache_client().delete()
    #
    # def namespace(self):                                                        # Access namespace operations
    #     return self.cache_client().namespace()
    #
    # def namespaces(self):                                                       # Access namespaces operations
    #     return self.cache_client().namespaces()

    @classmethod
    def env_vars(cls) -> List__Fast_API__Registry__Env_Vars:                    # Expected env vars for this client
        return List__Fast_API__Registry__Env_Vars([Schema__Fast_API__Registry__Env_Var(name=ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE            , required=True ),
                                                   Schema__Fast_API__Registry__Env_Var(name=ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME , required=False),
                                                   Schema__Fast_API__Registry__Env_Var(name=ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE, required=False)])

    @classmethod
    def client_name(cls) -> str:
        return 'Cache__Service__Registry__Client'


# ═══════════════════════════════════════════════════════════════════════════════
# Helper: Create registry with in-memory cache client
# ═══════════════════════════════════════════════════════════════════════════════

@type_safe
def service_registry__register__cache_service(registry:Fast_API__Service__Registry
                              ) -> Cache__Service__Registry__Client:
    cache_in_memory = Cache__Service__In_Memory().setup()                       # Create in-memory cache service

    with Cache__Service__Registry__Client() as _:                               # Create registry-compatible client
        _.setup_in_memory(fast_api_app = cache_in_memory.fast_api_app ,
                          cache_client = cache_in_memory.cache_client )
        _.setup()
        registry.register(_)                                                    # Register the client

        return _





