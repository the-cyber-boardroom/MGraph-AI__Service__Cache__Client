from enum import Enum


class Enum__Client__Mode(str, Enum):
    REMOTE       = "remote"                                                        # HTTP calls to deployed service
    IN_MEMORY    = "in_memory"                                                     # FastAPI TestClient (same process)
    #LOCAL_SERVER = "local_server"                                                  # Fast_API_Server (local HTTP)
