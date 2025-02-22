import pytest

from calculator_179d.data_types import BuildingType, ClimateZone, HVACSystemType, PropertyInfo


@pytest.fixture
def property_info_dict():
    return {
        'building_type': BuildingType.SMALL_OFFICE,
        'climate_zone': ClimateZone.CZ_1A,
        'hvac_system': HVACSystemType.PSZ_AC_WITH_GAS_COIL,
        'gross_floor_area_m2': 92.90304,
        'number_of_floors': 1,
        'aspect_ratio': 1.0,
        'window_wall_ratio': 0.4,
        'roof_u_value_w_per_m2_k': 0.3571069182389937,
        'wall_u_value_w_per_m2_k': 0.7009876543209876,
        'window_u_factor_w_per_m2_k': 2.5551,
        'window_shgc': 0.22,
        'proposed_lpd_w_per_m2': 10.763910416709722,
        'electricity_rate_cents_per_kwh': 11.58,
        'natural_gas_rate_usd_per_therm': 11.38,
        'energy_tax_deduction_rate_min': 0.5,
        'energy_tax_deduction_rate_max': 1.0,
        'all_179d_tax_deduction_rate_min': 2.5,
        'all_179d_tax_deduction_rate_max': 5.0,
        'increment_energy': 0.02,
        'min_threshold_energy': 0.25,
        'increment_all_179d': 0.1,
        'min_threshold_all_179d': 0.25,
        'water_heating_standby_loss_btu_per_h': 850.0,
        'water_heating_thermal_efficiency': 96.5,
        'water_heating_first_hour_rating_gal_per_h': None,
        'water_heating_uef': None,
        'water_heating_capacity_btu_per_h': None,
        'SEER': 10.1,
        'SEER2': None,
        'EER': None,
        'EER2': None,
        'gas_coil_average_efficiency': 0.95,
        'boiler_average_efficiency': None,
        'HSPF': None,
        'HSPF2': None,
        'heatingCOP': None,
        'heating_capacity_btu_per_h': None,
    }


def test_fixture_is_ok(property_info_dict):
    PropertyInfo(**property_info_dict)


def test_water_heating_validation_all_electric_is_skipped(property_info_dict):
    property_info_dict["hvac_system"] = HVACSystemType.PSZ_HP

    property_info_dict['water_heating_standby_loss_btu_per_h'] = None
    property_info_dict['water_heating_thermal_efficiency'] = None
    property_info_dict['water_heating_first_hour_rating_gal_per_h'] = None
    property_info_dict['water_heating_uef'] = None
    property_info_dict['water_heating_capacity_btu_per_h'] = None

    PropertyInfo(**property_info_dict)


@pytest.mark.parametrize(
    "res_loss, res_et, com_uef, com_fhr, com_cap, error_msg",
    [
        [None, None, None, None, None, "Missing some inputs"],
        [
            800.0,
            None,
            None,
            None,
            None,
            "When water_heating_standby_loss_btu_per_h is passed, water_heating_thermal_efficiency must be passed.",
        ],
        [800.0, 96.6, 0.88, None, None, "Ambiguous condition"],
        [None, None, 0.88, None, None, "When water_heating_uef is passed, .* must be passed."],
        [None, None, 0.88, 50.0, None, "When water_heating_uef is passed, .* must be passed."],
        [None, None, 0.88, None, 60000, "When water_heating_uef is passed, .* must be passed."],
    ],
)
def test_water_heating_validation_missing(property_info_dict, res_loss, res_et, com_uef, com_fhr, com_cap, error_msg):
    property_info_dict["hvac_system"] = HVACSystemType.PSZ_AC_WITH_GAS_COIL

    property_info_dict['water_heating_standby_loss_btu_per_h'] = res_loss
    property_info_dict['water_heating_thermal_efficiency'] = res_et
    property_info_dict['water_heating_first_hour_rating_gal_per_h'] = com_fhr
    property_info_dict['water_heating_uef'] = com_uef
    property_info_dict['water_heating_capacity_btu_per_h'] = com_cap

    with pytest.raises(ValueError, match=error_msg):
        PropertyInfo(**property_info_dict)


def test_lpd_validation_per_building_type(property_info_dict):
    for bt, (min_lpd, max_lpd) in PropertyInfo.LPD_W_PER_M2_BOUNDS.items():
        property_info_dict["building_type"] = bt

        too_low_lpd = min_lpd - 0.0001
        too_high_lpd = max_lpd + 0.0001
        ok_lpd = (min_lpd + max_lpd) / 2.0

        property_info_dict["proposed_lpd_w_per_m2"] = ok_lpd
        PropertyInfo(**property_info_dict)

        for not_ok_lpd in [too_low_lpd, too_high_lpd]:
            property_info_dict["proposed_lpd_w_per_m2"] = not_ok_lpd

            with pytest.raises(ValueError, match="is outside the allowable range"):
                PropertyInfo(**property_info_dict)
