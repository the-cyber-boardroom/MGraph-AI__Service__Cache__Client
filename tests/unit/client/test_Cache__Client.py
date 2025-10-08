from unittest                                                    import TestCase
from mgraph_ai_service_cache_client.client.Cache__Client         import Cache__Client
from mgraph_ai_service_cache_client.client.Cache__Client__Config import Cache__Client__Config


class test_Cache__Client(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Cache__Client()


    def test__setUpClass(self):
        with self.client as _:
            assert type(_)        is Cache__Client
            assert type(_.config) is Cache__Client__Config