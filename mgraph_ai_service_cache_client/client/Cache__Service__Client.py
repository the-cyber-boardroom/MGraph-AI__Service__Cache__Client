from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config import Cache__Service__Fast_API__Client__Config

# todo: question: should this be called Client__Cache_Service (would make sense when we have multiple of these happening at the same time:
#                                                              like Client__Http_Service, Client__LLMs_Service, Client__News_Service, etc..
class Cache__Service__Client(Type_Safe):
    config   : Cache__Service__Fast_API__Client__Config

    @cache_on_self
    def client(self):
        return Cache__Service__Fast_API__Client(config=self.config)