# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .date_part_expr_arg import DatePartExprArg
from .date_part_expr_date_part import DatePartExprDatePart
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class DatePartExpr(UniversalBaseModel):
    arg: DatePartExprArg
    date_part: DatePartExprDatePart

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
