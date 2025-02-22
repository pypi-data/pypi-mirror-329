# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class AppointmentType(str, enum.Enum):
    PHLEBOTOMY = "phlebotomy"
    PATIENT_SERVICE_CENTER = "patient_service_center"

    def visit(
        self, phlebotomy: typing.Callable[[], T_Result], patient_service_center: typing.Callable[[], T_Result]
    ) -> T_Result:
        if self is AppointmentType.PHLEBOTOMY:
            return phlebotomy()
        if self is AppointmentType.PATIENT_SERVICE_CENTER:
            return patient_service_center()
