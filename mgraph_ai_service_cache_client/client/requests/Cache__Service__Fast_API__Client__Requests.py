import requests
from typing                                                                                                             import Any, Optional, Dict
from osbot_utils.decorators.methods.cache_on_self                                                                       import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                                    import Type_Safe
from starlette.testclient                                                                                               import TestClient
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config                     import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.requests.schemas.Schema__Cache__Service__Fast_API__Client__Requests__Result  import Schema__Cache__Service__Fast_API__Client__Requests__Result
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode                                    import Enum__Client__Mode




class Cache__Service__Fast_API__Client__Requests(Type_Safe):
    config       : Cache__Service__Fast_API__Client__Config                         # Service__Fast_API__Client__Config
    #_server      : Optional[Any]              = None                               # Fast_API_Server for local
    #_session     : requests.Session         = None                                  # Session for remote

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self._setup_mode()

    @cache_on_self
    def test_client(self):
        if self.config.fast_api_app is None:
            raise Exception("in Cache__Service__Fast_API__Client__Requests.test_client the target self.config.fast_api_app must be configured")
        return TestClient(self.config.fast_api_app)

    @cache_on_self
    def session(self):
        session = requests.Session()
        if hasattr(self.config, 'api_key') and self.config.api_key:
            session.headers['Authorization'] = f'Bearer {self.config.api_key}'
        return session


    # def _setup_mode(self):                                                         # Initialize the appropriate execution backend
    #
    #     if self.mode == Enum__Client__Mode.IN_MEMORY:                              # In-memory mode with TestClient
    #     if self._app:
    #         self.mode = Enum__Client__Mode.IN_MEMORY
    #         from fastapi.testclient import TestClient
    #         self._test_client = TestClient(self._app)
    #
    #     # elif self._server:                                                         # Local server mode
    #     #     self.mode = Enum__Client__Mode.LOCAL_SERVER
    #     #     from osbot_fast_api.utils.Fast_API_Server import Fast_API_Server
    #     #     if not isinstance(self._server, Fast_API_Server):
    #     #         self._server = Fast_API_Server(app=self._server)
    #     #         self._server.start()
    #
    #     else:                                                                      # Remote mode
    #         self.mode     = Enum__Client__Mode.REMOTE
    #         self._session = requests.Session()
    #         self._configure_session()

    # def _configure_session(self):                                                  # Configure session for remote calls
    #     if self._session:                                                          # Add any auth headers from config
    #         if hasattr(self.config, 'api_key') and self.config.api_key:
    #             self._session.headers['Authorization'] = f'Bearer {self.config.api_key}'

    def execute(self, method  : str              ,                                 # HTTP method (GET, POST, etc)
                      path     : str              ,                                 # Endpoint path
                      body     : Any        = None,                                 # Request body
                      headers  : Optional[Dict] = None                              # Additional headers
                ) -> Schema__Cache__Service__Fast_API__Client__Requests__Result:                          # Execute request transparently based on mode
                                                                                    # Merge headers
        request_headers = {**self.auth_headers(), **(headers or {})}
                                                                                    # Execute based on mode
        if self.config.mode == Enum__Client__Mode.IN_MEMORY:
            response = self._execute_in_memory(method, path, body, request_headers)
        else:
            response = self._execute_remote(method, path, body, request_headers)
                                                                                    # Convert to unified result
        return self._build_result(response, path)

    def _execute_in_memory(self, method  : str  ,                                  # HTTP method
                                path     : str  ,                                  # Endpoint path
                                body     : Any  ,                                  # Request body
                                headers  : Dict                                    # Headers
                         ):                                                        # Execute using FastAPI TestClient
        method_func = getattr(self.test_client(), method.lower())
        if body:
            if type(body) is bytes:
                return method_func(path, data=body, headers=headers)
            else:
                return method_func(path, json=body, headers=headers)
        else:
            return method_func(path, headers=headers)

    # def _execute_local_server(self, method  : str  ,                               # HTTP method
    #                                path     : str  ,                               # Endpoint path
    #                                body     : Any  ,                               # Request body
    #                                headers  : Dict                                 # Headers
    #                         ):                                                     # Execute using local Fast_API_Server
    #     url         = f"{self._server.url()}{path}"
    #     method_func = getattr(requests, method.lower())
    #     if body:
    #         return method_func(url, json=body, headers=headers)
    #     else:
    #         return method_func(url, headers=headers)

    def _execute_remote(self, method  : str  ,                                     # HTTP method
                             path     : str  ,                                     # Endpoint path
                             body     : Any  ,                                     # Request body
                             headers  : Dict                                       # Headers
                      ):                                                           # Execute using requests to remote service
        url         = f"{self.config.base_url}{path}"
        method_func = getattr(self.session(), method.lower())
        if body:
            if type(body) is bytes:                                                 # todo: BUG need to support submitting bytes like how we are doing here
                headers["Content-Type"]=  "application/octet-stream"                #       we also need to set this content header
                return method_func(url, data=body, headers=headers)                 #
            else:                                                                   #
                return method_func(url, json=body, headers=headers)
        else:
            return method_func(url, headers=headers)

    def _build_result(self, response ,                                             # Response object
                           path                                                    # Path requested
                    ) -> Schema__Cache__Service__Fast_API__Client__Requests__Result:                     # Convert any response type to unified result

        json_data = None
        text_data = None
                                                                                    # Try to extract JSON
        try:
            json_data = response.json()
        except:
            pass
                                                                                    # Try to extract text
        try:
            text_data = response.text
        except:
            pass

        return Schema__Cache__Service__Fast_API__Client__Requests__Result(
            status_code = response.status_code                                   ,
            json        = json_data                                             ,
            text        = text_data                                             ,
            content     = response.content if hasattr(response, 'content') else b"",
            headers     = dict(response.headers) if hasattr(response, 'headers') else {},
            path        = path
        )

    def auth_headers(self) -> Dict[str, str]:                                      # Get authentication headers from config
        headers = {}
                                                                                    # Add API key if configured
        if hasattr(self.config, 'api_key_header') and hasattr(self.config, 'api_key'):
            if self.config.api_key_header and self.config.api_key:
                headers[self.config.api_key_header] = self.config.api_key

        return headers