from enum import Enum
from typing import NamedTuple


class TranslationCacheTypeEnum(Enum):
    IN_MEMORY_LRU = 'IN_MEMORY_LRU'
    # STORAGE_REDIS = 'STORAGE_REDIS'


class TranslationApiSdkConfig(NamedTuple):
    public_api_url: str
    cache_type: TranslationCacheTypeEnum = TranslationCacheTypeEnum.IN_MEMORY_LRU
    # cache_storage_uri: str = ''
    cache_ttl_s: int = 3600
    client_prefix: str = ''  # like name of client service
