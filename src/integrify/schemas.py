import json
from enum import Enum
from typing import ClassVar, Generic, TypeVar, Union

from pydantic import BaseModel, Field, field_validator

_ResponseT = TypeVar('_ResponseT', bound=Union[BaseModel, dict])


class Environment(str, Enum):
    TEST = 'test'
    PROD = 'prod'


class APIResponse(BaseModel, Generic[_ResponseT]):
    """Cavab sorğu base payload tipi. Generic tip-i qeyd etmıəklə
    sorğu cavabını validate edə bilərsiniz.
    """

    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: _ResponseT = Field(validation_alias='content')
    """Cavab sorğusunun body-si"""

    @field_validator('body', mode='before')
    @classmethod
    def convert_to_dict(cls, v: Union[str, bytes]):
        """Binary content-i dict-ə çevirərək, validation-a hazır vəziyyətə gətirir."""
        return json.loads(v)


class PayloadBaseModel(BaseModel):
    URL_PARAM_FIELDS: ClassVar[set[str]] = set()

    @classmethod
    def from_args(cls, *args, **kwds):
        """Verilən `*args` və `**kwds` (və ya `**kwargs`) parametrlərini birləşdirərək
        Pydantic validasiyası edən funksiya. Positional arqumentlər üçün (`*args`) Pydantic
        modelindəki field-lərin ardıcıllığı və çağırılan funksiyada parametrlərinin ardıcıllığı
        EYNİ OLMALIDIR, əks halda, bu method yararsızdır.
        """
        return cls.model_validate({**dict(zip(cls.model_fields.keys(), args)), **kwds})
