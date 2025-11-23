from typing                                                                          import Any, Optional, Dict
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id

from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Store__Response import Schema__Cache__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy import Enum__Cache__Store__Strategy


class Service__Fast_API__Client__File__Store(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    def store__string(self, strategy  : Enum__Cache__Store__Strategy,
                            #namespace : str,                                           # todo: BUG namespace is Safe_Str__Id
                            namespace: Safe_Str__Id                 ,
                            body : str
                      ) -> Schema__Cache__Store__Response:                                                    # Auto-generated from endpoint post__store__string
                                                                                    # Build path
        path = f"/{namespace}/{strategy}/store/string"
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
        return Schema__Cache__Store__Response.from_json(result.json)                # Return response data
        return result.json if result.json else result.text

    def store__string__cache_key(self, namespace: str                           ,
                                       strategy : Enum__Cache__Store__Strategy  ,
                                       cache_key: str                           ,
                                       body     : str                           ,
                                       file_id  : str   = ''
                                  ) -> Schema__Cache__Store__Response:                              # Auto-generated from endpoint post__store__string__cache_key
                                                                                    # Build path
        path = f"/{namespace}/{strategy}/store/string/{cache_key}?file_id={file_id}"
        #body = None
                                                                                    # Execute request
        result = self.requests.execute(method = "POST",
                                       path   = path  ,
                                       body   = body  )
                                                                                    # Return response data
        return Schema__Cache__Store__Response.from_json(result.json)
        #return result.json if result.json else result.text

    def store__json(self, strategy : Enum__Cache__Store__Strategy,
                          namespace: Safe_Str__Id,
                          body     : Dict
                      )-> Schema__Cache__Store__Response:
        path = f"/{namespace}/{strategy}/store/json"                            # Build path
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
        return Schema__Cache__Store__Response.from_json(result.text)              # Return response data

    def store__json__cache_key(self, namespace: str,
                                     strategy : Enum__Cache__Store__Strategy,
                                     cache_key: str,
                                     body     : dict ,
                                     file_id  : str  = '',
                                     json_field_path = ''               # todo: added new json_field_path
                                 ) -> Schema__Cache__Store__Response:                          # Auto-generated from endpoint post__store__json__cache_key
                                                                                    # Build path
        path = f"/{namespace}/{strategy}/store/json/{cache_key}?file_id={file_id}&json_field_path={json_field_path}"
        #body = None
                                                                                    # Execute request
        result = self.requests.execute(method = "POST",
                                      path   = path,
                                      body   = body)
        return Schema__Cache__Store__Response.from_json(result.text)                # Return response data
        #return result.json if result.json else result.text

    def store__binary(self, strategy : Enum__Cache__Store__Strategy,
                            namespace: Safe_Str__Id                ,
                            body     : bytes
                       ) -> Schema__Cache__Store__Response:
        path  = f"/{namespace}/{strategy}/store/binary"                          # Build path
        result = self.requests.execute(method = "POST",                             # Execute request
                                       path   = path  ,
                                       body   = body  )
        return Schema__Cache__Store__Response.from_json(result.json)                # Return response data

    def store__binary__cache_key(self, namespace: str,
                                       strategy: Enum__Cache__Store__Strategy,
                                       cache_key: str,
                                       body = bytes ,
                                       file_id: str = '') -> Schema__Cache__Store__Response:                              # Auto-generated from endpoint post__store__binary__cache_key
                                                                                    # Build path
        path = f"/{namespace}/{strategy}/store/binary/{cache_key}?file_id={file_id}"
        #body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
        return Schema__Cache__Store__Response.from_json(result.json)                # Return response data
        #return result.json if result.json else result.text