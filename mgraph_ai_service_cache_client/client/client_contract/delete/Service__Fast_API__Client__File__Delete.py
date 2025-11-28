from typing                          import Any, Dict
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Service__Fast_API__Client__File__Delete(Type_Safe):
    _client: Any                                                                    # Reference to main client

    @property
    def requests(self):                                                             # Access the unified request handler
        return self._client.requests()

    # todo: this should a variation of the Schema__Cache__Delete__Success (which needed refactoring)
    def delete__cache_id(self, cache_id: str, namespace: str) -> Dict:                              # Auto-generated from endpoint delete__delete__cache_id
                                                                                    # Build path
        path = f"/{namespace}/delete/{cache_id}"
        body = None
                                                                                    # Execute request
        result = self.requests.execute(
            method = "DELETE",
            path   = path,
            body   = body
        )
        if result.status_code == 200:                                                                                          # Return response data
            return result.json
        return None