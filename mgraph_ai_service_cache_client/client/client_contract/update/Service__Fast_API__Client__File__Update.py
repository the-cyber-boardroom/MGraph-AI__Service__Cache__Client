from typing                                                                          import Any
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Update__Response    import Schema__Cache__Update__Response


class Service__Fast_API__Client__File__Update(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    def update__string(self,
                       cache_id : Random_Guid   ,
                       namespace: Safe_Str__Id  ,
                       body     : str
                  ) -> Schema__Cache__Update__Response:                            # Update string data in existing cache entry
                                                                                    # Build path
        path = f"/{namespace}/update/{cache_id}/string"
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return Schema__Cache__Update__Response.from_json(result.json)

    def update__json(self,
                     cache_id : Random_Guid   ,
                     namespace: Safe_Str__Id  ,
                     body     : dict
                ) -> Schema__Cache__Update__Response:                              # Update JSON data in existing cache entry
                                                                                    # Build path
        path = f"/{namespace}/update/{cache_id}/json"
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return Schema__Cache__Update__Response.from_json(result.text)

    def update__binary(self,
                       cache_id : Random_Guid   ,
                       namespace: Safe_Str__Id  ,
                       body     : bytes
                  ) -> Schema__Cache__Update__Response:                            # Update binary data in existing cache entry
                                                                                    # Build path
        path = f"/{namespace}/update/{cache_id}/binary"
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return Schema__Cache__Update__Response.from_json(result.json)