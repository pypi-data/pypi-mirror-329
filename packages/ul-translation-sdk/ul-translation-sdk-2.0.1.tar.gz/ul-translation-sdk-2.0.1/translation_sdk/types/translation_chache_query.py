from typing import Optional

from ul_api_utils.api_resource.api_request import ApiRequestQuery


class ApiTranslactionCacheQuery(ApiRequestQuery):
    prefix: Optional[str] = None
    postfix: Optional[str] = None
