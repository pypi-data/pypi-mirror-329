import joblib
import numpy as np

import calculator_179d.calculate_common_features as ccf
from calculator_179d.constants import GJ_TO_KBTU
from calculator_179d.data_types import FuelType, ModelType, PropertyInfo


class SurrogateModel:
    def __init__(self, model_type: ModelType, fuel_type: FuelType, property_info: PropertyInfo):
        self.model_type = model_type
        self.fuel_type = fuel_type
        self.property_info = property_info
        self.surrogate_model = self._read_proposed_model()

    # pick the sklearn model based on bldg type, climate zone and hvac_system
    def _read_proposed_model(self):
        model_path = self.property_info.get_model_file_path(model_type=self.model_type, fuel_type=self.fuel_type)
        with open(model_path, 'rb') as f:
            model = joblib.load(f)

        return model

    # create input array used for model prediction
    def _create_input_array(self):
        # calculated features - ua building, ACH infiltration, surface to volume ratio
        [cooling_cop, heating_cop] = ccf.calculate_cooling_and_heating_cop(property_info=self.property_info)
        ua_bldg = ccf.calculate_ua_bldg(property_info=self.property_info)
        ach_infiltration = ccf.calculate_ACH_infiltration(property_info=self.property_info)
        sa_to_vol_ratio = ccf.calculate_sa_to_vol_ratio(property_info=self.property_info)
        ext_wall_surface_area = ccf.calculate_ext_wall_surface_area(property_info=self.property_info)
        window_area = ccf.calculate_window_area(property_info=self.property_info)
        roof_area = ccf.calculate_roof_area(property_info=self.property_info)

        if self.fuel_type == FuelType.NATURALGAS:
            [wh_ua_w_per_K, wh_eta_burner_final] = self.property_info.calculate_wh_ua_and_efficiency()

            return np.array(
                [
                    [
                        self.property_info.number_of_floors,
                        self.property_info.gross_floor_area_m2,
                        ua_bldg,
                        self.property_info.window_wall_ratio,
                        self.property_info.window_shgc,
                        ach_infiltration,
                        self.property_info.proposed_lpd_w_per_m2,
                        heating_cop,
                        sa_to_vol_ratio,
                        self.property_info.aspect_ratio,
                        ext_wall_surface_area,
                        roof_area,
                        window_area,
                        self.property_info.wall_u_value_w_per_m2_k,
                        self.property_info.window_u_factor_w_per_m2_k,
                        self.property_info.roof_u_value_w_per_m2_k,
                        wh_eta_burner_final,
                        wh_ua_w_per_K,
                    ]
                ]
            )

        # create input array - same order as used during model development
        # include heating cop if hvac system is heat pump
        if self.property_info.hvac_system.is_heat_pump:
            return np.array(
                [
                    [
                        self.property_info.number_of_floors,
                        self.property_info.gross_floor_area_m2,
                        ua_bldg,
                        self.property_info.window_wall_ratio,
                        self.property_info.window_shgc,
                        ach_infiltration,
                        self.property_info.proposed_lpd_w_per_m2,
                        cooling_cop,
                        heating_cop,  # This is added here, omitted when not an HP
                        sa_to_vol_ratio,
                        self.property_info.aspect_ratio,
                        ext_wall_surface_area,
                        roof_area,
                        window_area,
                        self.property_info.wall_u_value_w_per_m2_k,
                        self.property_info.window_u_factor_w_per_m2_k,
                        self.property_info.roof_u_value_w_per_m2_k,
                    ]
                ]
            )

        # Electricity, not HP
        return np.array(
            [
                [
                    self.property_info.number_of_floors,
                    self.property_info.gross_floor_area_m2,
                    ua_bldg,
                    self.property_info.window_wall_ratio,
                    self.property_info.window_shgc,
                    ach_infiltration,
                    self.property_info.proposed_lpd_w_per_m2,
                    cooling_cop,
                    # heating_cop,
                    sa_to_vol_ratio,
                    self.property_info.aspect_ratio,
                    ext_wall_surface_area,
                    roof_area,
                    window_area,
                    self.property_info.wall_u_value_w_per_m2_k,
                    self.property_info.window_u_factor_w_per_m2_k,
                    self.property_info.roof_u_value_w_per_m2_k,
                ]
            ]
        )

        # Predict annual electricity 179d

    def estimate_annual_kbtu(self) -> float:
        # create input array for prediction
        input_array = self._create_input_array()
        # predict floor area normalized annualy electricity 179d
        return self.surrogate_model.predict(input_array)[0][0] * GJ_TO_KBTU
