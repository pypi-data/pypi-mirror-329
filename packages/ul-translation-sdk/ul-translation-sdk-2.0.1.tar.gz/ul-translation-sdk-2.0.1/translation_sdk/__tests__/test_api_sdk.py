# import unittest
#
# from ul_api_utils.modules.api_sdk import ApiSdk
# from ul_api_utils.modules.api_sdk_config import ApiSdkConfig
#
# from translation_sdk.translation_api_sdk import TranslationApiSdk
# from translation_sdk.translation_api_sdk_config import TranslationApiSdkConfig, TranslationCacheTypeEnum
#
#
# class MyTestCase(unittest.TestCase):
#     def test_sdk_init(self):
#         api_sdk = ApiSdk(ApiSdkConfig())
#         flask_app = api_sdk.init_with_flask(__name__)
#         translation_sdk = TranslationApiSdk(
#             TranslationApiSdkConfig(
#                 public_api_url='some_url',
#                 cache_type=TranslationCacheTypeEnum.IN_MEMORY_LRU,
#                 client_prefix='test_service',
#             )
#         )
#         print(translation_sdk.get_full_translation_cache())
#
#
# if __name__ == '__main__':
#     unittest.main()
#
