from typing                                                                                 import List
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path           import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now            import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Schema__Cache__Update__Response(Type_Safe):                      # Response for cache update operations
    cache_id         : Cache_Id                                        # Cache entry ID (unchanged)
    cache_hash       : Safe_Str__Cache_Hash                             # Content hash (V1: unchanged)
    namespace        : Safe_Str__Id                                     # Namespace
    paths            : List[Safe_Str__File__Path]                       # All updated file paths
    size             : Safe_UInt                                        # Updated content size in bytes
    timestamp        : Timestamp_Now                                    # Update timestamp
    updated_content  : bool                                             # Content files updated
    updated_hash     : bool                                             # Hash reference updated
    updated_metadata : bool                                             # Metadata files updated
    updated_id_ref   : bool                                             # ID reference updated