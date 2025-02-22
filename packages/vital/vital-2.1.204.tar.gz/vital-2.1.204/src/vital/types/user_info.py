# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .address import Address
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class UserInfo(UniversalBaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    gender: str
    dob: str
    address: Address

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
