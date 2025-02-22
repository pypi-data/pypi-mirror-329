"""The main calculator for 179D.

The primary entry point is :meth:`calculate_savings`
"""

import json
import sys
from pathlib import Path

import numpy as np

from calculator_179d.constants import CENTS_TO_DOLLARS, M2_TO_FT2
from calculator_179d.data_types import FuelType, ModelType, PropertyInfo
from calculator_179d.output_data_types import CalculatorOutputs, CostOutputs, EnergyOutputs, ModelOutputs
from calculator_179d.surrogate_model import SurrogateModel


# 4 prediction models used to compute proposed electricity and naturalgas
# and baseline electricity and naturalgas
# prediction model outputs are in GJ, function converts outputs to kBTU
def calculate_model_outputs(property_info: PropertyInfo) -> ModelOutputs:
    """Calculate the energy consumption from the surrogate model."""

    # proposed and baseline electricity 179d
    # create proposed electricity model object based on bulding type, climate zone, and system type
    proposed_electricity_179d_obj = SurrogateModel(
        model_type=ModelType.PROPOSED, fuel_type=FuelType.ELECTRICITY, property_info=property_info
    )
    # estimate annual electricity using proposed model, and user calculator inputs
    proposed_electricity_kbtu = proposed_electricity_179d_obj.estimate_annual_kbtu()
    # create baseline model object based on bulding type, climate zone, and system type
    baseline_electricity_179d_obj = SurrogateModel(
        model_type=ModelType.BASELINE, fuel_type=FuelType.ELECTRICITY, property_info=property_info
    )
    # estimate baseline annual electricity withe baseline model and user calculator inputs
    baseline_electricity_kbtu = baseline_electricity_179d_obj.estimate_annual_kbtu()

    # no natural gas models for hvac systems with heat pump or have electric coil
    if not property_info.hvac_system.is_gas:
        return ModelOutputs(
            baseline_electricity_kbtu=baseline_electricity_kbtu,
            proposed_electricity_kbtu=proposed_electricity_kbtu,
        )

    # Calculate Gas
    proposed_naturalgas_179d_obj = SurrogateModel(
        model_type=ModelType.PROPOSED, fuel_type=FuelType.NATURALGAS, property_info=property_info
    )
    proposed_naturalgas_kbtu = proposed_naturalgas_179d_obj.estimate_annual_kbtu()
    baseline_naturalgas_179d_obj = SurrogateModel(
        model_type=ModelType.BASELINE, fuel_type=FuelType.NATURALGAS, property_info=property_info
    )
    baseline_naturalgas_kbtu = baseline_naturalgas_179d_obj.estimate_annual_kbtu()

    return ModelOutputs(
        baseline_electricity_kbtu=baseline_electricity_kbtu,
        baseline_naturalgas_kbtu=baseline_naturalgas_kbtu,
        proposed_electricity_kbtu=proposed_electricity_kbtu,
        proposed_naturalgas_kbtu=proposed_naturalgas_kbtu,
    )


def calculate_savings(property_info: PropertyInfo) -> CalculatorOutputs:
    """This is the main entry point for the calculator."""

    gross_floor_area_ft2 = property_info.gross_floor_area_m2 * M2_TO_FT2

    # calculate model outputs
    model_outputs = calculate_model_outputs(property_info=property_info)

    # calculate energy and energy savings
    energy_outputs = EnergyOutputs.fromModelOutputs(
        model_outputs=model_outputs, gross_floor_area_ft2=gross_floor_area_ft2
    )

    # calculate cost and cost savings
    cost_outputs = CostOutputs.fromModelOutputs(
        model_outputs=model_outputs,
        gross_floor_area_ft2=gross_floor_area_ft2,
        hvac_system_type=property_info.hvac_system,
        electricity_rate_usd_per_kwh=property_info.electricity_rate_cents_per_kwh * CENTS_TO_DOLLARS,
        naturalgas_rate_usd_per_therm=property_info.natural_gas_rate_usd_per_therm,
    )

    if cost_outputs.savings_total_cost_percent >= property_info.min_threshold_energy * 100:
        tax_deduction_rate_energy = (
            property_info.energy_tax_deduction_rate_min
            + (cost_outputs.savings_total_cost_percent - property_info.min_threshold_energy * 100)
            * property_info.increment_energy
        )
        if tax_deduction_rate_energy > property_info.energy_tax_deduction_rate_max:
            tax_deduction_rate_energy = property_info.energy_tax_deduction_rate_max
    else:
        print("Minimum savings requirement not met and not qualified for 179D tax deduction")
        tax_deduction_rate_energy = 0

    if cost_outputs.savings_total_cost_percent >= property_info.min_threshold_all_179d * 100:
        tax_deduction_rate_all = (
            property_info.all_179d_tax_deduction_rate_min
            + (cost_outputs.savings_total_cost_percent - property_info.min_threshold_all_179d * 100)
            * property_info.increment_all_179d
        )
        if tax_deduction_rate_all > property_info.all_179d_tax_deduction_rate_max:
            tax_deduction_rate_all = property_info.all_179d_tax_deduction_rate_max
    else:
        print("Minimum savings requirement not met and not qualified for 179D tax deduction")
        tax_deduction_rate_all = 0

    return CalculatorOutputs(
        model_outputs=model_outputs,
        energy_outputs=energy_outputs,
        cost_outputs=cost_outputs,
        tax_deduction_rate_all=tax_deduction_rate_all,
        tax_deduction_rate_energy=tax_deduction_rate_energy,
    )


if __name__ == "__main__":
    json_file = Path(sys.argv[1])
    assert json_file.is_file()
    property_info = PropertyInfo.from_json(json_file.read_text())
    # compute outputs and save in calculator_outputs.json
    results = calculate_savings(property_info)
    Path('output_files/calculator_outputs.json').write_text(json.dumps(results.to_dict(), indent=2))
