from typing import Literal

from kisters.network_store.model_library.base import BaseGroup


class _Group(BaseGroup):
    domain: Literal["water"] = "water"


class HydroPowerPlant(_Group):
    element_class: Literal["HydroPowerPlant"] = "HydroPowerPlant"


class PumpingStation(_Group):
    element_class: Literal["PumpingStation"] = "PumpingStation"


class SluiceComplex(_Group):
    element_class: Literal["SluiceComplex"] = "SluiceComplex"


class WeirComplex(_Group):
    element_class: Literal["WeirComplex"] = "WeirComplex"


class GateComplex(_Group):
    element_class: Literal["GateComplex"] = "GateComplex"


class Waterfall(_Group):
    element_class: Literal["Waterfall"] = "Waterfall"


class Subsystem(_Group):
    element_class: Literal["Subsystem"] = "Subsystem"
