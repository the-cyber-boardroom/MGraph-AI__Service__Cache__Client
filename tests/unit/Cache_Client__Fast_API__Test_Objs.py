# from fastapi                                                            import FastAPI
# from osbot_fast_api.api.Fast_API                                        import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE
# from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
# from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id   import Cache_Id
# from osbot_utils.utils.Env                                              import set_env
# from starlette.testclient                                               import TestClient
# from mgraph_ai_service_cache_client.fast_api.Cache_Client__Fast_API     import Cache_Client__Fast_API
#
# TEST_API_KEY__NAME = 'key-used-in-pytest'
# TEST_API_KEY__VALUE = Cache_Id()
#
# class Cache_Client__Fast_API__Test_Objs(Type_Safe):
#     fast_api        : Cache_Client__Fast_API     = None
#     fast_api__app   : FastAPI               = None
#     fast_api__client: TestClient            = None
#     setup_completed : bool                  = False
#
# service_fast_api_test_objs = Cache_Client__Fast_API__Test_Objs()
#
# def setup__cache_client__fast_api_test_objs():
#         with service_fast_api_test_objs as _:
#             if service_fast_api_test_objs.setup_completed is False:
#                 _.fast_api         = Cache_Client__Fast_API().setup()
#                 _.fast_api__app    = _.fast_api.app()
#                 _.fast_api__client = _.fast_api.client()
#                 _.setup_completed  = True
#
#                 set_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME , TEST_API_KEY__NAME)
#                 set_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE, TEST_API_KEY__VALUE)
#         return service_fast_api_test_objs

from typing                                                                                 import Tuple
from fastapi                                                                                import FastAPI
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API__Config                        import Serverless__Fast_API__Config
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                               import Cache_Service__Fast_API
from mgraph_ai_service_cache.service.cache.Cache__Service                                   import Cache__Service
from mgraph_ai_service_cache_client.client.Client__Cache__Service                           import Client__Cache__Service
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client

# todo: refactor code below to a helper class that we can reuse across (since the idea is not to add a dependency on the cache_service here, see if we can add this helper class to the mgraph_ai_service_cache package)
#       since this will be useful for the projects that want to easily run the cache service in memory
@type_safe
def cache__service__fast_api_app() -> Tuple[FastAPI, Cache__Service]:
    serverless_config       = Serverless__Fast_API__Config              (enable_api_key = False                )
    cache_service__fast_api = Cache_Service__Fast_API                   (config         = serverless_config ).setup()
    fast_api_app            = cache_service__fast_api.app()
    return fast_api_app, cache_service__fast_api.cache_service

@type_safe
def client_cache_service() -> Tuple[Cache__Service__Fast_API__Client, Cache__Service]:
    fast_api_app, cache_service  = cache__service__fast_api_app()
    client__cache_service        = Client__Cache__Service().set__fast_api_app(fast_api_app).client()
    return client__cache_service, cache_service