from .electron_transport import max_canopy_electron_transport_at_25
from .tomato_constants import *


def co2_concentration_inside_stomata(air_co2):
    """
    Equation 9.21
    stomata_CO2_concentration = GREENHOUSE_AIR_TO_STOMATA_CO2_CONCENTRATION*CO2
    Returns: CO2 concentration inside stomata [µmol {CO2} mol^-1 {air}]
    """
    return GREENHOUSE_AIR_TO_STOMATA_CO2_CONCENTRATION * air_co2


def co2_compensation(carbohydrate_amount_Leaf, canopy_t):
    """
    Equation 9.23
    CO2_compensation_point = (max_canopy_electron_transport_rate_at_25/MAX_LEAF_ELECTRON_TRANSPORT_RATE)*CANOPY_TEMPERATURE_EFFECT * t_Canopy
                            + 20*CANOPY_TEMPERATURE_EFFECT*(1-(max_canopy_electron_transport_rate_at_25/MAX_LEAF_ELECTRON_TRANSPORT_RATE))
    Returns: CO2 compensation point [µmol {CO2} mol^-1 {air}]
    """
    max_canopy_electron_transport_rate_at_25 = max_canopy_electron_transport_at_25(carbohydrate_amount_Leaf)
    return (max_canopy_electron_transport_rate_at_25/MAX_LEAF_ELECTRON_TRANSPORT_RATE)*CANOPY_TEMPERATURE_EFFECT * canopy_t \
         + 20*CANOPY_TEMPERATURE_EFFECT*(1-(max_canopy_electron_transport_rate_at_25/MAX_LEAF_ELECTRON_TRANSPORT_RATE))

