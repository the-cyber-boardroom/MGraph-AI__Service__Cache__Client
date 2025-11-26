from typing                                                                                    import Dict, List
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                 import type_safe
from mgraph_ai_service_cache_client.client.requests.Cache__Service__Fast_API__Client__Requests import Cache__Service__Fast_API__Client__Requests


class Service__Fast_API__Client__Namespace(Type_Safe):
    requests : Cache__Service__Fast_API__Client__Requests                                                                   # Reference to main client

    # todo: BUG: rename file_hashes to cache_hashes     (after client refactor)
    # todo: return type should be Safe_Str__Cache_Hash (see if this not bug a bug @type_safe auto conversion of the list[str] we get from the f"/{namespace}/file-hashes" call)
    @type_safe
    def file_hashes(self, namespace: Safe_Str__Id) -> List[str]:                    # Auto-generated from endpoint get__file_hashes
                                                                                    # Build path
        path = f"/{namespace}/file-hashes"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = body )
        return result.json                                                                                    # Return response data

    # todo: BUG: rename file_ids to cache_ids     (after client refactor)
    @type_safe
    def file_ids(self, namespace: Safe_Str__Id) -> List:                              # Auto-generated from endpoint get__file_ids
                                                                                    # Build path
        path = f"/{namespace}/file-ids"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def stats(self, namespace: str) -> Dict:                              # Auto-generated from endpoint get__stats
                                                                                    # Build path
        path = f"/{namespace}/stats"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text