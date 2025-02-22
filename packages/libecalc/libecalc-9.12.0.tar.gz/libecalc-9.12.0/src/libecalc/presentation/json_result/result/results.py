from __future__ import annotations

from _operator import attrgetter
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from libecalc.common.component_info.component_level import ComponentLevel
from libecalc.common.component_type import ComponentType
from libecalc.common.logger import logger
from libecalc.common.math.numbers import Numbers
from libecalc.common.serializable_chart import SingleSpeedChartDTO, VariableSpeedChartDTO
from libecalc.common.stream_conditions import TimeSeriesStreamConditions
from libecalc.common.time_utils import Frequency
from libecalc.common.units import Unit
from libecalc.common.utils.rates import (
    TimeSeriesBoolean,
    TimeSeriesFloat,
    TimeSeriesInt,
    TimeSeriesRate,
    TimeSeriesVolumesCumulative,
)
from libecalc.core.models.results.compressor import (
    CompressorTrainCommonShaftFailureStatus,
)
from libecalc.presentation.json_result.result.base import EcalcResultBaseModel
from libecalc.presentation.json_result.result.emission import (
    EmissionResult,
)
from libecalc.presentation.json_result.result.tabular_time_series import (
    TabularTimeSeries,
)


class NodeInfo(EcalcResultBaseModel):
    componentType: ComponentType
    component_level: ComponentLevel
    parent: Optional[str] = None  # reference parent id
    name: str


class CommonResultBase(TabularTimeSeries):
    """Base component for all results: Model, Installation, GenSet, Consumer System, Consumer, etc."""

    # we need to use camelCase here due to serialization/stub restrictions wrt FE stub generation

    is_valid: TimeSeriesBoolean

    # We need both energy usage and power rate since we sometimes want both fuel and power usage.
    energy_usage: TimeSeriesRate
    energy_usage_cumulative: TimeSeriesVolumesCumulative

    power: Optional[TimeSeriesRate] = None
    power_cumulative: Optional[TimeSeriesVolumesCumulative] = None


class ComponentResultBase(CommonResultBase, NodeInfo):
    id: str
    emissions: dict[str, EmissionResult]


class EquipmentResultBase(ComponentResultBase): ...


class AssetResult(ComponentResultBase):
    """The aggregated eCalc model result."""

    componentType: Literal[ComponentType.ASSET]
    hydrocarbon_export_rate: TimeSeriesRate
    power_electrical: Optional[TimeSeriesRate] = None
    power_electrical_cumulative: Optional[TimeSeriesVolumesCumulative] = None
    power_mechanical: Optional[TimeSeriesRate] = None
    power_mechanical_cumulative: Optional[TimeSeriesVolumesCumulative] = None


class InstallationResult(AssetResult):
    """The installation result component."""

    componentType: Literal[ComponentType.INSTALLATION]
    regularity: TimeSeriesFloat  # Regularity is currently set at per installation, send through. Possibly skip in output if confusing


class GeneratorSetResult(EquipmentResultBase):
    """The Generator set result component."""

    componentType: Literal[ComponentType.GENERATOR_SET]
    power_capacity_margin: TimeSeriesRate


class ConsumerSystemResult(EquipmentResultBase):
    componentType: Literal[
        ComponentType.PUMP_SYSTEM,
        ComponentType.COMPRESSOR_SYSTEM,
        ComponentType.CONSUMER_SYSTEM_V2,
    ]

    consumer_type: Literal[ComponentType.COMPRESSOR, ComponentType.PUMP] = None

    @field_validator("consumer_type", mode="before")
    def set_consumer_type_based_on_component_type_if_possible(cls, consumer_type, info: ValidationInfo):
        """
        Set consumer type for legacy system where component type contains the same information.
        """
        component_type = info.data.get("componentType")
        if consumer_type is None:
            if component_type == ComponentType.PUMP_SYSTEM:
                return ComponentType.PUMP
            elif component_type == ComponentType.COMPRESSOR_SYSTEM:
                return ComponentType.COMPRESSOR

        return consumer_type

    operational_settings_used: Optional[TimeSeriesInt] = Field(
        None,
        description="The operational settings used for this system. "
        "0 indicates that no valid operational setting was found.",
    )
    operational_settings_results: Optional[dict[int, list[Any]]] = None


class GenericConsumerResult(EquipmentResultBase):
    componentType: Literal[ComponentType.GENERIC]


class PumpResult(EquipmentResultBase):
    componentType: Literal[ComponentType.PUMP]
    inlet_liquid_rate_m3_per_day: TimeSeriesRate
    inlet_pressure_bar: TimeSeriesFloat
    outlet_pressure_bar: TimeSeriesFloat
    operational_head: TimeSeriesFloat

    streams: Optional[list[TimeSeriesStreamConditions]]  # Optional because only in v2


class CompressorResult(EquipmentResultBase):
    componentType: Literal[ComponentType.COMPRESSOR]
    recirculation_loss: TimeSeriesRate
    rate_exceeds_maximum: TimeSeriesBoolean

    streams: Optional[list[TimeSeriesStreamConditions]]  # Optional because only in v2


class VentingEmitterResult(EquipmentResultBase):
    componentType: Literal[ComponentType.VENTING_EMITTER]


class ConsumerModelResultBase(NodeInfo, CommonResultBase):
    """The Consumer base result component."""

    ...


class PumpModelResult(ConsumerModelResultBase):
    """The Pump result component."""

    componentType: Literal[ComponentType.PUMP]
    inlet_liquid_rate_m3_per_day: Optional[TimeSeriesRate] = None
    inlet_pressure_bar: Optional[TimeSeriesFloat] = None
    outlet_pressure_bar: Optional[TimeSeriesFloat] = None
    operational_head: Optional[TimeSeriesFloat] = None
    is_valid: TimeSeriesBoolean


class TurbineModelResult(TabularTimeSeries):
    energy_usage_unit: Unit
    power_unit: Unit
    efficiency: TimeSeriesFloat
    energy_usage: TimeSeriesRate
    exceeds_maximum_load: TimeSeriesBoolean
    fuel_rate: TimeSeriesRate
    is_valid: TimeSeriesBoolean
    load: TimeSeriesRate
    power: TimeSeriesRate


class CompressorStreamConditionResult(TabularTimeSeries):
    actual_rate_m3_per_hr: TimeSeriesFloat
    actual_rate_before_asv_m3_per_hr: TimeSeriesFloat
    standard_rate_sm3_per_day: TimeSeriesRate
    standard_rate_before_asv_sm3_per_day: TimeSeriesRate
    kappa: TimeSeriesFloat
    density_kg_per_m3: TimeSeriesFloat
    pressure: TimeSeriesFloat
    temperature_kelvin: TimeSeriesFloat
    z: TimeSeriesFloat


class CompressorModelStageResult(TabularTimeSeries):
    chart: Optional[Union[SingleSpeedChartDTO, VariableSpeedChartDTO]]
    chart_area_flags: list[str]
    energy_usage_unit: Unit
    power_unit: Unit
    fluid_composition: dict[str, Optional[float]]

    head_exceeds_maximum: TimeSeriesBoolean
    is_valid: TimeSeriesBoolean
    polytropic_efficiency: TimeSeriesFloat
    polytropic_enthalpy_change_before_choke_kJ_per_kg: TimeSeriesFloat
    polytropic_enthalpy_change_kJ_per_kg: TimeSeriesFloat
    polytropic_head_kJ_per_kg: TimeSeriesFloat
    asv_recirculation_loss_mw: TimeSeriesRate
    energy_usage: TimeSeriesRate
    mass_rate_kg_per_hr: TimeSeriesFloat
    mass_rate_before_asv_kg_per_hr: TimeSeriesFloat
    power: TimeSeriesRate
    pressure_is_choked: TimeSeriesBoolean
    rate_exceeds_maximum: TimeSeriesBoolean
    rate_has_recirculation: TimeSeriesBoolean
    speed: TimeSeriesFloat
    inlet_stream_condition: CompressorStreamConditionResult
    outlet_stream_condition: CompressorStreamConditionResult


class CompressorModelResult(ConsumerModelResultBase):
    componentType: Literal[ComponentType.COMPRESSOR]
    failure_status: list[Optional[CompressorTrainCommonShaftFailureStatus]]
    requested_inlet_pressure: TimeSeriesFloat
    requested_outlet_pressure: TimeSeriesFloat
    rate: TimeSeriesRate
    maximum_rate: TimeSeriesRate
    stage_results: list[CompressorModelStageResult]
    turbine_result: Optional[TurbineModelResult] = None
    inlet_stream_condition: CompressorStreamConditionResult
    outlet_stream_condition: CompressorStreamConditionResult


class GenericModelResult(ConsumerModelResultBase):
    """Generic consumer result component."""

    componentType: Literal[ComponentType.GENERIC]


# Consumer result is referred to as ENERGY_USAGE_MODEL in the input YAML
ConsumerModelResult = Annotated[
    Union[CompressorModelResult, PumpModelResult, GenericModelResult],
    Field(discriminator="componentType"),
]

ComponentResult = Annotated[
    Union[
        AssetResult,
        InstallationResult,
        GeneratorSetResult,
        ConsumerSystemResult,
        CompressorResult,
        PumpResult,
        GenericConsumerResult,
        VentingEmitterResult,
    ],
    Field(discriminator="componentType"),
]


class EcalcModelResult(EcalcResultBaseModel):
    """Result object holding one component for each part of the eCalc model run:

    ModelResult, InstallationResult, GeneratorSetResult, ConsumerSystemResult, ConsumerGroupResult and ConsumerResult
    """

    component_result: ComponentResult
    sub_components: list[ComponentResult]
    models: list[ConsumerModelResult]

    @field_validator("sub_components")
    @classmethod
    def sort_sub_components(cls, sub_components):
        return sorted(sub_components, key=attrgetter("componentType", "name"))

    @field_validator("models")
    @classmethod
    def sort_models(cls, models):
        return sorted(models, key=attrgetter("componentType", "name"))

    @property
    def periods(self):
        return self.component_result.periods

    @property
    def components(self) -> list[ComponentResult]:
        return [self.component_result, *self.sub_components]

    def get_components(self, component_ids: list[str]) -> list[ComponentResult]:
        return [component for component in self.components if component.id in component_ids]

    def get_component_by_name(self, component_name: str) -> Optional[ComponentResult]:
        components = [component for component in self.components if component.name == component_name]
        if not components:
            return None

        if len(components) > 1:
            logger.warning(f"Querying duplicate component {component_name}. Returning first match")

        return components[0]

    def resample(self, freq: Frequency) -> EcalcModelResult:
        return Numbers.format_results_to_precision(
            self.__class__(
                component_result=self.component_result.resample(freq),
                sub_components=[sub_component.resample(freq) for sub_component in self.sub_components],
                models=[model.resample(freq) for model in self.models],
            ),
            precision=6,
        )
