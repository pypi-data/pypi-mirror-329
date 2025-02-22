# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class AuthType(str, enum.Enum):
    PASSWORD = "password"
    OAUTH = "oauth"
    EMAIL = "email"

    def visit(
        self,
        password: typing.Callable[[], T_Result],
        oauth: typing.Callable[[], T_Result],
        email: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is AuthType.PASSWORD:
            return password()
        if self is AuthType.OAUTH:
            return oauth()
        if self is AuthType.EMAIL:
            return email()
