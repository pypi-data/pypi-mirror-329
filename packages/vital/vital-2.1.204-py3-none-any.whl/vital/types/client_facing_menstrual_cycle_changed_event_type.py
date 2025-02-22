# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ClientFacingMenstrualCycleChangedEventType(str, enum.Enum):
    DAILY_DATA_MENSTRUAL_CYCLE_CREATED = "daily.data.menstrual_cycle.created"
    DAILY_DATA_MENSTRUAL_CYCLE_UPDATED = "daily.data.menstrual_cycle.updated"

    def visit(
        self,
        daily_data_menstrual_cycle_created: typing.Callable[[], T_Result],
        daily_data_menstrual_cycle_updated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ClientFacingMenstrualCycleChangedEventType.DAILY_DATA_MENSTRUAL_CYCLE_CREATED:
            return daily_data_menstrual_cycle_created()
        if self is ClientFacingMenstrualCycleChangedEventType.DAILY_DATA_MENSTRUAL_CYCLE_UPDATED:
            return daily_data_menstrual_cycle_updated()
