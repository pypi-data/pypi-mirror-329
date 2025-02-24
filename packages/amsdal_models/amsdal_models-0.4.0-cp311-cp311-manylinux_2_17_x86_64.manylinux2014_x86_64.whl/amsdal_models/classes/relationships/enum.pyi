from enum import Enum
from typing import Any

class ReferenceMode(str, Enum):
    CASCADE: str
    PROTECT: str
    RESTRICT: str
    SET_NULL: str
    SET_DEFAULT: str
    DO_NOTHING: str
    @staticmethod
    def SET(value: Any) -> None: ...
