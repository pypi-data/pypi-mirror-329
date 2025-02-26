from typing import Dict

from pydantic import RootModel


class ApiFullTranslationCacheResponse(RootModel[Dict[str, Dict[str, str]]]):
    pass


class ApiLangTranslationCacheResponse(RootModel[Dict[str, str]]):
    pass
