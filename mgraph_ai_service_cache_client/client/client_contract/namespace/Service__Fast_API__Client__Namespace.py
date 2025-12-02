from typing                                                                                    import Dict, List
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                             import Cache_Id
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash       import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                          import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                 import type_safe
from mgraph_ai_service_cache_client.client.requests.Cache__Service__Fast_API__Client__Requests import Cache__Service__Fast_API__Client__Requests


class Service__Fast_API__Client__Namespace(Type_Safe):
    requests : Cache__Service__Fast_API__Client__Requests                                                                   # Reference to main client

    # todo: return type should be Safe_Str__Cache_Hash (see if this not bug a bug @type_safe auto conversion of the list[str] we get from the f"/{namespace}/file-hashes" call)
    # todo: update the main call below when fixed on Cache_Client
    @type_safe
    def cache_hashes(self,
                     namespace: Safe_Str__Id
                ) -> List[Safe_Str__Cache_Hash]:
                                                                                    # Build path
        path = f"/{namespace}/file-hashes"                                          # todo: BUG: rename file_hashes to cache_hashes     (after client refactor)
        body = None
                                                                                    # Execute request
        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = body )

        if result.status_code == 200:
            cache_hashes = Type_Safe__List(expected_type=Safe_Str__Cache_Hash)
            cache_hashes.extend(result.json)
            return cache_hashes
        return []

    @type_safe
    def cache_ids(self,
                  namespace: Safe_Str__Id
             ) -> List[Cache_Id]:
                                                                                    # Build path
        path = f"/{namespace}/file-ids"                                             # todo: BUG: rename file_ids to cache_ids     (after client refactor)
        body = None
                                                                                    # Execute request
        result = self.requests.execute(method = "GET",
                                       path   = path,
                                       body   = body)

        return result.json                                                                            # Return response data

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
        return result.json                                                                            # Return response data
        #return result.json if result.json else result.text