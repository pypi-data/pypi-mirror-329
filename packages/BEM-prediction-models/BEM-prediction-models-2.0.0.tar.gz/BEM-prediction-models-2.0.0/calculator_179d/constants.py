"""This defines some constants such as conversions between SI and IP units."""

from pathlib import Path

#: Giga Joules to kBTu
GJ_TO_KBTU = 947.817
#: Square feet to square meters
FT2_TO_M2 = 0.09290304
#: Square meters to square feet
M2_TO_FT2 = 1 / FT2_TO_M2

#: Btu/h to Watts (W)
#: Equivalent to openstudio.convert(1, "kBtu", "kWh").get()
BTU_PER_H_TO_W = 0.29307107

#: kBtu to kWh
KBTU_TO_KWH = 0.293014  # TODO: this is wrong!
#: kBtu to thousand cu.ft (= therms)
KBTU_TO_THOUSAND_CUFT = 1.0 / 1039.0
# Cents to dollars
CENTS_TO_DOLLARS = 1.0 / 100
#: Convert an IP U-value in Btu/ft^2*h*R to an SI U-value in W/m^2*K
#: Equivalent to ``openstudio.convert(1, 'Btu/ft^2*h*R', 'W/m^2*K').get()``
U_VALUE_IP_TO_SI = 5.678

#: root dir of the calculator_179d package
PACKAGE_DIR = Path(__file__).parent
#: where the model files .pk are stored
MODEL_FILES_DIR = PACKAGE_DIR / 'model_files'
