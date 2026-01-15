# ═══════════════════════════════════════════════════════════════════════════════
# Cache Service Client - Data Operations Hub
# Central access point for data file operations under cache entries
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                         import Any
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                                   import cache_on_self
from .Service__Fast_API__Client__Data__Retrieve                                     import Service__Fast_API__Client__Data__Retrieve
from .Service__Fast_API__Client__Data__Delete                                       import Service__Fast_API__Client__Data__Delete
from .Service__Fast_API__Client__Data__Exists                                       import Service__Fast_API__Client__Data__Exists
from .Service__Fast_API__Client__Data__List                                         import Service__Fast_API__Client__Data__List
from .Service__Fast_API__Client__Data__Update                                       import Service__Fast_API__Client__Data__Update


class Service__Fast_API__Client__Data(Type_Safe):                                   # Hub for data file operations
    _client: Any                                                                    # Reference to main client

    @cache_on_self
    def retrieve(self) -> Service__Fast_API__Client__Data__Retrieve:                # Access retrieve operations
        return Service__Fast_API__Client__Data__Retrieve(_client=self._client)

    @cache_on_self
    def delete(self) -> Service__Fast_API__Client__Data__Delete:                    # Access delete operations
        return Service__Fast_API__Client__Data__Delete(_client=self._client)

    @cache_on_self
    def exists(self) -> Service__Fast_API__Client__Data__Exists:                    # Access exists operations
        return Service__Fast_API__Client__Data__Exists(_client=self._client)

    @cache_on_self
    def list(self) -> Service__Fast_API__Client__Data__List:                        # Access list operations
        return Service__Fast_API__Client__Data__List(_client=self._client)

    @cache_on_self
    def update(self) -> Service__Fast_API__Client__Data__Update:                    # Access update operations
        return Service__Fast_API__Client__Data__Update(_client=self._client)