#!/usr/bin/env python
"""Tests for `calculator179`."""
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import pytest
from strenum import StrEnum

from calculator_179d.constants import FT2_TO_M2, U_VALUE_IP_TO_SI
from calculator_179d.data_types import BuildingType, ClimateZone, HVACSystemType, PropertyInfo
from calculator_179d.main_calculator import calculate_savings
from calculator_179d.output_data_types import CalculatorOutputs

TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / 'test_data'
TEST_RESULTS_PATH = TEST_DIR / 'test_results.json'

DEFAULT_ECONOMICS = {
    "electricity_rate_cents_per_kwh": 11.58,
    "natural_gas_rate_usd_per_therm": 11.38,
    "energy_tax_deduction_rate_min": 0.5,
    "energy_tax_deduction_rate_max": 1,
    "all_179d_tax_deduction_rate_min": 2.5,
    "all_179d_tax_deduction_rate_max": 5,
    "increment_energy": 0.02,
    "min_threshold_energy": 0.25,
    "increment_all_179d": 0.1,
    "min_threshold_all_179d": 0.25,
}

N_DECIMALS = 3


class BuildingSize(StrEnum):
    SMALL = "small"
    LARGE = "large"

    @property
    def square_feet(self):
        return 1000.0 if self == BuildingSize.SMALL else 24999.0

    @property
    def square_meter(self):
        return self.square_feet * FT2_TO_M2

    def generate_number_of_floors(self) -> List[int]:
        if self.SMALL:
            return [1]
        else:
            return [1, 3]


class SHWType(StrEnum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"


# for casetype = min savings should be less than min savings limit = -100.
# for casetype = max savings should be less than max savings limit = 150
class CaseType(StrEnum):
    MIN = "min"
    MAX = "max"

    def savings_percent_limit(self, savings_percent):
        if self == self.MIN and savings_percent > -100 and savings_percent < 25:
            return True
        elif self == self.MAX and savings_percent < 150:
            return True
        else:
            return False


def _read_envelope_lookup() -> Dict[Tuple[ClimateZone, CaseType], Dict[str, float]]:
    """Returns a dict with values expected for envelope.

    eg: ```
    {
        (ClimateZone.CZ_1A, CaseType.MAX) : {
          'roof_u_value_w_per_m2_k': 0.11356,
          'wall_u_value_w_per_m2_k': 0.18926666666666667,
          'window_wall_ratio': 0.01,
          'window_u_factor_w_per_m2_k': 1.1356
        }
    }
    ```
    """
    result = {}

    df = pd.read_csv(
        TEST_DATA_DIR / 'envelope.csv',
        index_col=[0, 1],
    )
    for (cz_str, case_type_str), row in df.iterrows():  # type: ignore[misc]
        row['roof_r_value_ip']
        converted = {
            'roof_u_value_w_per_m2_k': U_VALUE_IP_TO_SI * 1 / row['roof_r_value_ip'],
            'wall_u_value_w_per_m2_k': U_VALUE_IP_TO_SI * 1 / row['wall_r_value_ip'],
            'window_wall_ratio': row['window_to_wall_ratio'],
            'window_u_factor_w_per_m2_k': U_VALUE_IP_TO_SI * row['window_u_value_ip'],
            'window_shgc': row['shgc'],
        }
        result[(ClimateZone(cz_str), CaseType(case_type_str.lower()))] = converted

    return result


def _read_lpd_lookup() -> Dict[Tuple[BuildingType, CaseType], float]:
    """Returns a dict with values expected for lpd in watts per m2.

    eg: ```
    {
        (BuildingType.SMALL_OFFICE, CaseType.MAX) : 4.52,
    }
    ```
    """

    result = {}

    df = pd.read_csv(
        TEST_DATA_DIR / 'lpd.csv',
        index_col=[0, 1],
    )
    for (bt_str, case_type_str), row in df.iterrows():  # type: ignore[misc]
        result[(BuildingType(bt_str), CaseType(case_type_str.lower()))] = row['lpd_w_per_ft2'] / FT2_TO_M2

    return result


def _read_shw_lookup() -> Dict[Tuple[BuildingType, SHWType, CaseType], Dict[str, float]]:
    result = {}

    df = pd.read_csv(
        TEST_DATA_DIR / 'shw.csv',
        index_col=[0, 1, 2],
    )
    for (bt_str, shw_str, case_type_str), row in df.iterrows():  # type: ignore[misc]
        result[(BuildingType(bt_str), SHWType(shw_str.lower()), CaseType(case_type_str.lower()))] = {
            str(k): float(v) for k, v in row.items() if not pd.isna(v)
        }

    return result


def _read_hvac_lookup() -> Dict[Tuple[BuildingType, HVACSystemType, CaseType], Dict[str, float]]:
    result = {}

    df = pd.read_csv(
        TEST_DATA_DIR / 'hvac.csv',
        index_col=[0, 1, 2],
    )
    for (bt_str, hvac_str, case_type_str), row in df.iterrows():  # type: ignore[misc]
        d = {typing.cast(str, k): float(v) for k, v in row.items() if not pd.isna(v)}
        if 'ERV' in d:
            d.pop('ERV')  # TODO
        result[(BuildingType(bt_str), HVACSystemType(hvac_str), CaseType(case_type_str.lower()))] = d

    return result


ENVELOPE_LOOKUP = _read_envelope_lookup()
LPD_LOOKUP = _read_lpd_lookup()
SHW_LOOKUP = _read_shw_lookup()
HVAC_LOOKUP = _read_hvac_lookup()


BT_ALIASES = {BuildingType.SMALL_OFFICE: 'so', BuildingType.RETAIL_STRIPMALL: 'rs'}
HVAC_ALIASES = {
    HVACSystemType.PSZ_AC_WITH_ELECTRIC_COIL: 'sys2',
    HVACSystemType.PSZ_AC_WITH_GAS_COIL: 'sys3',
    HVACSystemType.PSZ_HP: 'sys1',
}

# Test params
ASPECT_RATIOS = [1.0, 6.0]
SHGCS = [0.22, 0.45]

HVAC_SYSTEM_TYPES = [
    HVACSystemType.PSZ_HP,
    HVACSystemType.PSZ_AC_WITH_ELECTRIC_COIL,
    HVACSystemType.PSZ_AC_WITH_GAS_COIL,
]

BUILDING_TYPES = [x for x in BuildingType]
SHW_TYPES = [x for x in SHWType]
CLIMATE_ZONES = [x for x in ClimateZone]
CASE_TYPES = [x for x in CaseType]
BUILDING_SIZES = [x for x in BuildingSize]


RESULTS_INDEX_NAMES = [
    'BuildingType',
    'HVACSystemType',
    'SHWType',
    'ClimateZone',
    'BuildingSize',
    'CaseType',
    'Aspect Ratio',
    'Number of Floors',
]


def _read_expected_results():
    df = pd.read_json(TEST_RESULTS_PATH, dtype={k: str for k in RESULTS_INDEX_NAMES})
    df.set_index(RESULTS_INDEX_NAMES, inplace=True)
    return df

    df.set_index(df.columns.tolist()[:8])


RESULTS = _read_expected_results()


@dataclass
class SingleTestInfo:
    building_type: BuildingType
    hvac_type: HVACSystemType
    shw_type: SHWType
    climate_zone: ClimateZone
    building_size: BuildingSize
    case_type: CaseType
    aspect_ratio: float
    number_of_floors: int

    def name(self) -> str:
        return (
            f"sqft{self.building_size.square_feet}_{BT_ALIASES[self.building_type]}_{HVAC_ALIASES[self.hvac_type]}_{self.shw_type}_"
            f"CZ{self.climate_zone}_ar{self.aspect_ratio}_nf{self.number_of_floors}_{self.case_type}"
        )

    def index(self) -> Tuple[str, ...]:
        return tuple(
            str(x)
            for x in (
                self.building_type,
                self.hvac_type,
                self.shw_type,
                self.climate_zone,
                self.building_size,
                self.case_type,
                self.aspect_ratio,
                self.number_of_floors,
            )
        )

    def envelope_info(self) -> Dict[str, float]:
        return ENVELOPE_LOOKUP[(self.climate_zone, self.case_type)]

    def shw_info(self) -> Dict[str, float]:
        """None for non gas."""
        if not self.hvac_type.is_gas:  # TODO; really?
            return {}

        return SHW_LOOKUP[(self.building_type, self.shw_type, self.case_type)]

    def lpd(self) -> float:
        return LPD_LOOKUP[(self.building_type, self.case_type)]

    def hvac_info(self) -> Dict[str, float]:
        return HVAC_LOOKUP[(self.building_type, self.hvac_type, self.case_type)]

    def to_json(self):
        return {
            'building_type': str(self.building_type),
            'climate_zone': str(self.climate_zone),
            'hvac_system': str(self.hvac_type),
            'gross_floor_area_m2': self.building_size.square_meter,
            'number_of_floors': self.number_of_floors,
            'aspect_ratio': self.aspect_ratio,
            **self.envelope_info(),
            'proposed_lpd_w_per_m2': self.lpd(),
            **self.shw_info(),
            **self.hvac_info(),
            **DEFAULT_ECONOMICS,
        }

    def to_param(self):
        return pytest.param(self, id=self.name())

    def expected_results(self):
        return RESULTS.loc[self.index()]


def get_all_tests() -> List[SingleTestInfo]:
    all_tests: List[SingleTestInfo] = []
    for building_type in BUILDING_TYPES:
        for hvac_type in HVAC_SYSTEM_TYPES:
            for shw_type in SHW_TYPES:
                for climate_zone in CLIMATE_ZONES:
                    for aspect_ratio in ASPECT_RATIOS:
                        for case_type in CASE_TYPES:
                            for building_size in BUILDING_SIZES:
                                for number_of_floors in building_size.generate_number_of_floors():
                                    all_tests.append(
                                        SingleTestInfo(
                                            building_type=building_type,
                                            hvac_type=hvac_type,
                                            shw_type=shw_type,
                                            climate_zone=climate_zone,
                                            building_size=building_size,
                                            case_type=case_type,
                                            aspect_ratio=aspect_ratio,
                                            number_of_floors=number_of_floors,
                                        )
                                    )
    return all_tests


@pytest.mark.parametrize(
    "test_info",
    [t.to_param() for t in get_all_tests()],
)
def test_calculate_savings(test_info: SingleTestInfo):
    property_info = PropertyInfo(**test_info.to_json())
    calculator_outputs = calculate_savings(property_info=property_info)
    assert isinstance(calculator_outputs, CalculatorOutputs)
    results = calculator_outputs.to_dict()
    assert test_info.case_type.savings_percent_limit(results['savings_total_cost_percent_actual'])
    expected_results = test_info.expected_results().to_dict()

    assert sorted(results.keys()) == sorted(expected_results.keys())
    for k, expected in expected_results.items():
        actual = round(results[k], N_DECIMALS)
        assert actual == pytest.approx(expected), f"Difference for {k}"


@pytest.mark.parametrize(
    "test_info",
    [t.to_param() for t in get_all_tests()],
)
def test_is_valid_pydantic(test_info: SingleTestInfo):
    PropertyInfo.from_dict(test_info.to_json())


def _regenerate_test_results() -> pd.DataFrame:
    results = {}
    statuses = {}
    for t in get_all_tests():
        sim_ok = True
        error_msg = None
        property_info = PropertyInfo(**t.to_json())
        index = t.index()
        try:
            d = calculate_savings(property_info)
            results[index] = d.to_dict()
        except Exception as e:
            sim_ok = False
            error_msg = f"{type(e).__name__}: {e}"

        statuses[index] = {'status': sim_ok, 'error': error_msg}

    df = pd.DataFrame(results).T
    df.index.names = RESULTS_INDEX_NAMES

    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    df_status = pd.DataFrame(statuses).T
    df_status.index.names = RESULTS_INDEX_NAMES
    failed = df_status[df_status['status'] == False]
    if not failed.empty:
        raise ValueError(f"{len(failed)} simulation failed: {failed}")

    df.round(N_DECIMALS).reset_index().to_json(TEST_RESULTS_PATH, orient='records', indent=2)
    return df
