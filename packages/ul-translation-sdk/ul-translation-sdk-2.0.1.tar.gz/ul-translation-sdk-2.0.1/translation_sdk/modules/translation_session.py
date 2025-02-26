from enum import Enum
from typing import Any, Mapping, Optional, Type, Dict, TYPE_CHECKING, TypeVar, List, Iterable

from translation_sdk.constants import RE_COMMA
from translation_sdk.errors import TranslatorChoicesMapValidationError, TranslatorChoicesValidationError

if TYPE_CHECKING:
    from translation_sdk.translation_api_sdk import TranslationApiSdk

TEnum = TypeVar('TEnum', bound=Enum)


class TranslationSession:

    def __init__(self, lang: str, sdk: 'TranslationApiSdk', prefix: str = '') -> None:
        self._lang = lang
        self._translator_api = sdk

    def get_translations(self) -> Dict[str, str]:
        """get ALL translations of current lang"""
        return self._translator_api.get_lang_translation_cache(self._lang)  # type: ignore

    def i18n(self, key: str, *, default: Optional[str] = None, **kwargs: Dict[str, Any]) -> str:
        """get translate value by key"""
        assert isinstance(key, str)
        key = f'{self._translator_api._config.client_prefix}.{key}'
        if default is None:
            return self.get_translations()[key]
        return self.get_translations().get(key, str(default))

    def check_choices(self, key: str, enum: Type[Enum]) -> None:
        self.enum_map(enum, key, strict=True)
        self.i18n(f'{key}.ERROR')

    def enum_map(
        self,
        enum: Type[TEnum],
        key: str,
        *,
        enum_restrictions: List[TEnum] | None = None,
        strict: bool = True,
    ) -> Mapping[str, TEnum]:
        res = {}
        enum_iterator: Iterable[TEnum] = enum.__iter__() if enum_restrictions is None else enum_restrictions
        for v in enum_iterator:
            for k in RE_COMMA.split(self.i18n(f'{key}.ENUM.{v.name}')):
                if k:
                    res[k] = v
                elif strict:
                    raise KeyError(f'{enum.__name__} not found in translation by key "{key}.ENUM.{v.name}"')
        return res

    def validate_choices(
        self,
        value: str | None,
        key: str,
        enum: Type[TEnum],
        *,
        enum_restrictions: List[TEnum] | None = None,
        strict: bool = True,
    ) -> TEnum:
        value_raw = str(value or '').lower().strip()
        choices_map = self.enum_map(enum, key, enum_restrictions=enum_restrictions, strict=strict)
        choices = choices_map.keys()
        if value_raw not in choices:
            raise TranslatorChoicesValidationError(self.i18n(f'{key}.ERROR', default=''), choices=choices)
        res = choices_map.get(value_raw, None)
        if res is None:
            raise TranslatorChoicesMapValidationError(self.i18n(f'{key}.ERROR', default=''), choices=choices)
        return res
