from typing import Any, Optional, Dict
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Service__Fast_API__Client__Data__Store(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    def data__store_binary(self, cache_id: str, namespace: str) -> Dict:                              # Auto-generated from endpoint post__data__store_binary
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/binary"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_binary__with__id(self, cache_id: str, namespace: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_binary__with__id
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/binary/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_binary__with__id_and_key(self, cache_id: str, namespace: str, data_key: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_binary__with__id_and_key
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/binary/{data_key:path}/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_json(self, cache_id: str, namespace: str) -> Dict:                              # Auto-generated from endpoint post__data__store_json
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/json"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_json__with__id(self, cache_id: str, namespace: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_json__with__id
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/json/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_json__with__id_and_key(self, cache_id: str, namespace: str, data_key: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_json__with__id_and_key
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/json/{data_key:path}/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_string(self, cache_id: str, namespace: str) -> Dict:                              # Auto-generated from endpoint post__data__store_string
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/string"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_string__with__id(self, cache_id: str, namespace: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_string__with__id
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/string/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text

    def data__store_string__with__id_and_key(self, cache_id: str, namespace: str, data_key: str, data_file_id: str) -> Dict:                              # Auto-generated from endpoint post__data__store_string__with__id_and_key
                                                                                    # Build path
        path = f"/{{namespace}}/cache/{{cache_id}}/data/store/string/{data_key:path}/{{data_file_id}}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "POST",
            path   = path,
            body   = body
        )
                                                                                    # Return response data
        return result.json if result.json else result.text