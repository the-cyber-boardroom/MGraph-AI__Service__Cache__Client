# ═══════════════════════════════════════════════════════════════════════════════
# test_Cache__Service__Client
# Tests for refactored Cache service client
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                           import TestCase
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client                          import Cache__Service__Client
from mgraph_ai_service_cache_client.client.cache_client.Cache__Service__Client__Requests                import Cache__Service__Client__Requests
from mgraph_ai_service_cache_client.client.client_contract.admin.Cache__Service__Client__Admin__Storage import Cache__Service__Client__Admin__Storage
from mgraph_ai_service_cache_client.client.client_contract.data.Cache__Service__Client__Data            import Cache__Service__Client__Data
from mgraph_ai_service_cache_client.client.client_contract.data.Cache__Service__Client__Data__Store     import Cache__Service__Client__Data__Store
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Delete    import Cache__Service__Client__File__Delete
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Exists    import Cache__Service__Client__File__Exists
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Retrieve  import Cache__Service__Client__File__Retrieve
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Store     import Cache__Service__Client__File__Store
from mgraph_ai_service_cache_client.client.client_contract.file.Cache__Service__Client__File__Update    import Cache__Service__Client__File__Update
from mgraph_ai_service_cache_client.client.client_contract.info.Service__Fast_API__Client__Info         import Cache__Service__Client__Info
from mgraph_ai_service_cache_client.client.client_contract.namespace.Cache__Service__Client__Namespace  import Cache__Service__Client__Namespace
from mgraph_ai_service_cache_client.client.client_contract.namespace.Cache__Service__Client__Namespaces import Cache__Service__Client__Namespaces
from mgraph_ai_service_cache_client.client.client_contract.server.Cache__Service__Client__Server        import Cache__Service__Client__Server
from mgraph_ai_service_cache_client.client.client_contract.zip.Cache__Service__Client__Zip              import Cache__Service__Client__Zip
from osbot_utils.utils.Objects                                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe


# ═══════════════════════════════════════════════════════════════════════════════
# Unit Tests - Client Structure
# ═══════════════════════════════════════════════════════════════════════════════

class test_Cache__Service__Client(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_service_client = Cache__Service__Client()

    def test__init__(self):                                                     # Test auto-initialization
        with self.cache_service_client as _:
            assert type(_)         is Cache__Service__Client
            assert base_classes(_) == [Type_Safe, object]
                                                                                # No config attribute - stateless!

    def test__requests__returns_transport_with_service_type(self):              # Test requests creates transport
        with self.cache_service_client as _:
            requests = _.requests()
            assert type(requests)        is Cache__Service__Client__Requests
            assert requests.service_type is Cache__Service__Client
            
    def test__requests__cached_on_self(self):                                   # Test requests is cached
        with self.cache_service_client as _:
            requests_1 = _.requests()
            requests_2 = _.requests()
            assert requests_1 is requests_2

    def test__store__returns_correct_type(self):                                # Test store() returns domain class
        with self.cache_service_client as _:
            store = _.store()
            assert type(store) is Cache__Service__Client__File__Store

    def test__store__receives_requests(self):                                   # Test store receives requests
        with self.cache_service_client as _:
            store = _.store()
            assert store.requests is _.requests()

    def test__retrieve__returns_correct_type(self):                             # Test retrieve() returns domain class
        with self.cache_service_client as _:
            retrieve = _.retrieve()
            assert type(retrieve) is Cache__Service__Client__File__Retrieve

    def test__exists__returns_correct_type(self):                               # Test exists() returns domain class
        with self.cache_service_client as _:
            exists = _.exists()
            assert type(exists) is Cache__Service__Client__File__Exists

    def test__delete__returns_correct_type(self):                               # Test delete() returns domain class
        with self.cache_service_client as _:
            delete = _.delete()
            assert type(delete) is Cache__Service__Client__File__Delete

    def test__update__returns_correct_type(self):                               # Test update() returns domain class
        with self.cache_service_client as _:
            update = _.update()
            assert type(update) is Cache__Service__Client__File__Update

    def test__data_store__returns_correct_type(self):                           # Test data_store() returns domain class
        with self.cache_service_client as _:
            data_store = _.data_store()
            assert type(data_store) is Cache__Service__Client__Data__Store

    def test__data__returns_correct_type(self):                                 # Test data() returns domain class
        with self.cache_service_client as _:
            data = _.data()
            assert type(data) is Cache__Service__Client__Data

    def test__zip__returns_correct_type(self):                                  # Test zip() returns domain class
        with self.cache_service_client as _:
            zip_client = _.zip()
            assert type(zip_client) is Cache__Service__Client__Zip

    def test__namespace__returns_correct_type(self):                            # Test namespace() returns domain class
        with self.cache_service_client as _:
            namespace = _.namespace()
            assert type(namespace) is Cache__Service__Client__Namespace

    def test__namespaces__returns_correct_type(self):                           # Test namespaces() returns domain class
        with self.cache_service_client as _:
            namespaces = _.namespaces()
            assert type(namespaces) is Cache__Service__Client__Namespaces

    def test__admin_storage__returns_correct_type(self):                        # Test admin_storage() returns domain class
        with self.cache_service_client as _:
            admin_storage = _.admin_storage()
            assert type(admin_storage) is Cache__Service__Client__Admin__Storage

    def test__server__returns_correct_type(self):                               # Test server() returns domain class
        with self.cache_service_client as _:
            server = _.server()
            assert type(server) is Cache__Service__Client__Server

    def test__info__returns_correct_type(self):                                 # Test info() returns domain class
        with self.cache_service_client as _:
            info = _.info()
            assert type(info) is Cache__Service__Client__Info

    def test__all_domain_methods__receive_same_requests(self):                  # All domain ops get same requests instance
        with self.cache_service_client as _:
            requests = _.requests()
            assert _.store().requests        is requests
            assert _.retrieve().requests     is requests
            assert _.exists().requests       is requests
            assert _.delete().requests       is requests
            assert _.info().requests         is requests


