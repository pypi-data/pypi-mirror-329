# ----- Metric conversion from AHRI metrics to COP for use in the surrogate modeling and also include other metrics --------------

# ------- Cooling
# Inputs:
# seer
# eer
# seer2
# eer2
# Outputs:
#    COP

# ------- Heating
# Inputs:
# HSPF
# HSPF2
# HeatingCOP (COP47)
# Boiler Average Efficiency
# Gas Coil Average Efficiency
# Outputs:
#    COP

# Usage:
# args={'SEER':10,'HSPF':5}
# CoolingCOP,HeatingCOP=AHRI2COP(**args)


def AHRI2COP(args):

    if ('SEER' in args) and (args['SEER'] > 0):

        coolingcop = 0.2692 * args['SEER'] + 0.2706

    elif ('SEER2' in args) and (args['SEER2'] > 0):

        seer = args['SEER2'] / 0.95  # SEER2 to SEER conversion (SEER2/SEER=0.95)
        coolingcop = 0.2692 * seer + 0.2706

    elif ('EER' in args) and (args['EER'] > 0):

        r = 0.12
        coolingcop = (args['EER'] / 3.413 + r) / (1 - r)

    elif ('EER2' in args) and (args['EER2'] > 0):

        eer = args['EER2'] / 0.95  # EER2 to EER conversion (EER2/EER=0.95)
        r = 0.12
        coolingcop = (eer / 3.413 + r) / (1 - r)

    else:

        print('System type is different than DX')

    if ('electric coil') in args['hvac_system']:
        heatingcop = 0

    elif ('HSPF' in args) and (args['HSPF'] > 0):
        heatingcop = 0.0353 * args['HSPF'] * args['HSPF'] + 0.0331 * args['HSPF'] + 0.9447

    elif ('HSPF2' in args) and (args['HSPF2'] > 0):
        hspf = args['HSPF2'] / 0.84  # SEER2 to SEER conversion (HSPF2/HSPF=0.84)
        heatingcop = 0.0353 * hspf**2 + 0.0331 * hspf + 0.9447

    elif ('heatingCOP' in args) and (args['heatingCOP'] > 0):
        heatingcop = (
            1.48e-7 * args['heatingCOP'] * args['heating_capacity_btu_per_h'] + 1.062 * args['heatingCOP']
        )  # Heater capacity in Btu/hr  ToDo: check the heating_capacity_btu_per_h as part of inputs with COP47

    elif ('boiler_average_efficiency' in args) and (args['boiler_average_efficiency'] > 0):
        heatingcop = args['boiler_average_efficiency']

    elif ('gas_coil_average_efficiency' in args) and (args['gas_coil_average_efficiency'] > 0):
        heatingcop = args['gas_coil_average_efficiency']

    else:
        print('Web tool efficiency metrics do not match the modeled')

    return coolingcop, heatingcop
