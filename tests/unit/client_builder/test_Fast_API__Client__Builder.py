import tempfile
from unittest                                                                import TestCase

from osbot_utils.utils.Files import folder_name, parent_folder_name

from mgraph_ai_service_cache_client.client_builder.Fast_API__Client__Builder import Fast_API__Client__Builder


class test_Fast_API__Client__Builder(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client_builder          = Fast_API__Client__Builder()


    def test_create_files(self):
        saved_files = self.client_builder.create_client_files()
        assert saved_files == [ 'Service__Fast_API__Client.py'                              ,
                                'Service__Fast_API__Client__Config.py'                      ,
                                'Service__Fast_API__Client__Requests.py'                    ,
                                'admin_storage/Service__Fast_API__Client__Admin__Storage.py',
                                'auth/Service__Fast_API__Client__Set_Cookie.py'             ,
                                'data/Service__Fast_API__Client__Data.py'                   ,
                                'data/Service__Fast_API__Client__Data__Delete.py'           ,
                                'data/Service__Fast_API__Client__Data__Retrieve.py'         ,
                                'data_store/Service__Fast_API__Client__Data__Store.py'      ,
                                'delete/Service__Fast_API__Client__File__Delete.py'         ,
                                'exists/Service__Fast_API__Client__File__Exists.py'         ,
                                'info/Service__Fast_API__Client__Info.py'                   ,
                                'namespace/Service__Fast_API__Client__Namespace.py'         ,
                                'retrieve/Service__Fast_API__Client__File__Retrieve.py'     ,
                                'server/Service__Fast_API__Client__Server.py'               ,
                                'store/Service__Fast_API__Client__File__Store.py'           ,
                                'zip/Service__Fast_API__Client__Zip.py'                     ]

    def test_target_folder(self):
        with self.client_builder  as _:
            target_folder = _.target_folder()
            assert folder_name       (target_folder) == 'client_contract'
            assert parent_folder_name(target_folder) == 'mgraph_ai_service_cache_client'