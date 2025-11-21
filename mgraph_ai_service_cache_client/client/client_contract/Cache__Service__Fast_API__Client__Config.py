from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Name import Safe_Str__Http__Header__Name
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Value import Safe_Str__Http__Header__Value
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url        import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from typing                                                                     import Optional
from mgraph_ai_service_cache_client.utils.Version                               import version__mgraph_ai_service_cache_client


class Cache__Service__Fast_API__Client__Config(Type_Safe):
    base_url        : Safe_Str__Url                 = None
    api_key         : Safe_Str__Http__Header__Value = None                                          # Optional API key
    api_key_header  : Safe_Str__Http__Header__Name  = None                                          # Header name for API key
    timeout         : Safe_UInt                     = 30                                            # Request timeout in seconds
    #verify_ssl      : bool          = True                                                         # Verify SSL certificates
    service_name    : Safe_Str__Id       = "Cache__Service__Fast_API"
    service_version : Safe_Str__Version  = version__mgraph_ai_service_cache_client