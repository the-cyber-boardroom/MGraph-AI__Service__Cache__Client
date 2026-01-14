from typing                                                                                     import Any
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__Exists__Response          import Schema__Cache__Exists__Response
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                              import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                 import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash        import Safe_Str__Cache_Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                  import type_safe



class Service__Fast_API__Client__File__Exists(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    @type_safe
    def exists__cache_id(self, cache_id  : Cache_Id    ,                            # Check if cache_id exists
                               namespace : Safe_Str__Id
                        ) -> Schema__Cache__Exists__Response:
        path   = f"/{namespace}/exists/id/{cache_id}"
        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = None )

        if result.status_code == 200:
            return Schema__Cache__Exists__Response.from_json(result.json)

        return None

    @type_safe
    def exists__hash__cache_hash(self, cache_hash : Safe_Str__Cache_Hash,           # Check if hash exists
                                       namespace  : Safe_Str__Id
                                ) -> Schema__Cache__Exists__Response:
        path   = f"/{namespace}/exists/hash/{cache_hash}"
        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = None )

        if result.status_code == 200:
            return Schema__Cache__Exists__Response.from_json(result.json)

        return None