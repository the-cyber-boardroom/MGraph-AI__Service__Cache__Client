from fastapi                                                                                        import FastAPI
from osbot_fast_api.services.schemas.registry.enums.Enum__Fast_API__Service__Registry__Client__Mode import Enum__Fast_API__Service__Registry__Client__Mode
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version                     import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Name            import Safe_Str__Http__Header__Name
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Value           import Safe_Str__Http__Header__Value
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                            import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from mgraph_ai_service_cache_client.utils.Version                                                   import version__mgraph_ai_service_cache_client

CACHE__SERVICE__NAME             = "Cache__Service__Fast_API"
CACHE__SERVICE__REQUEST__TIMEOUT = 30

class Cache__Service__Fast_API__Client__Config(Type_Safe):
    base_url             : Safe_Str__Url                                    = None
    api_key              : Safe_Str__Http__Header__Value                    = None                                       # Optional API key
    api_key_header       : Safe_Str__Http__Header__Name                     = None                                       # Header name for API key
    mode                 : Enum__Fast_API__Service__Registry__Client__Mode  = Enum__Fast_API__Service__Registry__Client__Mode.IN_MEMORY
    fast_api_app         : FastAPI                                          = None                                       # FastAPI app for in-memory
    timeout              : Safe_UInt                                        = CACHE__SERVICE__REQUEST__TIMEOUT           # Request timeout in seconds
    service_name         : Safe_Str__Id                                     = CACHE__SERVICE__NAME
    service_version      : Safe_Str__Version                                = version__mgraph_ai_service_cache_client