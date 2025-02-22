"""This module defines ``dataclasses.dataclass`` classes that represent the outputs."""

from typing import Dict

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated

from calculator_179d.constants import KBTU_TO_KWH, KBTU_TO_THOUSAND_CUFT
from calculator_179d.data_types import HVACSystemType


class ModelOutputs(BaseModel):
    """The surrogate model outputs."""

    baseline_electricity_kbtu: Annotated[
        float, Field(description="Baseline Electricity Annual Usage", json_schema_extra={"units": "kBtu"})
    ]
    proposed_electricity_kbtu: Annotated[
        float, Field(description="Proposed Electricity Annual Usage", json_schema_extra={"units": "kBtu"})
    ]
    baseline_naturalgas_kbtu: Annotated[
        float, Field(default=0, description="Baseline Natural Gas Annual Usage", json_schema_extra={"units": "kBtu"})
    ]
    proposed_naturalgas_kbtu: Annotated[
        float, Field(default=0, description="Proposed Natural Gas Annual Usage", json_schema_extra={"units": "kBtu"})
    ]

    def to_dict(self) -> Dict[str, float]:
        """Convert to a dictionary."""
        return self.model_dump()


class EnergyOutputs(BaseModel):
    """Energy metrics per sqft and total savings we calculate."""

    proposed_electricity_kbtu_per_sqft: Annotated[
        float, Field(description="Proposed Electricity EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    baseline_electricity_kbtu_per_sqft: Annotated[
        float, Field(description="Baseline Electricity EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    proposed_total_energy_kbtu: Annotated[
        float, Field(description="Proposed Total Energy consumption", json_schema_extra={"units": "kBtu"})
    ]
    proposed_total_energy_kbtu_per_sqft: Annotated[
        float, Field(description="Proposed Total EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    baseline_total_energy_kbtu: Annotated[
        float, Field(description="Proposed Total Energy consumption", json_schema_extra={"units": "kBtu"})
    ]
    baseline_total_energy_kbtu_per_sqft: Annotated[
        float, Field(description="Proposed Total EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    savings_electricity_kbtu: Annotated[
        float, Field(description="Electricity savings", json_schema_extra={"units": "kBtu"})
    ]
    savings_electricity_kbtu_per_sqft: Annotated[
        float, Field(description="Electricty savings per area", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    savings_total_energy_kbtu: Annotated[float, Field(description="Total savings", json_schema_extra={"units": "kBtu"})]
    savings_total_energy_kbtu_per_sqft: Annotated[
        float, Field(description="Total savings per area", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    # Natural gas at end because some models don't have it
    proposed_naturalgas_kbtu_per_sqft: Annotated[
        float, Field(default=0, description="Proposed Natural Gas EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    baseline_naturalgas_kbtu_per_sqft: Annotated[
        float, Field(default=0, description="Baseline Natural Gas EUI", json_schema_extra={"units": "kBtu/ft^2"})
    ]
    savings_naturalgas_kbtu: Annotated[
        float, Field(default=0, description="Natural Gas savings", json_schema_extra={"units": "kBtu"})
    ]
    savings_naturalgas_kbtu_per_sqft: Annotated[
        float, Field(default=0, description="Natural Gas savings per area", json_schema_extra={"units": "kBtu/ft^2"})
    ]

    def to_dict(self) -> Dict[str, float]:
        """Convert to a dictionary."""
        return self.model_dump()

    @staticmethod
    def fromModelOutputs(model_outputs: ModelOutputs, gross_floor_area_ft2: float):
        proposed_electricity_kbtu_per_sqft = model_outputs.proposed_electricity_kbtu / gross_floor_area_ft2
        baseline_electricity_kbtu_per_sqft = model_outputs.baseline_electricity_kbtu / gross_floor_area_ft2
        proposed_naturalgas_kbtu_per_sqft = model_outputs.proposed_naturalgas_kbtu / gross_floor_area_ft2
        baseline_naturalgas_kbtu_per_sqft = model_outputs.baseline_naturalgas_kbtu / gross_floor_area_ft2

        # Calculate total energy
        # electricity +  natural gas consumption
        proposed_total_energy_kbtu = model_outputs.proposed_electricity_kbtu + model_outputs.proposed_naturalgas_kbtu
        proposed_total_energy_kbtu_per_sqft = proposed_total_energy_kbtu / gross_floor_area_ft2
        baseline_total_energy_kbtu = model_outputs.baseline_electricity_kbtu + model_outputs.baseline_naturalgas_kbtu
        baseline_total_energy_kbtu_per_sqft = baseline_total_energy_kbtu / gross_floor_area_ft2

        # Calculate energy savings
        savings_electricity_kbtu = max(
            model_outputs.baseline_electricity_kbtu - model_outputs.proposed_electricity_kbtu, 0
        )
        savings_electricity_kbtu_per_sqft = savings_electricity_kbtu / gross_floor_area_ft2
        savings_naturalgas_kbtu = max(
            model_outputs.baseline_naturalgas_kbtu - model_outputs.proposed_naturalgas_kbtu, 0
        )
        savings_naturalgas_kbtu_per_sqft = savings_naturalgas_kbtu / gross_floor_area_ft2
        savings_total_energy_kbtu = max(baseline_total_energy_kbtu - proposed_total_energy_kbtu, 0)
        savings_total_energy_kbtu_per_sqft = savings_total_energy_kbtu / gross_floor_area_ft2

        return EnergyOutputs(
            proposed_electricity_kbtu_per_sqft=proposed_electricity_kbtu_per_sqft,
            baseline_electricity_kbtu_per_sqft=baseline_electricity_kbtu_per_sqft,
            proposed_naturalgas_kbtu_per_sqft=proposed_naturalgas_kbtu_per_sqft,
            baseline_naturalgas_kbtu_per_sqft=baseline_naturalgas_kbtu_per_sqft,
            proposed_total_energy_kbtu=proposed_total_energy_kbtu,
            proposed_total_energy_kbtu_per_sqft=proposed_total_energy_kbtu_per_sqft,
            baseline_total_energy_kbtu=baseline_total_energy_kbtu,
            baseline_total_energy_kbtu_per_sqft=baseline_total_energy_kbtu_per_sqft,
            savings_electricity_kbtu=savings_electricity_kbtu,
            savings_electricity_kbtu_per_sqft=savings_electricity_kbtu_per_sqft,
            savings_naturalgas_kbtu=savings_naturalgas_kbtu,
            savings_naturalgas_kbtu_per_sqft=savings_naturalgas_kbtu_per_sqft,
            savings_total_energy_kbtu=savings_total_energy_kbtu,
            savings_total_energy_kbtu_per_sqft=savings_total_energy_kbtu_per_sqft,
        )


class CostOutputs(BaseModel):
    """Economic metrics we calculate."""

    proposed_electricity_usd: Annotated[
        float, Field(default=0, description="Proposed Electricity cost", json_schema_extra={"units": "USD"})
    ]
    baseline_electricity_usd: Annotated[
        float, Field(default=0, description="Baseline Electricity cost", json_schema_extra={"units": "USD"})
    ]
    proposed_electricity_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Proposed Electricity cost per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    baseline_electricity_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Baseline Electricity cost per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    proposed_naturalgas_usd: Annotated[
        float, Field(default=0, description="Proposed Natural Gas cost", json_schema_extra={"units": "USD"})
    ]
    baseline_naturalgas_usd: Annotated[
        float, Field(default=0, description="Baseline Natural Gas cost", json_schema_extra={"units": "USD"})
    ]
    proposed_naturalgas_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Proposed Natural Gas cost per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    baseline_naturalgas_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Baseline Natural Gas cost per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    proposed_total_usd: Annotated[
        float, Field(default=0, description="Proposed Total cost", json_schema_extra={"units": "USD"})
    ]
    proposed_total_usd_per_sqft: Annotated[
        float, Field(default=0, description="Proposed Total cost per area", json_schema_extra={"units": "USD/ft^2"})
    ]
    baseline_total_usd: Annotated[
        float, Field(default=0, description="Baseline Total cost", json_schema_extra={"units": "USD"})
    ]
    baseline_total_usd_per_sqft: Annotated[
        float, Field(default=0, description="Baseline Total cost per area", json_schema_extra={"units": "USD/ft^2"})
    ]
    savings_electricity_usd: Annotated[
        float, Field(default=0, description="Electricity cost savings", json_schema_extra={"units": "USD"})
    ]
    savings_electricity_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Electricity cost savings per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    savings_naturalgas_usd: Annotated[
        float, Field(default=0, description="Natural Gas cost savings", json_schema_extra={"units": "USD"})
    ]
    savings_naturalgas_usd_per_sqft: Annotated[
        float,
        Field(default=0, description="Natural Gas cost savings per area", json_schema_extra={"units": "USD/ft^2"}),
    ]
    savings_total_usd: Annotated[
        float, Field(default=0, description="Total cost savings", json_schema_extra={"units": "USD"})
    ]
    savings_total_usd_per_sqft: Annotated[
        float, Field(default=0, description="Total cost savings per area", json_schema_extra={"units": "USD/ft^2"})
    ]
    savings_electricity_cost_percent: Annotated[
        float, Field(default=0, description="Electricity cost savings", json_schema_extra={"units": "%"})
    ]
    savings_naturalgas_cost_percent: Annotated[
        float, Field(default=0, description="Natural Gas cost savings", json_schema_extra={"units": "%"})
    ]
    savings_total_cost_percent: float = 0  #: Actual Total cost savings in % calculated by the model, but kept > 0
    savings_total_cost_percent_total_per_sqft: float = 0
    savings_total_cost_percent_actual: float = 0  #: Actual Total cost savings in % calculated by the model

    def to_dict(self) -> Dict[str, float]:
        """Convert to a dictionary."""
        return self.model_dump()

    @staticmethod
    def fromModelOutputs(
        model_outputs: ModelOutputs,
        gross_floor_area_ft2: float,
        hvac_system_type: HVACSystemType,
        electricity_rate_usd_per_kwh: float,
        naturalgas_rate_usd_per_therm: float,
    ):
        # calculate costs
        # baseline costs
        baseline_electricity_usd = electricity_rate_usd_per_kwh * model_outputs.baseline_electricity_kbtu * KBTU_TO_KWH
        baseline_electricity_usd_per_sqft = baseline_electricity_usd / gross_floor_area_ft2

        baseline_naturalgas_usd = (
            naturalgas_rate_usd_per_therm * model_outputs.baseline_naturalgas_kbtu * KBTU_TO_THOUSAND_CUFT
        )
        baseline_naturalgas_usd_per_sqft = baseline_naturalgas_usd / gross_floor_area_ft2

        baseline_total_usd = baseline_electricity_usd + baseline_naturalgas_usd
        baseline_total_usd_per_sqft = baseline_total_usd / gross_floor_area_ft2

        # proposed costs
        proposed_electricity_usd = electricity_rate_usd_per_kwh * model_outputs.proposed_electricity_kbtu * KBTU_TO_KWH
        proposed_electricity_usd_per_sqft = proposed_electricity_usd / gross_floor_area_ft2

        proposed_naturalgas_usd = (
            naturalgas_rate_usd_per_therm * model_outputs.proposed_naturalgas_kbtu * KBTU_TO_THOUSAND_CUFT
        )
        proposed_naturalgas_usd_per_sqft = proposed_naturalgas_usd / gross_floor_area_ft2
        proposed_total_usd = proposed_electricity_usd + proposed_naturalgas_usd
        proposed_total_usd_per_sqft = proposed_total_usd / gross_floor_area_ft2

        # calculate cost savings
        savings_electricity_usd = max(baseline_electricity_usd - proposed_electricity_usd, 0)
        savings_electricity_usd_per_sqft = savings_electricity_usd / gross_floor_area_ft2
        savings_naturalgas_usd = max(baseline_naturalgas_usd - proposed_naturalgas_usd, 0)
        savings_naturalgas_usd_per_sqft = savings_naturalgas_usd / gross_floor_area_ft2
        savings_total_usd = max(baseline_total_usd - proposed_total_usd, 0)
        savings_total_usd_per_sqft = savings_total_usd / gross_floor_area_ft2

        # Cost savings percentage
        # TODO: why is this rounding?
        savings_total_cost_percent_Actual = round(
            ((baseline_total_usd - proposed_total_usd) / baseline_total_usd) * 100
        )
        savings_total_cost_percent = max(savings_total_cost_percent_Actual, 0)
        savings_electricity_cost_percent = max(
            round(((baseline_electricity_usd - proposed_electricity_usd) / baseline_electricity_usd) * 100),
            0,
        )

        savings_naturalgas_cost_percent = 0
        if hvac_system_type.is_gas:
            savings_naturalgas_cost_percent = max(
                round(((baseline_naturalgas_usd - proposed_naturalgas_usd) / baseline_naturalgas_usd) * 100),
                0,
            )
        savings_total_cost_percent_per_sqft = savings_total_cost_percent / gross_floor_area_ft2

        return CostOutputs(
            proposed_electricity_usd=proposed_electricity_usd,
            baseline_electricity_usd=baseline_electricity_usd,
            proposed_electricity_usd_per_sqft=proposed_electricity_usd_per_sqft,
            baseline_electricity_usd_per_sqft=baseline_electricity_usd_per_sqft,
            proposed_naturalgas_usd=proposed_naturalgas_usd,
            baseline_naturalgas_usd=baseline_naturalgas_usd,
            proposed_naturalgas_usd_per_sqft=proposed_naturalgas_usd_per_sqft,
            baseline_naturalgas_usd_per_sqft=baseline_naturalgas_usd_per_sqft,
            proposed_total_usd=proposed_total_usd,
            proposed_total_usd_per_sqft=proposed_total_usd_per_sqft,
            baseline_total_usd=baseline_total_usd,
            baseline_total_usd_per_sqft=baseline_total_usd_per_sqft,
            savings_electricity_usd=savings_electricity_usd,
            savings_electricity_usd_per_sqft=savings_electricity_usd_per_sqft,
            savings_naturalgas_usd=savings_naturalgas_usd,
            savings_naturalgas_usd_per_sqft=savings_naturalgas_usd_per_sqft,
            savings_total_usd=savings_total_usd,
            savings_total_usd_per_sqft=savings_total_usd_per_sqft,
            savings_electricity_cost_percent=savings_electricity_cost_percent,
            savings_naturalgas_cost_percent=savings_naturalgas_cost_percent,
            savings_total_cost_percent=savings_total_cost_percent,
            savings_total_cost_percent_total_per_sqft=savings_total_cost_percent_per_sqft,
            savings_total_cost_percent_actual=savings_total_cost_percent_Actual,
        )


class CalculatorOutputs(BaseModel):
    """Whole calculator outputs."""

    model_outputs: ModelOutputs
    energy_outputs: EnergyOutputs
    cost_outputs: CostOutputs
    tax_deduction_rate_energy: float = 0
    tax_deduction_rate_all: float = 0

    def to_dict(self) -> Dict[str, float]:
        """Convert to a flattened dictionary, similar to the former json payload."""
        return {
            **self.model_outputs.to_dict(),
            **self.energy_outputs.to_dict(),
            **self.cost_outputs.to_dict(),
            **{
                "tax_deduction_rate_energy": self.tax_deduction_rate_energy,
                "tax_deduction_rate_all": self.tax_deduction_rate_all,
            },
        }
