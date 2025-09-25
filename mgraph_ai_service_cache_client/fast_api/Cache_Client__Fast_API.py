from osbot_fast_api_serverless.fast_api.Serverless__Fast_API         import Serverless__Fast_API
from mgraph_ai_service_cache_client.fast_api.routes.Routes__Info     import Routes__Info
from mgraph_ai_service_cache_client.utils.Version                    import version__mgraph_ai_service_cache_client



class Cache_Client__Fast_API(Serverless__Fast_API):
    title   = "ASd"  #     FAST_API__TITLE
    version = version__mgraph_ai_service_cache_client

    def setup_routes(self):
        self.add_routes(Routes__Info  )



