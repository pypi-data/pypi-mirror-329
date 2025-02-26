# from typing import Any, Dict, Optional
# from redis import Redis
#
# from translation_sdk.constants import TRANSLATON_SERVICE_STORAGE_PREFIX
#
#
# def check_key_exist(
#     redis_connection: Redis[bytes],
#     key: Optional[str] = None,
# ) -> bool:
#     key = key[:-1] if key.endswith('.') else key
#     return redis_connection.exists(f'{TRANSLATON_SERVICE_STORAGE_PREFIX}.{key}??')
