from enum import Enum
from typing import Annotated, Any, Literal, Optional, Union

from kisters.network_store.model_library.base import (
    BaseNode as _BaseNode,
)
from kisters.network_store.model_library.base import (
    Model as _Model,
)
from pydantic import Field, field_validator


class _Node(_BaseNode):
    domain: Literal["water"] = "water"
    name: Annotated[Optional[str], Field(description="Optional node name")] = None


class LevelFlow(_Model):
    level: Annotated[float, Field(description="Water level in m")]
    flow: Annotated[float, Field(ge=0.0, description="Flow in CM")]


class LevelFlowEquation(_Model):
    a3: float = Field(0.0, description="a3 * level^3")
    a2: float = Field(0.0, description="a2 * level^2")
    a1: float = Field(0.0, description="a1 * level")
    a0: float = Field(0.0, description="a0")
    level_min: float = Field(..., description="Minimum level")
    level_max: float = Field(..., description="Maximum level")


class InterpEnum(str, Enum):
    linear = "linear"
    bspline = "bspline"


class NodeSchematizationModeEnum(str, Enum):
    SEQUENTIAL = "sequential"
    COLLOCATED = "collocated"


class Junction(_Node):
    element_class: Literal["Junction"] = "Junction"
    level_flow_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-storage interpolation approach"
    )
    level_flow_schematization_mode: Optional[NodeSchematizationModeEnum] = Field(
        NodeSchematizationModeEnum.SEQUENTIAL,
        description="Schematization mode of the optional rating curve (sequential, collocated)",
    )
    level_flow: Optional[Union[list[LevelFlow], LevelFlowEquation]] = Field(
        None,
        description="Optional level-flow rating curve",
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )
    catchment_uid: Optional[str] = Field(
        None, description="Unique identifier of the catchment"
    )


class LevelBoundary(_Node):
    element_class: Literal["LevelBoundary"] = "LevelBoundary"
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )


class FlowBoundary(_Node):
    element_class: Literal["FlowBoundary"] = "FlowBoundary"
    level_flow_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-storage interpolation approach"
    )
    level_flow_schematization_mode: Optional[NodeSchematizationModeEnum] = Field(
        NodeSchematizationModeEnum.SEQUENTIAL,
        description="Schematization mode of the optional rating curve (sequential, collocated)",
    )
    level_flow: Optional[list[LevelFlow]] = Field(
        None,
        description="Optional level-flow rating curve",
        min_length=4,
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class LevelVolume(_Model):
    level: float = Field(..., description="Reservoir level in m")
    volume: float = Field(
        ..., ge=0.0, description="Reservoir volume in CM (default), MCM, BCM"
    )


class LevelVolumeEquation(_Model):
    a3: float = Field(0.0, description="a3 * level^3")
    a2: float = Field(0.0, description="a2 * level^2")
    a1: float = Field(0.0, description="a1 * level")
    a0: float = Field(0.0, description="a0")
    level_min: float = Field(..., description="Minimum level")
    level_max: float = Field(..., description="Maximum level")


class StorageLevelCapacity(_Model):
    level: float = Field(..., description="Reservoir level in m")
    capacity: float = Field(..., ge=0.0, description="Total outflow capacity in m^3/s")


class _WeirParameters(_Model):
    factor: float = Field(
        ..., description="Weir factor, Q = factor * (level - crest_level) ** 1.5"
    )
    crest_level: float = Field(
        ...,
        description="Weir crest level in m, Q = factor * (level - crest_level) ** 1.5",
    )


class HeatModel(str, Enum):
    NONE = "none"
    EXCESS_TEMPERATURE = "excess_temperature"


class Storage(_Node):
    element_class: Literal["Storage"] = "Storage"
    schematization_mode: NodeSchematizationModeEnum = Field(
        NodeSchematizationModeEnum.COLLOCATED,
        description="Storage schematization model (default: collocated, sequential)",
    )
    flow_boundary: Optional[bool] = Field(
        False,
        description="Optional inflow or lateral flow into the Storage node",
    )
    volume_unit: Optional[str] = Field(
        None, description="Optional volume unit: CM (default), MCM, BCM"
    )
    level_volume: Union[list[LevelVolume], LevelVolumeEquation] = Field(
        ...,
        description="Mandatory level-storage table or equation providing the "
        "storage volume per level",
    )
    level_volume_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-storage interpolation approach"
    )
    level_capacity: Optional[list[StorageLevelCapacity]] = Field(
        None,
        description="Optional level-capacity table providing the "
        "maximum total outflow per level",
        min_length=4,
    )
    level_capacity_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-capacity interpolation approach"
    )
    level_uncontrolled: Optional[Union[list[LevelFlow], _WeirParameters]] = Field(
        None,
        description="Optional level-uncontrolled table or weir parameters "
        "providing the uncontrolled flow per level",
    )
    level_uncontrolled_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline,
        description="Level-uncontrolled flow interpolation approach for table option",
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )
    level_full: Optional[float] = Field(
        None,
        description="Full reservoir level (corresponds to filling degree of 100%)",
    )
    heat_model: Optional[HeatModel] = Field(
        HeatModel.NONE,
        description="Optional heat model for the simulation of water temperature",
    )

    @field_validator("level_uncontrolled")
    def check_min_length(cls, v: Any) -> Any:
        if isinstance(v, list) and len(v) < 4:
            msg = "level_uncontrolled must have at least 4 items if it is a list"
            raise ValueError(msg)
        return v

    @field_validator("level_volume")
    @classmethod
    def check_monotonic_volume(cls, v: Any) -> Any:
        if isinstance(v, list):
            # table of level volume pairs
            for a, b in zip(v, v[1:]):
                if a.level >= b.level:
                    msg = f"Level must be strictly increasing ({a.level} >= {b.level})"
                    raise ValueError(msg)
                if a.volume >= b.volume:
                    msg = (
                        f"Volume must be strictly increasing ({a.volume} >= {b.volume})"
                    )
                    raise ValueError(msg)
        else:
            # level volume equation
            if (
                3.0 * v.a3 * v.level_min * v.level_min + 2.0 * v.a2 * v.level_min + v.a1
                < 0.0
            ) or (
                3.0 * v.a3 * v.level_max * v.level_max + 2.0 * v.a2 * v.level_max + v.a1
                < 0.0
            ):
                msg = "Volume and its derivative must be strictly increasing in level volume eq."
                raise ValueError(msg)
        return v

    @field_validator("level_capacity")
    @classmethod
    def check_monotonic_capacity(cls, v: Any) -> Any:
        if isinstance(v, list):
            for a, b in zip(v, v[1:]):
                if a.level >= b.level:
                    msg = "Level must be strictly increasing ({a.level} >= {b.level})"
                    raise ValueError(msg)
                if a.capacity > b.capacity:
                    msg = "Volume must be increasing ({a.capacity} > {b.capacity})"
                    raise ValueError(msg)
        return v


class HydraulicNode(_Node):
    element_class: Literal["HydraulicNode"] = "HydraulicNode"
    flow_boundary: Optional[bool] = Field(
        False,
        description="Optional inflow or lateral flow into the hydraulic node",
    )
    volume_unit: Optional[str] = Field(
        None, description="Optional volume unit: CM (default), MCM, BCM"
    )
    level_volume: Union[list[LevelVolume], LevelVolumeEquation] = Field(
        ...,
        description="Mandatory level-storage table or equation providing the "
        "storage volume per level",
    )
    level_volume_interp: Optional[InterpEnum] = Field(
        InterpEnum.bspline, description="Level-storage interpolation approach"
    )
    heat_model: Optional[HeatModel] = Field(
        HeatModel.NONE,
        description="Optional heat model for the simulation of water temperature",
    )

    @field_validator("level_volume")
    @classmethod
    def check_monotonic_volume(cls, v: Any) -> Any:
        if isinstance(v, list):
            # table of level volume pairs
            for a, b in zip(v, v[1:]):
                if a.level >= b.level:
                    msg = f"Level must be strictly increasing ({a.level} >= {b.level})"
                    raise ValueError(msg)
                if a.volume >= b.volume:
                    msg = (
                        f"Volume must be strictly increasing ({a.volume} >= {b.volume})"
                    )
                    raise ValueError(msg)
        else:
            # level volume equation
            if (2.0 * v.a2 * v.level_min + v.a1 < 0.0) or (
                2.0 * v.a2 * v.level_max + v.a1 < 0.0
            ):
                msg = "Volume must be strictly increasing in level volume equation"
                raise ValueError(msg)
        return v


class HBV(_Node):
    element_class: Literal["HBV"] = "HBV"
    schematization_mode: NodeSchematizationModeEnum = Field(
        NodeSchematizationModeEnum.COLLOCATED,
        description="Storage schematization model (default: collocated, sequential)",
    )
    # input
    pcalt: Optional[float] = Field(
        0.0,
        description="Altitude correction factor for precipitation [-], "
        "P = P * (1 + PCALT*(Z-ZREF))",
    )
    ecalt: Optional[float] = Field(
        0.0,
        description="Altitude correction factor for evaporation [-], "
        "EP = EP * (1 - ECALT*(Z-ZREF))",
    )
    ecf: Optional[float] = Field(
        1.0, ge=0.0, description="Evaporation correction factor [-]"
    )
    tcalt: Optional[float] = Field(
        0.0,
        description="Altitude correction factor for T [-], "
        "T = T - TCALT*(Z-ZREF)/100.0",
    )
    z: Optional[float] = Field(
        0.0,
        ge=0.0,
        description="Average altitude [meters above sea level]",
    )
    zref: Optional[float] = Field(
        0.0,
        ge=0.0,
        description="Reference altitude [meters above sea level]",
    )
    tt: Optional[float] = Field(
        1.0,
        ge=-5.0,
        le=5.0,
        description="Temperature limit for transition between snow and rain [oC]",
    )
    tti: Optional[float] = Field(
        2.0,
        ge=0.0,
        le=10.0,
        description="Temperature interval with both snow and rain [oC]",
    )
    rfcf: Optional[float] = Field(
        1.0, ge=0.0, description="Correction factor for rainfall [-]"
    )
    sfcf: Optional[float] = Field(
        1.0, ge=0.0, description="Correction factor for snowfall [-]"
    )

    # snow
    whc: Optional[float] = Field(
        0.1, ge=0.0, description="Maximum water holding capacity factor [-]"
    )
    cfmax: Optional[float] = Field(
        2.5, ge=0.0, description="Degree day factor [mm/(oC*day)]"
    )
    ttm: Optional[float] = Field(
        1.0, ge=-5.0, le=5.0, description="Temperature threshold for melting [oC]"
    )
    cfr: Optional[float] = Field(0.1, ge=0.0, description="Refreezing factor [-]")

    # interception
    lic: Optional[float] = Field(
        0.0, ge=0.0, description="Capacity of the interception storage [mm]"
    )

    # soil
    fc: Optional[float] = Field(
        100.0,
        ge=20.0,
        le=600.0,
        description="Field capacity of soil, i.e. maximum soil moisture content [mm]",
    )
    lp: Optional[float] = Field(
        0.5, ge=0.2, le=1.0, description="Limit for potential evapotranspiration [-]"
    )
    beta: Optional[float] = Field(
        1.5,
        ge=1.0,
        le=8.0,
        description="Exponential parameter for transformation "
        "from soil moisture to runoff",
    )
    cflux: Optional[float] = Field(
        0.05, ge=0.0, description="Daily maximum amount of capillary flow"
    )
    etf: Optional[float] = Field(0.0, description="Temperature correction factor")

    # response
    alpha: Optional[float] = Field(
        0.5, ge=0.2, le=2.0, description="Response parameter [-]"
    )
    perc: Optional[float] = Field(
        2.5,
        ge=0.0,
        le=6.0,
        description="Daily percolation rate from upper"
        " to lower zone response storage [mm/day]",
    )
    k: Optional[float] = Field(
        0.05, gt=0.0, description="Recession coefficient for the upper zone storage"
    )
    k1: Optional[float] = Field(
        0.05, gt=0.0, description="Recession coefficient for the lower zone storage"
    )
    area: float = Field(..., gt=0.0, description="Area of the catchment [km2]")
