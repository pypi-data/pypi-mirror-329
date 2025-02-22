import re
from typing import Optional

import pytest

from calculator_179d.constants import KBTU_TO_KWH, KBTU_TO_THOUSAND_CUFT
from calculator_179d.data_types import HVACSystemType
from calculator_179d.output_data_types import CalculatorOutputs, CostOutputs, EnergyOutputs, ModelOutputs


def test_model_outputs():
    ModelOutputs(
        baseline_electricity_kbtu=100,
        proposed_electricity_kbtu=87,
        baseline_naturalgas_kbtu=200,
        proposed_naturalgas_kbtu=178,
    )

    model_outputs = ModelOutputs(baseline_electricity_kbtu=100, proposed_electricity_kbtu=87)
    assert model_outputs.baseline_naturalgas_kbtu == 0
    assert model_outputs.proposed_naturalgas_kbtu == 0


@pytest.mark.parametrize("field_name", ModelOutputs.model_fields.keys())
def test_model_outputs_validation_wrong_type(field_name: str):
    minimal_dict = {'baseline_electricity_kbtu': 100.0, 'proposed_electricity_kbtu': 87.0}
    minimal_dict.update({field_name: None})  # type: ignore

    with pytest.raises(ValueError, match=re.compile(f"{field_name}.*Input should be a valid number", re.DOTALL)):
        ModelOutputs(**minimal_dict)


def test_model_outputs_validation_field_missing():
    with pytest.raises(ValueError, match="Field required"):
        ModelOutputs(
            proposed_electricity_kbtu=100,
        )
    with pytest.raises(ValueError, match="Field required"):
        ModelOutputs(
            baseline_electricity_kbtu=100,
        )


def test_energy_outputs_from_model_outputs_elec_only():
    baseline_electricity_kbtu = 100.0
    proposed_electricity_kbtu = 87.0
    gross_floor_area_ft2 = 100.0
    model_outputs = ModelOutputs(
        baseline_electricity_kbtu=baseline_electricity_kbtu,
        proposed_electricity_kbtu=proposed_electricity_kbtu,
    )
    energy_outputs = EnergyOutputs.fromModelOutputs(
        model_outputs=model_outputs, gross_floor_area_ft2=gross_floor_area_ft2
    )

    assert energy_outputs.proposed_electricity_kbtu_per_sqft == 0.87
    assert energy_outputs.proposed_total_energy_kbtu == 87.0
    assert energy_outputs.proposed_total_energy_kbtu_per_sqft == 0.87

    assert energy_outputs.baseline_electricity_kbtu_per_sqft == 1.0
    assert energy_outputs.baseline_total_energy_kbtu == 100.0
    assert energy_outputs.baseline_total_energy_kbtu_per_sqft == 1.0

    assert energy_outputs.savings_electricity_kbtu == 13.0
    assert energy_outputs.savings_electricity_kbtu_per_sqft == 0.13
    assert energy_outputs.savings_total_energy_kbtu == 13.0
    assert energy_outputs.savings_total_energy_kbtu_per_sqft == 0.13

    assert energy_outputs.proposed_naturalgas_kbtu_per_sqft == 0.0
    assert energy_outputs.baseline_naturalgas_kbtu_per_sqft == 0.0
    assert energy_outputs.savings_naturalgas_kbtu == 0.0
    assert energy_outputs.savings_naturalgas_kbtu_per_sqft == 0.0


def test_energy_outputs_from_model_outputs_both():
    baseline_electricity_kbtu = 100.0
    baseline_naturalgas_kbtu = 200.0

    proposed_electricity_kbtu = 90.0
    proposed_naturalgas_kbtu = 170.0

    gross_floor_area_ft2 = 100.0
    model_outputs = ModelOutputs(
        baseline_electricity_kbtu=baseline_electricity_kbtu,
        proposed_electricity_kbtu=proposed_electricity_kbtu,
        baseline_naturalgas_kbtu=baseline_naturalgas_kbtu,
        proposed_naturalgas_kbtu=proposed_naturalgas_kbtu,
    )
    energy_outputs = EnergyOutputs.fromModelOutputs(
        model_outputs=model_outputs, gross_floor_area_ft2=gross_floor_area_ft2
    )

    assert energy_outputs.proposed_total_energy_kbtu == 260.0
    assert energy_outputs.proposed_total_energy_kbtu == proposed_electricity_kbtu + proposed_naturalgas_kbtu

    assert energy_outputs.proposed_electricity_kbtu_per_sqft == 0.9
    assert energy_outputs.proposed_naturalgas_kbtu_per_sqft == 1.7
    assert energy_outputs.proposed_total_energy_kbtu_per_sqft == 2.6

    assert energy_outputs.baseline_total_energy_kbtu == 300.0
    assert energy_outputs.baseline_total_energy_kbtu == baseline_electricity_kbtu + baseline_naturalgas_kbtu

    assert energy_outputs.baseline_total_energy_kbtu_per_sqft == 3.0
    assert energy_outputs.baseline_naturalgas_kbtu_per_sqft == 2.0
    assert energy_outputs.baseline_electricity_kbtu_per_sqft == 1.0

    assert energy_outputs.savings_electricity_kbtu == 10.0
    assert energy_outputs.savings_electricity_kbtu == baseline_electricity_kbtu - proposed_electricity_kbtu
    assert energy_outputs.savings_electricity_kbtu_per_sqft == 0.1

    assert energy_outputs.savings_naturalgas_kbtu == 30.0
    assert energy_outputs.savings_naturalgas_kbtu == baseline_naturalgas_kbtu - proposed_naturalgas_kbtu
    assert energy_outputs.savings_naturalgas_kbtu_per_sqft == 0.3

    assert energy_outputs.savings_total_energy_kbtu == 40.0
    assert energy_outputs.savings_total_energy_kbtu_per_sqft == 0.4


def test_cost_outputs_from_model_outputs_elec_only():
    baseline_electricity_kwh = 1000.0
    baseline_electricity_kbtu = baseline_electricity_kwh / KBTU_TO_KWH

    proposed_electricity_kwh = 900.0
    proposed_electricity_kbtu = proposed_electricity_kwh / KBTU_TO_KWH

    gross_floor_area_ft2 = 100.0
    electricity_rate_usd_per_kwh = 0.2
    naturalgas_rate_usd_per_therm = 1.1

    baseline_electricity_cost = baseline_electricity_kwh * electricity_rate_usd_per_kwh
    assert baseline_electricity_cost == pytest.approx(200.0)
    proposed_electricity_cost = proposed_electricity_kwh * electricity_rate_usd_per_kwh
    assert proposed_electricity_cost == pytest.approx(180.0)

    model_outputs = ModelOutputs(
        baseline_electricity_kbtu=baseline_electricity_kbtu,
        proposed_electricity_kbtu=proposed_electricity_kbtu,
    )
    cost_outputs = CostOutputs.fromModelOutputs(
        model_outputs=model_outputs,
        gross_floor_area_ft2=gross_floor_area_ft2,
        hvac_system_type=HVACSystemType.PSZ_AC_WITH_ELECTRIC_COIL,
        electricity_rate_usd_per_kwh=electricity_rate_usd_per_kwh,
        naturalgas_rate_usd_per_therm=naturalgas_rate_usd_per_therm,
    )

    # Baseline
    assert cost_outputs.baseline_electricity_usd == pytest.approx(200.0)
    assert cost_outputs.baseline_electricity_usd == pytest.approx(baseline_electricity_cost)
    assert cost_outputs.baseline_electricity_usd_per_sqft == pytest.approx(2.0)

    assert cost_outputs.baseline_naturalgas_usd == pytest.approx(0.0)
    assert cost_outputs.baseline_naturalgas_usd_per_sqft == pytest.approx(0.0)

    assert cost_outputs.baseline_total_usd == pytest.approx(200.0)
    assert cost_outputs.baseline_total_usd == pytest.approx(baseline_electricity_cost)
    assert cost_outputs.baseline_total_usd_per_sqft == pytest.approx(2.0)

    # Proposed
    assert cost_outputs.proposed_electricity_usd == pytest.approx(180.0)
    assert cost_outputs.proposed_electricity_usd == pytest.approx(proposed_electricity_cost)
    assert cost_outputs.proposed_electricity_usd_per_sqft == pytest.approx(1.8)

    assert cost_outputs.proposed_naturalgas_usd == pytest.approx(0.0)
    assert cost_outputs.proposed_naturalgas_usd_per_sqft == pytest.approx(0.0)

    assert cost_outputs.proposed_total_usd == pytest.approx(180.0)
    assert cost_outputs.proposed_total_usd == pytest.approx(proposed_electricity_cost)
    assert cost_outputs.proposed_total_usd_per_sqft == pytest.approx(1.8)

    # Savings
    assert cost_outputs.savings_electricity_usd == pytest.approx(20.0)
    assert cost_outputs.savings_electricity_usd == pytest.approx(baseline_electricity_cost - proposed_electricity_cost)
    assert cost_outputs.savings_electricity_usd_per_sqft == pytest.approx(0.2)

    assert cost_outputs.savings_total_usd == pytest.approx(20.0)
    assert cost_outputs.savings_total_usd_per_sqft == pytest.approx(0.2)
    assert cost_outputs.savings_electricity_cost_percent == pytest.approx(10.0)
    assert cost_outputs.savings_total_cost_percent == pytest.approx(10.0)
    assert cost_outputs.savings_total_cost_percent_total_per_sqft == pytest.approx(0.1)
    assert cost_outputs.savings_total_cost_percent_actual == pytest.approx(10.0)

    assert cost_outputs.savings_naturalgas_usd == pytest.approx(0.0)
    assert cost_outputs.savings_naturalgas_usd_per_sqft == pytest.approx(0.0)
    assert cost_outputs.savings_naturalgas_cost_percent == pytest.approx(0.0)


def test_cost_outputs_from_model_outputs_both():
    baseline_electricity_kwh = 1000.0
    baseline_electricity_kbtu = baseline_electricity_kwh / KBTU_TO_KWH

    baseline_naturalgas_therms = 500.0
    baseline_naturalgas_kbtu = baseline_naturalgas_therms / KBTU_TO_THOUSAND_CUFT

    proposed_electricity_kwh = 900.0
    proposed_electricity_kbtu = proposed_electricity_kwh / KBTU_TO_KWH

    proposed_naturalgas_therms = 400.0
    proposed_naturalgas_kbtu = proposed_naturalgas_therms / KBTU_TO_THOUSAND_CUFT

    gross_floor_area_ft2 = 100.0
    electricity_rate_usd_per_kwh = 0.2
    naturalgas_rate_usd_per_therm = 2.0

    baseline_electricity_cost = baseline_electricity_kwh * electricity_rate_usd_per_kwh
    assert baseline_electricity_cost == pytest.approx(200.0)
    proposed_electricity_cost = proposed_electricity_kwh * electricity_rate_usd_per_kwh
    assert proposed_electricity_cost == pytest.approx(180.0)

    baseline_naturalgas_cost = baseline_naturalgas_therms * naturalgas_rate_usd_per_therm
    assert baseline_naturalgas_cost == pytest.approx(1000.0)
    proposed_naturalgas_cost = proposed_naturalgas_therms * naturalgas_rate_usd_per_therm
    assert proposed_naturalgas_cost == pytest.approx(800.0)

    model_outputs = ModelOutputs(
        baseline_electricity_kbtu=baseline_electricity_kbtu,
        proposed_electricity_kbtu=proposed_electricity_kbtu,
        baseline_naturalgas_kbtu=baseline_naturalgas_kbtu,
        proposed_naturalgas_kbtu=proposed_naturalgas_kbtu,
    )
    cost_outputs = CostOutputs.fromModelOutputs(
        model_outputs=model_outputs,
        gross_floor_area_ft2=gross_floor_area_ft2,
        hvac_system_type=HVACSystemType.PSZ_AC_WITH_GAS_COIL,
        electricity_rate_usd_per_kwh=electricity_rate_usd_per_kwh,
        naturalgas_rate_usd_per_therm=naturalgas_rate_usd_per_therm,
    )

    # Baseline
    assert cost_outputs.baseline_electricity_usd == pytest.approx(200.0)
    assert cost_outputs.baseline_electricity_usd == pytest.approx(baseline_electricity_cost)
    assert cost_outputs.baseline_electricity_usd_per_sqft == pytest.approx(2.0)

    assert cost_outputs.baseline_naturalgas_usd == pytest.approx(1000.0)
    assert cost_outputs.baseline_naturalgas_usd == pytest.approx(baseline_naturalgas_cost)
    assert cost_outputs.baseline_naturalgas_usd_per_sqft == pytest.approx(10.0)

    assert cost_outputs.baseline_total_usd == pytest.approx(1200.0)
    assert cost_outputs.baseline_total_usd == pytest.approx(baseline_electricity_cost + baseline_naturalgas_cost)
    assert cost_outputs.baseline_total_usd_per_sqft == pytest.approx(12.0)

    # Proposed
    assert cost_outputs.proposed_electricity_usd == pytest.approx(180.0)
    assert cost_outputs.proposed_electricity_usd == pytest.approx(proposed_electricity_cost)
    assert cost_outputs.proposed_electricity_usd_per_sqft == pytest.approx(1.8)

    assert cost_outputs.proposed_naturalgas_usd == pytest.approx(800.0)
    assert cost_outputs.proposed_naturalgas_usd == pytest.approx(proposed_naturalgas_cost)
    assert cost_outputs.proposed_naturalgas_usd_per_sqft == pytest.approx(8.0)

    assert cost_outputs.proposed_total_usd == pytest.approx(980.0)
    assert cost_outputs.proposed_total_usd == pytest.approx(proposed_electricity_cost + proposed_naturalgas_cost)
    assert cost_outputs.proposed_total_usd_per_sqft == pytest.approx(9.8)

    # Savings
    assert cost_outputs.savings_electricity_usd == pytest.approx(20.0)
    assert cost_outputs.savings_electricity_usd == pytest.approx(baseline_electricity_cost - proposed_electricity_cost)
    assert cost_outputs.savings_electricity_usd_per_sqft == pytest.approx(0.2)
    assert cost_outputs.savings_electricity_cost_percent == pytest.approx(10.0)

    assert cost_outputs.savings_naturalgas_usd == pytest.approx(200.0)
    assert cost_outputs.savings_naturalgas_usd == pytest.approx(baseline_naturalgas_cost - proposed_naturalgas_cost)
    assert cost_outputs.savings_naturalgas_usd_per_sqft == pytest.approx(2.0)
    assert cost_outputs.savings_naturalgas_cost_percent == pytest.approx(20.0)

    assert cost_outputs.savings_total_usd == pytest.approx(220.0)
    assert cost_outputs.savings_total_usd == pytest.approx(
        baseline_electricity_cost + baseline_naturalgas_cost - proposed_electricity_cost - proposed_naturalgas_cost
    )
    assert cost_outputs.savings_total_usd_per_sqft == pytest.approx(2.2)

    assert cost_outputs.savings_total_cost_percent == pytest.approx(18.0)
    assert cost_outputs.savings_total_cost_percent == pytest.approx(round(100.0 * 220.0 / 1200.0))
    assert cost_outputs.savings_total_cost_percent_total_per_sqft == pytest.approx(0.18)
    assert cost_outputs.savings_total_cost_percent_actual == pytest.approx(18.0)
