from unittest                                       import TestCase
from mgraph_ai_service_cache_client.utils.Version   import version__mgraph_ai_service_cache_client
from tests.unit.Cache_Client__Fast_API__Test_Objs   import setup__cache_client__fast_api_test_objs, TEST_API_KEY__NAME, TEST_API_KEY__VALUE


class test_Routes__Info__client(TestCase):
    @classmethod
    def setUpClass(cls):
        with setup__cache_client__fast_api_test_objs() as _:
            cls.client = _.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE

    def test__info_version(self):
        response = self.client.get('/info/versions')
        assert response.status_code == 200
        assert response.json().get('mgraph_ai_service_cache_client') == version__mgraph_ai_service_cache_client

    def test__info_status(self):
        response = self.client.get('/info/status')
        result = response.json()
        assert response.status_code == 200
        assert result['name'  ]     == 'mgraph_ai_service_cache_client'
        assert result['status']     == 'operational'