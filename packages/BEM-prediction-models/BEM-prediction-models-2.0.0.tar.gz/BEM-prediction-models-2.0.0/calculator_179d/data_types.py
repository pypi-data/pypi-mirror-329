"""This defines the enums and the main Pydantic Model ``PropertyInfo`` for the inputs."""

import json
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, model_validator
from strenum import StrEnum
from typing_extensions import Annotated

from calculator_179d.constants import MODEL_FILES_DIR
from calculator_179d.waterheater_attributes import (
    calculate_commercial_wh_ua_and_eff,
    calculate_residential_wh_ua_and_eff,
)


class FuelType(StrEnum):
    """Fuel Type"""

    ELECTRICITY = 'electricity'
    NATURALGAS = 'naturalgas'


class ModelType(StrEnum):
    """What is being modeled: Baseline or Proposed"""

    BASELINE = "baseline"
    PROPOSED = "proposed"


class BuildingType(StrEnum):
    """Building Types."""

    # TODO: some of these are commented out until we get data for them

    SMALL_OFFICE = 'small office'
    # MEDIUM_OFFICE = 'medium office'
    # LARGE_OFFICE = 'large office'
    # PRIMARY_SCHOOL = 'primary school'
    # FULL_SERVICE_RESTAURANT = 'full service restaurant'
    # QUICK_SERVICE_RESTAURANT = 'quick service restaurant'
    # RETAIL_STANDALONE = 'retail standalone'
    RETAIL_STRIPMALL = 'retail stripmall'
    # SMALL_HOTEL = 'small hotel'
    # WAREHOUSE = 'warehouse'


# climate zones
class ClimateZone(StrEnum):
    """Valid Climate Zones."""

    CZ_1A = '1A'
    CZ_2A = '2A'
    CZ_2B = '2B'
    CZ_3A = '3A'
    CZ_3B = '3B'
    CZ_3C = '3C'
    CZ_4A = '4A'
    CZ_4B = '4B'
    CZ_4C = '4C'
    CZ_5A = '5A'
    CZ_5B = '5B'
    CZ_6A = '6A'
    CZ_6B = '6B'
    CZ_7 = '7'
    CZ_8 = '8'


class HVACSystemType(StrEnum):
    """Supported HVAC System Types.

    The surrogate models can only handle 3 system types -- PSZ-HP, PSZ-AC with electric coil, PSZ-AC with gas coil.
    """

    PSZ_AC_WITH_ELECTRIC_COIL = 'PSZ-AC with electric coil'
    # PSZ_AC_WITH_GAS_BOILER = 'PSZ-AC with gas boiler'
    PSZ_AC_WITH_GAS_COIL = 'PSZ-AC with gas coil'
    PSZ_HP = 'PSZ-HP'
    # PTAC_WITH_ELECTRIC_COIL = 'PTAC with electric coil'
    # PTAC_WITH_GAS_COIL = 'PTAC with gas coil'
    # RESIDENTIAL_AC_WITH_RESIDENTIAL_FORCED_AIR_FURNACE = 'Residential AC with residential forced air furnace'
    # PTHP = 'PTHP'
    # PVAV_WITH_GAS_HEAT_WITH_ELECTRIC_REHEAT = 'PVAV with gas heat with electric reheat'

    @property
    def is_heat_pump(self) -> bool:
        return self in [
            HVACSystemType.PSZ_HP,
            # HVACSystemType.PTHP,
        ]

    @property
    def is_gas(self) -> bool:
        return self in [
            # HVACSystemType.PSZ_AC_WITH_GAS_BOILER,
            HVACSystemType.PSZ_AC_WITH_GAS_COIL,
            # HVACSystemType.PTAC_WITH_GAS_COIL,
            # HVACSystemType.RESIDENTIAL_AC_WITH_RESIDENTIAL_FORCED_AIR_FURNACE,
            # HVACSystemType.PVAV_WITH_GAS_HEAT_WITH_ELECTRIC_REHEAT
        ]


class PropertyInfo(BaseModel):
    """This is to the PropertyInfo, as a dataclass that serves as a validation facility"""

    LPD_W_PER_M2_BOUNDS: ClassVar[Dict[BuildingType, Tuple[float, float]]] = {
        BuildingType.SMALL_OFFICE: (4.5, 10.77),
        BuildingType.RETAIL_STRIPMALL: (4.77, 16.15),
    }

    EXCLUSIVE_COOLING_METRICS: ClassVar[List[str]] = ["SEER", "EER", "EER2", "SEER2"]
    EXCLUSIVE_HEATING_METRICS: ClassVar[List[str]] = [
        'gas_coil_average_efficiency',
        'boiler_average_efficiency',
        'HSPF',
        'HSPF2',
        'heatingCOP',
    ]
    SHW_INPUTS_RESIDENTIAL: ClassVar[List[str]] = [
        'water_heating_standby_loss_btu_per_h',
        'water_heating_thermal_efficiency',
    ]
    SHW_INPUTS_COMMERCIAL: ClassVar[List[str]] = [
        'water_heating_first_hour_rating_gal_per_h',
        'water_heating_uef',
        'water_heating_capacity_btu_per_h',
    ]

    # Required property information
    building_type: BuildingType

    climate_zone: ClimateZone

    hvac_system: HVACSystemType

    gross_floor_area_m2: Annotated[
        float,
        Field(
            title="Gross floor area of conditionned spaces",
            json_schema_extra={"units": "m^2"},
            ge=92.9,  #  1,000 ft^2
            lt=2323,  # 25,000 ft^2
        ),
    ]

    number_of_floors: Annotated[
        int,
        Field(
            title="Number of Floors",
            description="Enter the number of floors in the building fully above ground level (above grade)",
            ge=1,
            le=3,
        ),
    ]

    aspect_ratio: Annotated[
        float,
        Field(
            title="Aspect Ratio",
            description="Ratio of the longest dimension of the building footprint to the narrowest dimension",
            json_schema_extra={"$comment": "An aspect ratio of 1.0 represents a square building footprint"},
            ge=1.0,
            le=6.0,
        ),
    ]

    window_wall_ratio: Annotated[
        float,
        Field(
            title="Percentage of Gross Above-Grade Wall Area (WWR)",
            json_schema_extra={"units": "ratio"},
            ge=0.0,
            le=0.4,  # 40%
        ),
    ]

    roof_u_value_w_per_m2_k: Annotated[
        float,
        Field(
            title="Roof Assembly U-Value (Thermal Transmittance)",
            description=(
                "Heat transmission in unit time through unit area of a material or construction and "
                "the boundary air films, induced by unit temperature difference between the environments on each side."
            ),
            json_schema_extra={"units": "W/(m^2*K)"},
        ),
    ]

    wall_u_value_w_per_m2_k: Annotated[
        float,
        Field(
            title="Wall Assembly U-Value (Thermal Transmittance)",
            description=(
                "Heat transmission in unit time through unit area of a material or construction and "
                "the boundary air films, induced by unit temperature difference between the environments on each side."
            ),
            json_schema_extra={"units": "W/(m^2*K)"},
        ),
    ]

    window_u_factor_w_per_m2_k: Annotated[
        float,
        Field(
            title="Window Assembly U-Value (Thermal Transmittance)",
            description=(
                "Heat transmission in unit time through unit area of a material or construction and "
                "the boundary air films, induced by unit temperature difference between the environments on each side."
            ),
            json_schema_extra={
                "units": "W/(m^2*K)",
                "$comment": "Reported values for window U-factor should be assembly values that include the effects of frames",
            },
        ),
    ]

    window_shgc: Annotated[
        float,
        Field(
            title="Solar Heat Gain Coefficient (SHGC)",
            description=(
                "The ratio of the solar heat gain entering the space through the fenestration area "
                "to the incident solar radiation. Solar heat gain includes directly transmitted solar heat "
                "and absorbed solar radiation, which is then reradiated, conducted, or convected into the space"
            ),
            json_schema_extra={
                "$comment": "Reported values for window U-factor should be assembly values that include the effects of frames",
            },
        ),
    ]

    proposed_lpd_w_per_m2: Annotated[
        float,
        Field(
            title="Lighting power density (LPD)",
            description="The maximum lighting power per unit area of a building classification of space function",
            json_schema_extra={"$units": "W/m^2"},
            ge=4.49,  # 0.4184353 W/ft^2
            le=21.52,  # 2.0 W/ft^2, or tests don't validate Note: 179d_web uses 1 W/ft^2 / 10.77 W/m^2
        ),
    ]

    # Required economics
    electricity_rate_cents_per_kwh: Annotated[
        float,
        Field(
            title="Electricity rate",
            description="The cost of electricty per kWh",
            json_schema_extra={"$units": "cents/kWh"},
            # Wide bounds for now
            ge=5,
            le=80,
        ),
    ]
    natural_gas_rate_usd_per_therm: Annotated[
        float,
        Field(
            title="Natural Gas rate",
            description="The cost of gas per kWh",
            json_schema_extra={"$units": "USD/therm"},
            # Wide bounds for now
            ge=5,
            le=50,
        ),
    ]  #: USD per therm (1000 cu.ft)

    # TODO: unclear what these are
    energy_tax_deduction_rate_min: float
    energy_tax_deduction_rate_max: float
    all_179d_tax_deduction_rate_min: float
    all_179d_tax_deduction_rate_max: float
    increment_energy: float
    min_threshold_energy: float
    increment_all_179d: float
    min_threshold_all_179d: float

    # Optional SHW
    ## Commercial
    water_heating_standby_loss_btu_per_h: Annotated[
        Optional[float],
        Field(
            default=None,
            title="Water Heater Standby Loss",
            description=(
                "The average hourly energy required to maintain the stored water temperature based on a 70F "
                "temperature differential between stored water and ambient room temperature"
            ),
            json_schema_extra={"$units": "Btu/h"},  # Note: Really. Everything is passed as SI, but this is in IP.
            ge=800.0,
            le=1600.0,
        ),
    ]
    water_heating_thermal_efficiency: Annotated[
        Optional[float],
        Field(
            default=None,
            title="Water Heater Thermal Efficiency",
            description=(
                "The ratio of the heat energy transferred to the water flowing through the water heater "
                "to the amount of energy consumed by the water heater during full-firing rate, steady-state operation"
            ),
            json_schema_extra={"$units": "%"},
            ge=80.0,
            le=97.0,
        ),
    ]
    ## Residential
    water_heating_first_hour_rating_gal_per_h: Annotated[
        Optional[float],
        Field(
            default=None,
            title="Water Heater First Hour Rating (FHR)",
            description=(
                "An estimate of the maximum volume of hot water in gallons that a storage water heater can supply "
                "within an hour that begins with the water heater fully heated. The FHR is measured at "
                "a 125°F outlet temperature in the Uniform Energy Factor test method"
            ),
            json_schema_extra={"$units": "gal/h"},  # Note: Really.
            ge=45.0,
            le=120.0,
        ),
    ]
    water_heating_uef: Annotated[
        Optional[float],
        Field(
            default=None,
            title="Water Heater Uniform Energy Factor (UEF)",
            description=(
                "The newest measure of water heater overall efficiency. The higher the UEF value is, the more "
                "efficient the water heater. UEF is determined by the Department of Energy's test method outlined "
                "in 10 CFR Part 430, Subpart B, Appendix E"
            ),
            json_schema_extra={"$units": "ratio"},
            ge=0.5,
            le=0.9,
        ),
    ]
    water_heating_capacity_btu_per_h: Annotated[
        Optional[float],
        Field(
            default=None,
            title="Water Heater Capacity",
            description="The heating input capacity of the water heater",
            json_schema_extra={"$units": "Btu/h"},
            ge=25000,
            le=65000,
        ),
    ]

    # Cooling: One of these is expected
    SEER: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Seasonal Energy Efficiency Ratio (SEER)',
            description='the total cooling output of an air conditioner during its normal annual usage period for cooling (Btu) divided by the total electric energy input during the same period (W).',
            json_schema_extra={"$units": "Btu/(W*h)"},
            ge=9.686780461,
            le=21.28306092,
        ),
    ]

    SEER2: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Seasonal Energy Efficiency Ratio (SEER2)',
            description='the total cooling output of an air conditioner during its normal annual usage period for cooling (Btu) divided by the total electric energy input during the same period (W). Effective January 1, 2023, SEER2 reflects the new efficiency metric.',
            json_schema_extra={"$units": "Btu/(W*h)"},
            ge=9.202441437,
            le=20.21890788,
        ),
    ]

    EER: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Energy Efficiency Ratio (EER)',
            description='the ratio of net cooling capacity (Btu/h) to total rate of electric input in watts under designated operating conditions.',
            json_schema_extra={"$units": "Btu/(W*h)"},
            ge=8.235185188,
            le=17.61108,
        ),
    ]

    EER2: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Energy Efficiency Ratio (EER2)',
            description='the ratio of net cooling capacity (Btu/h) to total rate of electric input in watts under designated operating conditions. Effective January 1, 2023, EER2 reflects the new efficiency metric.',
            json_schema_extra={"$units": "Btu/(W*h)"},
            ge=7.823425928,
            le=16.730526,
        ),
    ]

    # Heating: One of these is expected
    gas_coil_average_efficiency: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Gas Coil Average Efficiency',
            description="Capacity weighted average gas coil efficiency for all gas coil equipment",
            json_schema_extra={"$units": "ratio"},
            ge=0.8,
            le=0.98,
        ),
    ]
    boiler_average_efficiency: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Heating Seasonal Performance Factor (HSPF)',
            description='the total heating output of a heat pump during its normal annual usage period for heating (Btu) divided by the total electric energy input during the same period.',
            json_schema_extra={"$units": "ratio"},
            ge=0.8,
            le=0.98,
        ),
    ]
    HSPF: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Heating Seasonal Performance Factor (HSPF)',
            description='the total heating output of a heat pump during its normal annual usage period for heating (Btu) divided by the total electric energy input during the same period.',
            json_schema_extra={"$units": "Btu/W*h"},
            ge=6.96630427,
            le=11.5073646,
        ),
    ]

    HSPF2: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Heating Seasonal Performance Factor (HSPF2)',
            description='the total heating output of a heat pump during its normal annual usage period for heating (Btu) divided by the total electric energy input during the same period. HSPF2 reflects the new higher static and load line (new efficiency metric) effective January 1, 2023.',
            json_schema_extra={"$units": "Btu/W*h"},
            ge=5.851695587,
            le=9.666186264,
        ),
    ]
    heatingCOP: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Heating Coefficient of Performance (COP)',
            description='the ratio of the rate of heat delivered to the rate of energy input, in consistent units, for a complete heat pump system, including the compressor under ARI operating conditions of outdoor temperature at 47°F (Dry-bulb) / 43°F (Wet-bulb) as indicated by Tables 6.8.1B and 6.8.1D of ASHRAE 90.1-2007.',
            json_schema_extra={"$units": "Btu/W*h"},
            ge=2.692641576,
            le=4.453150928,
        ),
    ]

    # Only expected if it's a HP
    heating_capacity_btu_per_h: Annotated[
        Optional[float],
        Field(
            default=None,
            title='Heating Capacity',
            description='total heating capacity as a sum of individual unit capacity',
            json_schema_extra={"$units": "Btu/h"},
            ge=27741,
            le=3523044,
        ),
    ]

    @model_validator(mode='after')
    def check_lpd_per_building_type(self):
        """Check that the LPD is within correct bounds given the BuildingType."""
        min_lpd, max_lpd = PropertyInfo.LPD_W_PER_M2_BOUNDS[self.building_type]
        if not (min_lpd <= self.proposed_lpd_w_per_m2 <= max_lpd):
            raise ValueError(
                f"For building_type '{self.building_type}', LPD of {self.proposed_lpd_w_per_m2} W/m^2 "
                f"is outside the allowable range: [{min_lpd}, {max_lpd}]"
            )
        return self

    @model_validator(mode='after')
    def check_water_heating(self):
        """Ensure either the residential or commercial metrics were passed, but not both."""

        # TODO: do we really not model DHW if it's an all electric building?
        if not self.hvac_system.is_gas:
            return self

        common_msg = (
            f"Pass either for residential: {PropertyInfo.SHW_INPUTS_RESIDENTIAL}, "
            f"or for commercial: {PropertyInfo.SHW_INPUTS_COMMERCIAL}"
        )

        # Residential
        if self.water_heating_standby_loss_btu_per_h is not None:
            if self.water_heating_uef is not None:
                raise ValueError(f"Ambiguous condition, cannot determine if Residential or Commercial.\n{common_msg}")
            if self.water_heating_thermal_efficiency is None:
                raise ValueError(
                    "When water_heating_standby_loss_btu_per_h is passed, water_heating_thermal_efficiency must be passed."
                )
            return self

        # Commercial?
        if self.water_heating_uef is None:
            raise ValueError(f"Missing some inputs.\n{common_msg}")
        if self.water_heating_first_hour_rating_gal_per_h is None:
            raise ValueError(
                "When water_heating_uef is passed, water_heating_first_hour_rating_gal_per_h must be passed."
            )
        if self.water_heating_capacity_btu_per_h is None:
            raise ValueError("When water_heating_uef is passed, water_heating_capacity_btu_per_h must be passed.")

        return self

    @model_validator(mode='after')
    def heatingCOP_requires_heating_capacity(self):
        """When heatingCOP is passed, heating_capacity_btu_per_h is required."""
        if self.heatingCOP is not None:
            if self.heating_capacity_btu_per_h is None:
                raise ValueError("When heatingCOP is provided, heating_capacity_btu_per_h is required.")

        return self

    @classmethod
    def from_dict(cls, property_info: dict):
        """Constructor from a dictionary."""
        return cls(**property_info)

    @classmethod
    def from_json(cls, json_str: str):
        """Constructor from a json string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def _lookup_model_file_name(self, model_type: ModelType, fuel_type: FuelType) -> str:
        return f"{model_type}_{fuel_type}_{self.building_type}_{self.hvac_system}_CZ{self.climate_zone}.pk".replace(
            ' ', '_'
        )

    def get_model_file_path(self, model_type: ModelType, fuel_type: FuelType) -> Path:
        """Return the .pk file path.

        Raises if it cannot be found.
        """
        p = MODEL_FILES_DIR / self._lookup_model_file_name(model_type=model_type, fuel_type=fuel_type)
        assert p.is_file(), "Computed model file does not exist at '{p}'"
        return p

    def has_residential_wh(self) -> bool:
        """Check if it has a Residential water heater."""
        return self.hvac_system.is_gas and self.water_heating_standby_loss_btu_per_h is not None

    def has_commercial_wh(self) -> bool:
        """Check if it has a Commercial water heater."""
        return self.hvac_system.is_gas and self.water_heating_uef is not None

    def calculate_wh_ua_and_efficiency(self) -> Tuple[float, float]:
        """Calculate [ua_w_per_k, eta_burner_final], for either a Residential or a Commercial Water Heater."""
        if not self.hvac_system.is_gas:
            raise ValueError("Not calculated for all electric buildings.")

        if self.has_residential_wh():
            return calculate_residential_wh_ua_and_eff(
                water_heating_standby_loss_btu_per_h=self.water_heating_standby_loss_btu_per_h,  # type: ignore[arg-type]
                water_heating_thermal_efficiency=self.water_heating_thermal_efficiency,  # type: ignore[arg-type]
            )

        return calculate_commercial_wh_ua_and_eff(
            water_heating_uef=self.water_heating_uef,  # type: ignore[arg-type]
            water_heating_first_hour_rating_gal_per_h=self.water_heating_first_hour_rating_gal_per_h,  # type: ignore[arg-type]
            water_heating_capacity_btu_per_h=self.water_heating_capacity_btu_per_h,  # type: ignore[arg-type]
        )


if __name__ == "__main__":
    print("Generating the JSON Schema")
    schema = PropertyInfo.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["additionalProperties"] = False
    # Add mutually exclusive groups
    schema["allOf"] = [
        {
            "$comment": "Only one of these cooling metrics must be provided",
            "oneOf": [{"required": [x]} for x in PropertyInfo.EXCLUSIVE_COOLING_METRICS],
        },
        {
            "$comment": "Only one of these heating metrics must be provided",
            "oneOf": [{"required": [x]} for x in PropertyInfo.EXCLUSIVE_HEATING_METRICS],
        },
        {
            "$comment": "Validate the subset of SHW inputs needed based on residential v commercial",
            "oneOf": [
                {"$comment": "A residential WH", "required": [x for x in PropertyInfo.SHW_INPUTS_RESIDENTIAL]},
                {"$comment": "A commercial WH", "required": [x for x in PropertyInfo.SHW_INPUTS_COMMERCIAL]},
            ],
        },
    ]

    json_path = Path(__file__).parent / "calculator_179d_schema.json"
    json_path.write_text(json.dumps(schema, indent=2, sort_keys=True))
    print(f"Saved at {json_path}")
