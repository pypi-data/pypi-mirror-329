import numpy as np

import calculator_179d.SurrogateModelMetricConversion as smc
from calculator_179d.data_types import BuildingType, PropertyInfo

# TODO: move most of these to the PropertyInfo probably, or at least specify exactly the arguments it needs


def calculate_ext_wall_surface_area(property_info: PropertyInfo) -> float:

    if property_info.building_type == BuildingType.SMALL_OFFICE:
        floor_to_floor_height_m = 10 * 0.3048  # floor height in m
    elif property_info.building_type == BuildingType.RETAIL_STRIPMALL:
        floor_to_floor_height_m = 17 * 0.3048  # floor height for retail stripmall
    else:
        raise ValueError(f"Non implemented for Building Type {property_info.building_type}")

    # floor area in m^2
    floor_area_m2 = property_info.gross_floor_area_m2 / property_info.number_of_floors
    # gross ext wall surface area in m^2
    ext_wall_surface_area_gross = (
        2
        * floor_to_floor_height_m
        * (np.sqrt(property_info.aspect_ratio * floor_area_m2) + np.sqrt(floor_area_m2 / property_info.aspect_ratio))
    ) * property_info.number_of_floors
    # opaque ext wall surface area in m^2
    ext_wall_surface_area = (1 - property_info.window_wall_ratio) * ext_wall_surface_area_gross

    return ext_wall_surface_area


def calculate_window_area(property_info: PropertyInfo) -> float:

    # opaque ext wall surface area
    ext_wall_surface_area = calculate_ext_wall_surface_area(property_info)
    # gross ext wall surface area
    ext_wall_surface_area_gross = ext_wall_surface_area / (1 - property_info.window_wall_ratio)
    window_area = property_info.window_wall_ratio * ext_wall_surface_area_gross

    return window_area


def calculate_roof_area(property_info):

    gross_floor_area_m2 = property_info.gross_floor_area_m2
    n_stories = property_info.number_of_floors
    roof_area = gross_floor_area_m2 / n_stories

    return roof_area


def calculate_ACH_infiltration(property_info):

    # bldg_type = property_info.building_type
    # if bldg_type == 'small office':
    floor_area_m2 = property_info.gross_floor_area_m2 / property_info.number_of_floors

    I = 0.0115824
    ach_infiltration = (
        (
            I
            * 120
            * (
                np.sqrt(property_info.aspect_ratio * floor_area_m2)
                + np.sqrt(floor_area_m2 / property_info.aspect_ratio)
            )
        )
        / (floor_area_m2 * property_info.number_of_floors)
    ) * property_info.number_of_floors

    return ach_infiltration


def calculate_ua_bldg(property_info):

    # calculate external wall surface area
    ext_wall_surface_area = calculate_ext_wall_surface_area(property_info)
    # calculate roof area
    roof_area = calculate_roof_area(property_info)
    # calculate window area
    window_area = calculate_window_area(property_info)

    # calculate ua_bldg
    ua_bldg = (
        roof_area * property_info.roof_u_value_w_per_m2_k
        + ext_wall_surface_area * property_info.wall_u_value_w_per_m2_k
        + window_area * property_info.window_u_factor_w_per_m2_k
    )

    return ua_bldg


def calculate_sa_to_vol_ratio(property_info):

    # calculate roof area
    roof_area = calculate_roof_area(property_info)
    # calculate surface to volume ratio
    sa_to_vol_ratio = 2.0 * (
        (property_info.aspect_ratio / roof_area) ** 0.5 + (1.0 / (property_info.aspect_ratio * roof_area)) ** 0.5
    ) + (1.0 / (10.0 * property_info.number_of_floors))

    return sa_to_vol_ratio


def calculate_cooling_and_heating_cop(property_info):
    ##COP values from ahri
    ahri_args = {}
    # get cooling and heating cop
    for feature in PropertyInfo.EXCLUSIVE_COOLING_METRICS:
        value = getattr(property_info, feature)
        if value is not None and value > 0:
            ahri_args[feature] = value

    for feature in PropertyInfo.EXCLUSIVE_HEATING_METRICS:
        value = getattr(property_info, feature)
        if value is not None and value > 0:
            ahri_args[feature] = value

    ahri_args['hvac_system'] = str(property_info.hvac_system)
    # add heating capacity if heatingCOP ahri metric provided
    if property_info.heatingCOP is not None:
        ahri_args['heating_capacity_btu_per_h'] = property_info.heating_capacity_btu_per_h

    # calculate heating and cooling efficiency values for surrogate model feature inputs
    [cooling_cop, heating_cop] = smc.AHRI2COP(ahri_args)

    return [cooling_cop, heating_cop]
