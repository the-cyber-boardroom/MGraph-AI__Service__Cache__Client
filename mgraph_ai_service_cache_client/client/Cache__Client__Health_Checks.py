from osbot_utils.decorators.methods.cache_on_self                                                     import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                  import Type_Safe
from osbot_utils.utils.Misc                                                                           import list_set
from mgraph_ai_service_cache_client.client.Cache__Client__Config                                      import Cache__Client__Config
from mgraph_ai_service_cache_client.client.Cache__Client__Requests                                    import Cache__Client__Requests
from mgraph_ai_service_cache_client.schemas.client.health_checks.Cache__Client__Health_Checks__Status import Cache__Client__Health_Checks__Status


class Cache__Client__Health_Checks(Type_Safe):
    config : Cache__Client__Config

    @cache_on_self
    def client__requests(self):
        return Cache__Client__Requests(config=self.config)

    def check__target_server__status(self):
        path          = "/openapi.json"                                  # in Fast_API this endpoint has no auth
        result        = self.client__requests().get(path)
        openapi_json  = result.json
        success       = list_set(openapi_json) == ['components', 'info', 'openapi', 'paths']

        status_kwargs = dict(duration      = result.duration          ,
                             success       = success                   ,
                             target_server = self.config.target_server)
        return Cache__Client__Health_Checks__Status(**status_kwargs)
