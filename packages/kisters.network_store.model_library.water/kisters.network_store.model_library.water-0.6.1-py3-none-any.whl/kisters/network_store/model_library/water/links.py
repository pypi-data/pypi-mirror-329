import enum
import math
from typing import Annotated, Any, Literal, Optional, Union

from kisters.network_store.model_library.base import (
    BaseLink as _BaseLink,
)
from kisters.network_store.model_library.base import (
    Location as _Location,
)
from kisters.network_store.model_library.base import (
    Model as _Model,
)
from pydantic import (
    Field,
    StrictFloat,
    StrictStr,
    ValidationInfo,
    field_validator,
    model_validator,
)
from typing_extensions import Self


class Polygon(_Model):
    vertices: Annotated[
        Optional[list[_Location]],
        Field(description="List of boundary vertices, that define the polygons"),
    ] = None


class LinkSchematizationModeEnum(str, enum.Enum):
    SEQUENTIAL = "sequential"
    COLLOCATED = "collocated"


class _Link(_BaseLink):
    domain: Literal["water"] = "water"


class Delay(_Link):
    element_class: Literal["Delay"] = "Delay"
    schematization_mode: LinkSchematizationModeEnum = Field(
        LinkSchematizationModeEnum.COLLOCATED,
        description="Schematization model (default: collocated, sequential)",
    )
    transit_time: Optional[float] = Field(
        None,
        ge=0.0,
        description="Time delay in time steps between source and target nodes",
    )
    multiplier: Optional[Union[StrictFloat, StrictStr]] = Field(
        None, description="Optional multiplier, outflow = multiplier * delayed(inflow)"
    )
    weighting_factors: Optional[list[float]] = Field(
        None,
        description="Optional weighting factors for values at current and previous time steps",
    )

    @field_validator("weighting_factors")
    @classmethod
    def check_list_size(
        cls, v: Optional[list[float]], info: ValidationInfo
    ) -> Optional[list[float]]:
        if isinstance(v, list):
            assert len(v) >= 2, f"{info.field_name} must contain at least 2 elements"
        return v


class PipeFrictionModel(str, enum.Enum):
    DARCY_WEISBACH = "darcy-weisbach"
    HAZEN_WILLIAMS = "hazen-williams"


class Pipe(_Link):
    element_class: Literal["Pipe"] = "Pipe"
    diameter: float = Field(..., gt=0.0, description="Measured internal diameter")
    length: float = Field(..., gt=0.0, description="Longitudinal length of the pipe")
    roughness: float = Field(..., gt=0.0, description="Friction coefficient")
    model: PipeFrictionModel = Field(
        ..., description="Friction loss approximation method"
    )
    check_valve: Optional[bool] = Field(False, description="Disallow reverse flow")


class ChannelRoughnessModel(str, enum.Enum):
    CHEZY = "chezy"
    MANNING = "manning"


class HydraulicRoutingModel(str, enum.Enum):
    SAINT_VENANT = "saint-venant"
    INERTIAL_WAVE = "inertial-wave"
    DIFFUSIVE_WAVE = "diffusive-wave"


class HydraulicCrossSectionStation(_Model):
    lr: float = Field(
        ..., description="Station distance from left bank when looking downstream"
    )
    z: float = Field(..., description="Station elevation")
    roughness_correction: Optional[float] = Field(
        None,
        description="Local roughness correction (acts as multiplier on base roughness)",
    )


class HydraulicLongitudinalStation(_Model):
    roughness: float = Field(..., gt=0.0, description="Friction coefficient")
    cross_section: list[HydraulicCrossSectionStation] = Field(
        ..., min_length=3, description="List of points defining the channel bottom"
    )
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )

    @field_validator("cross_section")
    @classmethod
    def check_cross_section_stations(cls, v: Any) -> Any:
        if sorted(v, key=lambda x: x.lr) != v:
            msg = "Cross Section Stations must be specified in increasing order"
            raise ValueError(msg)
        return v

    @field_validator("cross_section")
    @classmethod
    def check_non_empty(cls, v: Any) -> Any:
        z = [x.z for x in v]
        if min(z) >= max(z):
            msg = "Empty cross section specified"
            raise ValueError(msg)
        return v


class LongitudinalDelimitedStation(_Model):
    distance: float = Field(
        ..., ge=0.0, description="Distance along channel from source node [m]"
    )


class HydraulicLongitudinalDelimitedStation(
    HydraulicLongitudinalStation, LongitudinalDelimitedStation
):
    pass


class SpatialSchematizationModeEnum(str, enum.Enum):
    CENTRAL = "central"
    UPWIND = "upwind"


class _HydraulicRouting(_Model):
    model: HydraulicRoutingModel = Field(
        ..., description="Hydraulics approximation equations"
    )
    schematization_mode: Optional[LinkSchematizationModeEnum] = Field(
        LinkSchematizationModeEnum.COLLOCATED,
        description="Channel schematization option (sequential, default: collocated)",
    )
    schematization_mode_spatial: SpatialSchematizationModeEnum = Field(
        SpatialSchematizationModeEnum.CENTRAL,
        description="Spatial schematization mode (default: central, upwind)",
    )
    stations: Union[
        HydraulicLongitudinalStation, list[HydraulicLongitudinalDelimitedStation]
    ] = Field(..., description="Longitudinal stations defining channel geometry")
    roughness_model: ChannelRoughnessModel = Field(
        ChannelRoughnessModel.CHEZY, description="Friction loss approximation method"
    )
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m3/s"
    )

    @field_validator("stations")
    @classmethod
    def stations_sorted(cls, v: Any) -> Any:
        if isinstance(v, list):
            return sorted(v, key=lambda x: x.distance)
        return v

    @field_validator("stations")
    @classmethod
    def stations_unique(cls, v: Any) -> Any:
        if isinstance(v, list):
            distances = [s.distance for s in v]
            unique_distances = sorted(set(distances))
            if distances != unique_distances:
                msg = "Two stations may not be placed at the same distance"
                raise ValueError(msg)
        return v


class MuskingumLongitudinalStation(_Model):
    model: Literal["muskingum"] = Field(
        ..., description="To which models it can be applied"
    )
    k: float = Field(..., gt=0.0, description="Storage coefficient")
    x: float = Field(..., ge=0.0, le=1.0, description="Weighting factor")


class MuskingumCungeLongitudinalStation(_Model):
    model: Literal["muskingum-cunge"] = Field(
        ..., description="To which models it can be applied"
    )
    roughness: float = Field(..., gt=0.0, description="Friction coefficient")
    roughness_model: ChannelRoughnessModel = Field(
        ..., description="Friction loss approximation method"
    )
    cross_section: list[HydraulicCrossSectionStation] = Field(
        ..., min_length=3, description="List of points defining the channel bottom"
    )
    slope: float = Field(..., gt=0.0, description="Longitudinal slope [-]")


class ReservoirLongitudinalStation(_Model):
    model: Literal["reservoir"] = Field(
        ..., description="To which models it can be applied"
    )
    p: Union[StrictFloat, StrictStr] = Field(
        ..., description="Reservoir equation multiplier"
    )
    m: Union[StrictFloat, StrictStr] = Field(
        ..., description="Reservoir equation exponent"
    )


class HydrologicRoutingModel(str, enum.Enum):
    MUSKINGUM = "muskingum"
    MUSKINGUM_CUNGE = "muskingum-cunge"
    RESERVOIR = "reservoir"


class HydrologicRouting(_Model):
    reservoir_station: Optional[ReservoirLongitudinalStation] = Field(None)
    muskingum_station: Optional[MuskingumLongitudinalStation] = Field(None)
    muskingum_cunge_station: Optional[MuskingumCungeLongitudinalStation] = Field(None)


class Channel(_Link):
    element_class: Literal["Channel"] = "Channel"
    schematization_mode: Optional[LinkSchematizationModeEnum] = Field(
        LinkSchematizationModeEnum.COLLOCATED,
        description="Channel schematization option (sequential, default: collocated)",
    )
    length: float = Field(
        ..., gt=0.0, description="Longitudinal length of the channel [m]"
    )
    hydraulic_routing: Annotated[
        Optional[_HydraulicRouting], Field(description="Hydraulic routing model")
    ] = None
    hydrologic_routing: Annotated[
        Optional[HydrologicRouting], Field(description="Hydrologic routing model")
    ] = None
    catchment: Optional[Polygon] = Field(
        None,
        description="Boundary polygon of the catchment area",
    )
    catchment_area: Optional[float] = Field(None, description="Catchment area [km^2]")

    @model_validator(mode="after")
    def check_hydraulic_distance_less_than_length(self) -> Self:
        if (
            self.hydraulic_routing
            and isinstance(self.hydraulic_routing.stations, list)
            and self.hydraulic_routing.stations[-1].distance > self.length
        ):
            msg = (
                f"Station {self.hydraulic_routing.stations[-1].distance} "
                f"distance exceeds length {self.length}"
            )
            raise ValueError(msg)
        return self


class HydraulicLink(_Link):
    element_class: Literal["HydraulicLink"] = "HydraulicLink"
    schematization_mode: Optional[LinkSchematizationModeEnum] = Field(
        LinkSchematizationModeEnum.COLLOCATED,
        description="Channel schematization option (sequential, default: collocated)",
    )
    length: float = Field(
        ..., gt=0.0, description="Longitudinal length of the channel [m]"
    )
    hydraulic_routing: Optional[_HydraulicRouting] = Field(
        None, description="Hydraulic routing model"
    )

    @model_validator(mode="after")
    def check_hydraulic_distance_less_than_length(self) -> Self:
        if (
            self.hydraulic_routing
            and isinstance(self.hydraulic_routing.stations, list)
            and self.hydraulic_routing.stations[-1].distance > self.length
        ):
            msg = (
                f"Station {self.hydraulic_routing.stations[-1].distance} "
                f"distance exceeds length {self.length}"
            )
            raise ValueError(msg)
        return self


class FlowControlledStructure(_Link):
    element_class: Literal["FlowControlledStructure"] = "FlowControlledStructure"
    min_flow: Annotated[
        float, Field(description="Minimum volumetric flow rate in m^3/s")
    ]
    max_flow: Annotated[
        float, Field(description="Maximum volumetric flow rate in m^3/s")
    ]
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )

    @model_validator(mode="after")
    def min_flow_le_max_flow(self) -> Self:
        if self.min_flow > self.max_flow:
            msg = "max_flow must be greater than min_flow"
            raise ValueError(msg)
        return self

    @field_validator("min_flow", "max_flow")
    @classmethod
    def bounds_are_real_valued(cls, v: Any) -> Any:
        if v is not None and not math.isfinite(v):
            msg = "Only real-valued bounds are allowed"
            raise ValueError(msg)
        return v


class PumpTurbineSpeedPoint(_Model):
    flow: float = Field(..., ge=0.0)
    head: float = Field(..., ge=0.0)
    speed: float = Field(1.0, ge=0.0)


class PumpTurbineEfficiencyPoint(_Model):
    flow: float = Field(..., ge=0.0)
    head: float = Field(..., ge=0.0)
    efficiency: float = Field(..., gt=0.0, le=1.0)
    standard_deviation: Optional[float] = Field(5e-3, ge=0.0, le=1.0)


class PumpTurbineHeadTWCorrection(_Model):
    link_uid: str = Field(..., pattern="^[a-zA-Z]\\w*$")
    power: int = Field(..., ge=0)
    value: float


class PumpTurbineOtherConstraints(_Model):
    flow_power: float = Field(..., ge=0.0)
    head_power: float = Field(..., ge=0.0)
    value: float


class _PumpTurbine(_Link):
    speed: Annotated[
        Optional[list[PumpTurbineSpeedPoint]],
        Field(min_length=1, description="Flow-head-speed curve of drive shaft"),
    ] = None
    efficiency: Annotated[
        Optional[list[PumpTurbineEfficiencyPoint]],
        Field(
            min_length=1,
            description="Flow-head-efficiency energy conversion curve of assembly",
        ),
    ] = None
    length: Annotated[
        Optional[float], Field(gt=0.0, description="Length of flow path")
    ] = None
    min_flow: Annotated[
        float, Field(description="Minimum volumetric flow rate in m^3/s")
    ]
    max_flow: Annotated[
        float, Field(description="Maximum volumetric flow rate in m^3/s")
    ]
    initial_flow: Annotated[
        Optional[float],
        Field(description="Initial volumetric flow rate for simulation in m^3/s"),
    ] = None
    min_head: Annotated[
        Optional[float], Field(ge=0.0, description="Minimum head in m")
    ] = None
    max_head: Annotated[
        Optional[float], Field(ge=0.0, description="Maximum head in m")
    ] = None
    min_power: Annotated[float, Field(description="Minimum power in W")]
    max_power: Annotated[float, Field(description="Maximum power in W")]
    min_speed: Annotated[
        Optional[float], Field(ge=0.0, description="Minimum speed")
    ] = None
    max_speed: Annotated[
        Optional[float], Field(ge=0.0, description="Maximum speed")
    ] = None
    head_tailwater_correction: Annotated[
        Optional[list[PumpTurbineHeadTWCorrection]],
        Field(
            description="This polynomial is added to the difference between"
            " up- and downstream levels",
        ),
    ] = None
    other_constraints: Annotated[
        Optional[list[PumpTurbineOtherConstraints]],
        Field(description="Every polynomial will be added a constraint <= 0"),
    ] = None

    @field_validator(
        "min_flow",
        "max_flow",
        "min_head",
        "max_head",
        "min_power",
        "max_power",
        "min_speed",
        "max_speed",
    )
    @classmethod
    def bounds_are_real_valued(cls, v: Any) -> Any:
        if v is not None and not math.isfinite(v):
            msg = "Only real-valued bounds are allowed"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def min_flow_le_max_flow(self) -> Self:
        if self.min_flow > self.max_flow:
            msg = "max_flow must be greater than min_flow"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def min_head_le_max_head(self) -> Self:
        if (
            self.min_head is not None
            and self.max_head is not None
            and self.min_head > self.max_head
        ):
            msg = "max_head must be greater than min_head"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def min_power_le_max_power(self) -> Self:
        if self.min_power > self.max_power:
            msg = "max_power must be greater than min_power"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def min_speed_le_max_speed(self) -> Self:
        if (
            self.min_speed is not None
            and self.max_speed is not None
            and self.min_speed > self.max_speed
        ):
            msg = "max_speed must be greater than min_speed"
            raise ValueError(msg)
        return self


class Pump(_PumpTurbine):
    element_class: Literal["Pump"] = "Pump"


class Turbine(_PumpTurbine):
    element_class: Literal["Turbine"] = "Turbine"


class ValveModel(str, enum.Enum):
    PRV = "prv"
    PSV = "psv"
    PBV = "pbv"
    FCV = "fcv"
    TCV = "tcv"
    GPV = "gpv"


class Valve(_Link):
    element_class: Literal["Valve"] = "Valve"
    model: ValveModel = Field(..., description="Specific type of valve")
    coefficient: float = Field(..., gt=0.0, description="Discharge coefficient")
    diameter: float = Field(
        ..., ge=0.0, description="Measured characteristic internal diameter"
    )
    setting: float = Field(
        ..., description="Valve setting, meaning varies with valve model"
    )


class FlowModel(str, enum.Enum):
    FREE = "free"
    SUBMERGED = "submerged"
    DYNAMIC = "dynamic"


class _FlowRelation(_Link):
    coefficient: float = Field(..., gt=0.0, description="Discharge coefficient")
    flow_model: FlowModel = Field(..., description="Flow model")


class Weir(_FlowRelation):
    element_class: Literal["Weir"] = "Weir"
    min_crest_level: Annotated[float, Field(description="Minimum crest level")]
    max_crest_level: Annotated[float, Field(description="Maximum crest level")]
    initial_crest_level: Annotated[
        Optional[float], Field(description="Initial crest level value for simulation")
    ] = None
    crest_width: Annotated[float, Field(gt=0.0, description="Crest width")]

    @model_validator(mode="after")
    def min_crest_level_le_max_crest_level(self) -> Self:
        if self.min_crest_level > self.max_crest_level:
            msg = "max_crest_level must be greater than min_crest_level"
            raise ValueError(msg)
        return self


class Direction(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BOTH = "both"


class TopDownRectangularOrifice(_FlowRelation):
    element_class: Literal["TopDownRectangularOrifice"] = "TopDownRectangularOrifice"
    width: float = Field(..., gt=0.0, description="Orifice width")
    exponent: Optional[float] = Field(
        0.5, gt=0.3, lt=0.7, description="Orifice equation exponent (default = 0.5)"
    )
    direction: Optional[Direction] = Field(
        Direction.POSITIVE, description="Allowed flow direction"
    )


class TopDownSphericalOrifice(_FlowRelation):
    element_class: Literal["TopDownSphericalOrifice"] = "TopDownSphericalOrifice"


class Drain(_FlowRelation):
    element_class: Literal["Drain"] = "Drain"
    level: float = Field(..., description="Level at which drain is installed")
    min_area: float = Field(..., ge=0.0, description="Minimum aperture area")
    max_area: float = Field(..., gt=0.0, description="Maximum aperture area")
    initial_area: Optional[float] = Field(
        None, description="Initial area value for simulation"
    )
