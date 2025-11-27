from fastapi                                                                                        import FastAPI
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                import Enum__Client__Mode
from osbot_utils.utils.Env                                                                          import get_env
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                             import ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME, ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE, ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE
from osbot_utils.decorators.methods.cache_on_self                                                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                      import type_safe
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client         import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config

# todo: question: should this be called Client__Cache_Service (would make sense when we have multiple of these happening at the same time:
#                                                              like Client__Http_Service, Client__LLMs_Service, Client__News_Service, etc..
class Client__Cache__Service(Type_Safe):
    config   : Cache__Service__Fast_API__Client__Config

    @cache_on_self
    def client(self):
        #self.setup()                                                    # todo: see if this is a better place to put it
        return Cache__Service__Fast_API__Client(config=self.config)

    @type_safe
    def set__fast_api_app(self,
                          app: FastAPI
                    ) -> 'Client__Cache__Service':
        self.config.fast_api_app = app
        return self

    def setup(self):
        key_name   = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME  )
        key_value  = get_env(ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE )
        target_url = get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE             )
        if key_name and key_value and target_url:
            with self.config as _:
                _.api_key_header = key_name
                _.api_key        = key_value
                _.base_url       = target_url
                _.mode           = Enum__Client__Mode.REMOTE
        return self