import enum
from typing import List, Literal, Optional

from kisters.network_store.model_library.base import (
    BaseControl as _BaseControl,
)
from kisters.network_store.model_library.base import (
    ExtractEnum,
    TypeEnum,
)
from kisters.network_store.model_library.base import (
    Model as _Model,
)
from pydantic import Field


class _Control(_BaseControl):
    domain: Literal["water"] = "water"
    name: Optional[str] = Field(
        None,
        description="Optional node name",
    )


class OperatorEnum(str, enum.Enum):
    GT = "gt"
    LT = "lt"


class StatusEnum(str, enum.Enum):
    ON = "on"
    OFF = "off"


class Threshold(_Model):
    threshold: float
    operator: OperatorEnum
    status: StatusEnum


class DeadbandControl(_Control):
    element_class: Literal["DeadbandControl"] = "DeadbandControl"
    thresholds: List[Threshold]


class CustomParameter(_Model):
    name: str
    value: float


class CustomIO(_Model):
    type: TypeEnum
    variable: str
    path: str
    extract: ExtractEnum


class CustomControl(_Control):
    element_class: Literal["CustomControl"] = "CustomControl"
    name: str
    io: List[CustomIO]
    parameters: List[CustomParameter]
