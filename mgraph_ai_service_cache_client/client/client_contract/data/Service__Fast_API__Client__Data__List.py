# ═══════════════════════════════════════════════════════════════════════════════
# Cache Service Client - Data List Operations
# List data files under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                       import Any
from osbot_utils.type_safe.Type_Safe                                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                 import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                                import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                   import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                    import type_safe
from mgraph_ai_service_cache_client.schemas.cache.data.Schema__Cache__Data__List__Response        import Schema__Cache__Data__List__Response


class Service__Fast_API__Client__Data__List(Type_Safe):                                           # Client for listing data files
    _client: Any                                                                                  # Reference to main client

    @property
    def requests(self):                                                                           # Access the unified request handler
        return self._client.requests()

    @type_safe
    def data__list(self,
                   cache_id  : Cache_Id    ,
                   namespace : Safe_Str__Id,
                   recursive : bool = True
              ) -> Schema__Cache__Data__List__Response:                                           # List all data files under cache entry

        path = f"/{namespace}/cache/{cache_id}/data/list"

        if recursive is False:
            path = f"{path}?recursive=false"

        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = None )

        if result.status_code == 200:
            return Schema__Cache__Data__List__Response.from_json(result.json)
        return None

    @type_safe
    def data__list__with__key(self,
                              cache_id  : Cache_Id             ,
                              namespace : Safe_Str__Id         ,
                              data_key  : Safe_Str__File__Path ,
                              recursive : bool = True
                         ) -> Schema__Cache__Data__List__Response:                                # List data files under specific key path

        path = f"/{namespace}/cache/{cache_id}/data/list/{data_key}"

        if recursive is False:
            path = f"{path}?recursive=false"

        result = self.requests.execute(method = "GET",
                                       path   = path ,
                                       body   = None )

        if result.status_code == 200:
            return Schema__Cache__Data__List__Response.from_json(result.json)
        return None