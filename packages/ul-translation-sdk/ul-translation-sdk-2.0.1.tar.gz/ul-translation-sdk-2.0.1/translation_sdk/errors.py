from typing import Iterable


class TranslatorChoicesValidationError(Exception):
    def __init__(self, msg: str, choices: Iterable[str]) -> None:
        self.choices = choices
        self.msg = msg if msg else 'value is not a valid enumeration member'
        super().__init__(f'{self.msg} : {", ".join(choices)}')

    def to_value_error(self) -> None:
        raise ValueError(self.msg)


class TranslatorChoicesMapValidationError(TranslatorChoicesValidationError):
    pass


class TranslationAbstractError(Exception):
    def __init__(self, message: str, error: Exception, status_code: int) -> None:
        assert isinstance(message, str), f'message must be str. "{type(message).__name__}" was given'
        assert isinstance(error, Exception), f'error must be Exception. "{type(error).__name__}" was given'
        super(TranslationAbstractError, self).__init__(f'{message} :: {str(error)} :: {status_code})')
        self.status_code = status_code
        self.error = error


class TranslationRequestError(TranslationAbstractError):
    pass


class TranslationResponseError(TranslationAbstractError):
    pass
