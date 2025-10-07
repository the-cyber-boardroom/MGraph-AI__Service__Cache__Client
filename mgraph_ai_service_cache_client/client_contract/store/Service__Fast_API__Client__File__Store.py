from typing                                                                          import Any, Optional, Dict
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id

from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy


class Service__Fast_API__Client__File__Store(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    #def store__string(self, strategy: Enum__Cache__Store__Strategy, namespace: str) -> Dict:                             # todo: BUG, missing body in method param
    def store__string(self, strategy  : Enum__Cache__Store__Strategy,
                            #namespace : str,                                           # todo: BUG namespace is Safe_Str__Id
                            namespace: Safe_Str__Id                 ,
                            body : str
                      ) -> Dict:                                                    # Auto-generated from endpoint post__store__string
                                                                                    # Build path
        #path = f"/{{namespace}}/{{strategy}}/store/string"                         # todo: BUG used {{namespace}} instead of {namespace}
        path = f"/{namespace}/{strategy}/store/string"

        #body = None                                                                # todo: BUG name was None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def store__string__cache_key(self, namespace: str, strategy: Enum__Cache__Store__Strategy, cache_key: str, file_id: Optional[str] = None) -> Dict:                              # Auto-generated from endpoint post__store__string__cache_key
                                                                                    # Build path
        path = f"/{{namespace}}/{{strategy}}/store/string/{cache_key:path}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def store__json(self, strategy: Enum__Cache__Store__Strategy, namespace: str) -> Dict:                              # Auto-generated from endpoint post__store__json
                                                                                    # Build path
        path = f"/{{namespace}}/{{strategy}}/store/json"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def store__json__cache_key(self, namespace: str, strategy: Enum__Cache__Store__Strategy, cache_key: str, file_id: Optional[str] = None) -> Dict:                              # Auto-generated from endpoint post__store__json__cache_key
                                                                                    # Build path
        path = f"/{{namespace}}/{{strategy}}/store/json/{cache_key:path}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def store__binary(self, strategy: Enum__Cache__Store__Strategy, namespace: str) -> Dict:                              # Auto-generated from endpoint post__store__binary
                                                                                    # Build path
        path = f"/{{namespace}}/{{strategy}}/store/binary"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def store__binary__cache_key(self, namespace: str, strategy: Enum__Cache__Store__Strategy, cache_key: str, file_id: Optional[str] = None) -> Dict:                              # Auto-generated from endpoint post__store__binary__cache_key
                                                                                    # Build path
        path = f"/{{namespace}}/{{strategy}}/store/binary/{cache_key:path}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text