import os
from enum import Enum
from typing import List, Optional, Tuple, Type

from ul_api_utils.modules.api_sdk import ApiSdk
from ul_api_utils.api_resource.api_resource import ApiResource
from ul_api_utils.api_resource.api_response import HtmlApiResponse
from jinja2 import Template

from translation_sdk.translation_api_sdk import TranslationApiSdk

HERE = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(HERE, os.pardir))


def create_page(
    api_sdk: ApiSdk,
    translation_sdk: TranslationApiSdk,
    *,
    enums: Optional[List[Tuple[str, Type[Enum]]]] = None,
    keys: Optional[Tuple[str, ...]] = None,
) -> None:
    assert enums is not None or keys is not None
    with open(os.path.join(PARENT_DIR, 'templates', 'service_translations.html'), encoding='utf-8') as f:
        page_content = f.read()
    template = Template(page_content)

    @api_sdk.html_view('GET', '/translates', access=api_sdk.ACCESS_PUBLIC)
    def translation_page(api_resource: ApiResource) -> HtmlApiResponse:
        service_keys = [f'{translation_sdk._config.client_prefix}.{k}' for k in keys] if keys is not None else []
        if enums is not None:
            for enum_key in enums:
                key, enum = enum_key
                for v in enum:
                    service_keys.append(f'{translation_sdk._config.client_prefix}.{key}.ENUM.{v.value}')
                service_keys.append(f'{translation_sdk._config.client_prefix}.{key}.ERROR')
        all_translations = translation_sdk.get_full_translation_cache()
        langs = all_translations.keys()  # type: ignore
        res = HtmlApiResponse(
            content=template.render(
                langs=langs,
                keys=service_keys,
                translations=all_translations,
            ),
            status_code=200,
            ok=True,
        )
        return res
