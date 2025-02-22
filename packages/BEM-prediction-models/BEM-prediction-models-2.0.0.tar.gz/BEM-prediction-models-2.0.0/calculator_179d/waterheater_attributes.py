"""Water Heater UA and Efficiency calculations."""

from typing import Optional, Tuple

from calculator_179d.constants import BTU_PER_H_TO_W


def calculate_commercial_wh_ua_and_eff(
    water_heating_uef: float,
    water_heating_first_hour_rating_gal_per_h: float,
    water_heating_capacity_btu_per_h: float,
) -> Tuple[float, float]:
    """Calculate [ua_w_per_k, eta_burner_final] for a Commercial Water Heater.

    Args:
        water_heating_uef (float): UEF, [0.5, 0.9] range
        water_heating_first_hour_rating_gal_per_h (float): First hour rating in GPH
        water_heating_capacity_btu_per_h (float): heater capacity in Btu/h

    Returns:
        [float, float]: [ua_w_per_k, eta_burner_final]
    """
    assert water_heating_uef >= 0.5 and water_heating_uef <= 0.9
    assert water_heating_first_hour_rating_gal_per_h > 0
    assert water_heating_capacity_btu_per_h > 0

    # define constant properties
    density = 8.2938  # lb/gal
    cp = 1.0007  # Btu/lb-F
    t_in = 58.0  # F
    t_env = 67.5  # F
    t = 125.0  # F

    ef = 0.9066 * water_heating_uef + 0.0711
    if ef >= 0.75:
        recovery_efficiency = 0.561 * ef + 0.439
    else:
        recovery_efficiency = 0.252 * ef + 0.608

    if water_heating_first_hour_rating_gal_per_h >= 0 and water_heating_first_hour_rating_gal_per_h < 18:
        volume_drawn = 10.0  # gal
    elif water_heating_first_hour_rating_gal_per_h >= 18 and water_heating_first_hour_rating_gal_per_h < 51:
        volume_drawn = 38.0  # gal
    elif water_heating_first_hour_rating_gal_per_h >= 51 and water_heating_first_hour_rating_gal_per_h < 75:
        volume_drawn = 55.0  # gal
    elif water_heating_first_hour_rating_gal_per_h >= 75 and water_heating_first_hour_rating_gal_per_h <= 130:
        volume_drawn = 84.0  # gal
    else:
        raise ValueError('first_hour_rating is beyond modeling range (< 130)')

    # calc ua_w_per_k and eta_burner_final
    draw_mass = volume_drawn * density  # lb
    q_load = draw_mass * cp * (t - t_in)  # Btu/day
    poww = water_heating_capacity_btu_per_h
    ua_btu_per_hr_r = ((recovery_efficiency / water_heating_uef) - 1.0) / (
        (t - t_env) * (24.0 / q_load) - ((t - t_env) / (poww * water_heating_uef))
    )  # Btu/hr-F
    eta_burner_final = recovery_efficiency + (
        (ua_btu_per_hr_r * (t - t_env)) / poww
    )  # conversion efficiency is slightly larger than recovery efficiency
    ua_w_per_k = ua_btu_per_hr_r / 3.41 * 0.555556  # Btu/hr-R to W/K, 1 Btu/hr = 1/3.41 W, 1 R = 0.555556 K

    return ua_w_per_k, eta_burner_final


def calculate_residential_wh_ua_and_eff(
    water_heating_standby_loss_btu_per_h: float,
    water_heating_thermal_efficiency: float,
) -> Tuple[float, float]:
    """Calculate [ua_w_per_k, eta_burner_final] for a Residential Water Heater.

    Args:
        water_heating_standby_loss_btu_per_h (float): Standby losses, Btu/h
        water_heating_thermal_efficiency (float): Efficiency as a percentage, [60, 99] range

    Returns:
        [float, float]: [ua_w_per_k, eta_burner_final]
    """
    assert water_heating_standby_loss_btu_per_h > 0
    assert water_heating_thermal_efficiency >= 60.0 and water_heating_thermal_efficiency <= 99.0

    delta_t_r = 70  # degF
    delta_t_k = delta_t_r * (5.0 / 9.0)

    ua_w_per_k = (water_heating_standby_loss_btu_per_h * BTU_PER_H_TO_W) / delta_t_k

    eta_burner_final = water_heating_thermal_efficiency / 100

    return ua_w_per_k, eta_burner_final


def calculate_wh_ua_and_efficiency(
    water_heating_standby_loss_btu_per_h: Optional[float] = None,
    water_heating_thermal_efficiency: Optional[float] = None,
    water_heating_uef: Optional[float] = None,
    water_heating_first_hour_rating_gal_per_h: Optional[float] = None,
    water_heating_capacity_btu_per_h: Optional[float] = None,
) -> Tuple[float, float]:
    """Calculate [ua_w_per_k, eta_burner_final].

    Args:
        For a residential SHW heater:
            water_heating_standby_loss_btu_per_h (float): Standby losses, Btu/h
            water_heating_thermal_efficiency (float): Efficiency as a percentage, [60, 99] range
        For a commercial SHW heater:
            water_heating_uef (float): UEF, [0.5, 0.9] range
            water_heating_first_hour_rating_gal_per_h (float): First hour rating in GPH
            water_heating_capacity_btu_per_h (float): heater capacity in Btu/h

    Returns:
        [float, float]: [ua_w_per_k, eta_burner_final]
    """

    # Residential
    if water_heating_standby_loss_btu_per_h is not None:
        assert water_heating_uef is None, "Ambigous condition, cannot determine if Residential or Commercial"
        assert water_heating_thermal_efficiency is not None
        return calculate_residential_wh_ua_and_eff(
            water_heating_standby_loss_btu_per_h=water_heating_standby_loss_btu_per_h,
            water_heating_thermal_efficiency=water_heating_thermal_efficiency,
        )

    # Commercial?
    assert water_heating_uef is not None, "Missing some inputs"
    assert water_heating_first_hour_rating_gal_per_h is not None
    assert water_heating_capacity_btu_per_h is not None
    return calculate_commercial_wh_ua_and_eff(
        water_heating_uef=water_heating_uef,
        water_heating_first_hour_rating_gal_per_h=water_heating_first_hour_rating_gal_per_h,
        water_heating_capacity_btu_per_h=water_heating_capacity_btu_per_h,
    )
