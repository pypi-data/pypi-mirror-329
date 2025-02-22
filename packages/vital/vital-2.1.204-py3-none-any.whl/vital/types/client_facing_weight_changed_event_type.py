# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ClientFacingWeightChangedEventType(str, enum.Enum):
    DAILY_DATA_WEIGHT_CREATED = "daily.data.weight.created"
    DAILY_DATA_WEIGHT_UPDATED = "daily.data.weight.updated"

    def visit(
        self,
        daily_data_weight_created: typing.Callable[[], T_Result],
        daily_data_weight_updated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ClientFacingWeightChangedEventType.DAILY_DATA_WEIGHT_CREATED:
            return daily_data_weight_created()
        if self is ClientFacingWeightChangedEventType.DAILY_DATA_WEIGHT_UPDATED:
            return daily_data_weight_updated()
