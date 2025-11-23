from typing                          import Any, Dict
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

from mgraph_ai_service_cache_client.client.requests.schemas.Schema__Cache__Service__Fast_API__Client__Requests__Result import Schema__Cache__Service__Fast_API__Client__Requests__Result


class Service__Fast_API__Client__Data__Retrieve(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    def data__json__with__id(self, cache_id: str, namespace: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint get__data__json__with__id
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/json/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__json__with__id_and_key(self, cache_id: str, namespace: str, data_key: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint get__data__json__with__id_and_key
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/json/{data_key}/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    @type_safe
    def data__string__with__id(self,
                               cache_id: str,
                               namespace: str,
                               data_file_id: str
                          ) -> Schema__Cache__Service__Fast_API__Client__Requests__Result:                              # Auto-generated from endpoint get__data__string__with__id
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/string/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
        if result.status_code == 200:
            return Schema__Cache__Service__Fast_API__Client__Requests__Result.from_json(result.json) # Return response data
        return None
        #return result.json if result.json else result.text

    def data__string__with__id_and_key(self,
                                       cache_id: str,
                                       namespace: str,
                                       data_key: str,
                                       data_file_id: str) -> Dict:                              # Auto-generated from endpoint get__data__string__with__id_and_key
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/string/{data_key}/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__binary__with__id(self, cache_id: str, namespace: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint get__data__binary__with__id
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/binary/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
        return result.content
        #return result.json if result.json else result.text                         # Return response data

    def data__binary__with__id_and_key(self, cache_id: str, namespace: str, data_key: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint get__data__binary__with__id_and_key
                                                                                    # Build path
        path = f"/{namespace}/cache/{cache_id}/data/binary/{data_key}/{data_file_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "GET",
            path   = path,
            body   = body
        )
        return result.content
        return result.json if result.json else result.text                          # Return response data