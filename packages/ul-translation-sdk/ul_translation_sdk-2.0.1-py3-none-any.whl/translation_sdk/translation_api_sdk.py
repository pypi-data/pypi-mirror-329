import time
from functools import lru_cache
from typing import Type, Optional

from ul_api_utils.internal_api.internal_api import InternalApi
from ul_api_utils.internal_api.internal_api_response import TPyloadType

from translation_sdk.modules.translation_session import TranslationSession
from translation_sdk.types.translation_chache_query import ApiTranslactionCacheQuery
from translation_sdk.utils.internal_api_error_handler import internal_api_error_handler
from translation_sdk.translation_api_sdk_config import TranslationApiSdkConfig
from translation_sdk.types.translation_cache import ApiFullTranslationCacheResponse, ApiLangTranslationCacheResponse


class TranslationApiSdk:

    @lru_cache(maxsize=None)    # noqa: B019 # there should not be leaks memory leaks. flake8 just scared inmemory cache ;)
    def request_payload(
        self,
        _: int,
        endpoint: str,
        typed_as: Type[TPyloadType],
        prefix: str,
        postfix: str,
    ) -> TPyloadType:
        return self._public_api.request_get(
            path=endpoint,
            q=ApiTranslactionCacheQuery(
                prefix=prefix,
                postfix=postfix,
            ).model_dump(),
        ) \
            .typed(typed_as) \
            .check() \
            .payload

    def get_cache_payload(
        self,
        path: str,
        typed: Type[TPyloadType],
        prefix: Optional[str] = None,
        postfix: Optional[str] = None,
    ) -> TPyloadType:
        q_prefix = self._config.client_prefix if prefix is None else prefix
        ttl_status = round(time.time() / self._config.cache_ttl_s)
        return self.request_payload(ttl_status, path, typed, q_prefix, postfix)     # type: ignore  # Type[TPyloadType] is hashable

    def __init__(self, config: TranslationApiSdkConfig) -> None:
        self._config = config
        self._public_api = InternalApi(entry_point=self._config.public_api_url)

    def session(self, lang: str) -> 'TranslationSession':
        return TranslationSession(lang, self, prefix=self._config.client_prefix)

    @internal_api_error_handler
    def get_full_translation_cache(self, key_prefix: Optional[str] = None, key_postfix: Optional[str] = None) -> ApiFullTranslationCacheResponse:
        return self.get_cache_payload(
            '/langs/translation-cache',
            ApiFullTranslationCacheResponse,      # type: ignore
            prefix=f'{self._config.client_prefix}.{key_prefix}',
            postfix=f'{self._config.client_prefix}.{key_postfix}',
        )

    @internal_api_error_handler
    def get_lang_translation_cache(self, lang_abbr: str) -> ApiLangTranslationCacheResponse:
        return self.get_cache_payload(
            f'/langs/{lang_abbr}/translation-cache',
            ApiLangTranslationCacheResponse,      # type: ignore
        )
