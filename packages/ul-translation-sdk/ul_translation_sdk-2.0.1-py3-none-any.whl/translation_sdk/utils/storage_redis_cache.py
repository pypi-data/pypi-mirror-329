# from functools import lru_cache, wraps
# from typing import Callable, Any
# from datetime import datetime, timedelta
#
# from redis import Redis
#
# from translation_sdk.helpers.redis_client import check_key_exist
#
#
# def redis_cache(redis_connection: Redis[bytes], seconds: int):      # type: ignore
#     @wraps(func)
#     def wrapped_func(*args, **kwargs):      # type: ignore
#         if datetime.utcnow() >= func.expiration:
#             func.cache_clear()
#             func.expiration = datetime.utcnow() + func.lifetime
#
#         return func(*args, **kwargs)
#     return wrapped_func
#     def wrapper_cache(func: Callable[..., Any]):        # type: ignore
#         if not check_key_exist(redis_connection, func.__name__):
#             func = lru_cache(maxsize=None)(func)
#
#     return wrapper_cache
