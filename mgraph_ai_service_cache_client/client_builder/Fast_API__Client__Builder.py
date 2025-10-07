from osbot_fast_api.client.Fast_API__Client__Generator  import Fast_API__Client__Generator
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from mgraph_ai_service_cache.fast_api.Service__Fast_API import Service__Fast_API
from mgraph_ai_service_cache_client                     import client_contract


class Fast_API__Client__Builder(Type_Safe):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache_service__fast_api = Service__Fast_API().setup()
        self.generator               = Fast_API__Client__Generator(fast_api=self.cache_service__fast_api)

    def create_client_files(self):
        with self.generator as _:
            output_dir  = self.target_folder()
            saved_files = _.save_client_files(output_dir=output_dir)
            return sorted(saved_files)

    def target_folder(self):
        return client_contract.path
