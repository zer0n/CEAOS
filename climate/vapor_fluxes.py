from climate.heat_fluxes import sensible_heat_flux_between_direct_air_heater_and_greenhouse_air
from climate.utils import *


def differentiable_air_to_obj_vapor_flux(VP_1: float, VP_2: float, HEC: float):
    # Equation 8.44
    return 6.4E-9 * HEC * (VP_1 - VP_2) / (1 + math.exp(S_MV12 * (VP_1 - VP_2)))


def general_vapor_flux(f_12: float, VP_1: float, VP_2: float, object_1_t: float, object_2_t: float):
    # Equation 8.45
    return M_WATER * f_12 * (VP_1 / (object_1_t + 273.15) + VP_2 / (object_2_t + 273.15)) / M_GAS


def fogging_system_to_greenhouse_air_latent_vapor_flux(setpoints: Setpoints):
    # Equation 8.64
    U_Fog = setpoints.U_Fog
    cap_Fog = Coefficients.ActiveClimateControl.cap_Fog
    floor_area = Coefficients.Construction.floor_area
    return U_Fog * cap_Fog / floor_area


def heat_blower_to_greenhouse_air_vapor_flux(setpoints: Setpoints):
    # Equation 8.55
    sensible_heat_flux_BlowAir = sensible_heat_flux_between_direct_air_heater_and_greenhouse_air(setpoints)
    return ETA_HEATVAP * sensible_heat_flux_BlowAir


def greenhouse_air_to_thermal_screen_vapor_flux(setpoints: Setpoints, states: States):
    air_t = states.air_t
    thermal_screen_t = states.thermal_screen_t
    HEC_AirThScr = 1.7 * setpoints.U_ThScr * abs(air_t - thermal_screen_t) ** 0.33
    thScr_vp = saturation_vapor_pressure(thermal_screen_t)
    return differentiable_air_to_obj_vapor_flux(states.air_vapor_pressure, thScr_vp, HEC_AirThScr)


def greenhouse_air_to_above_thermal_screen_vapor_flux(states: States, setpoints: Setpoints, weather: Weather):
    air_t = states.air_t
    above_thermal_screen_t = states.above_thermal_screen_t
    thScr_air_flux_rate = thermal_screen_air_flux_rate(setpoints, states, weather)
    f_AirTop = thScr_air_flux_rate
    return general_vapor_flux(f_AirTop, states.air_vapor_pressure, states.above_thermal_screen_vapor_pressure, air_t, above_thermal_screen_t)


def greenhouse_air_to_outdoor_vapor_flux(states: States, setpoints: Setpoints, weather: Weather):
    total_side_vent_rate = total_side_vents_ventilation_rates(setpoints, states, weather)
    f_VentForced = 0  # According to GreenLight, forced ventilation doesn't exist in this greenhouse
    f_AirOut = total_side_vent_rate + f_VentForced
    return general_vapor_flux(f_AirOut, states.air_vapor_pressure, weather.outdoor_vp, states.air_t, weather.outdoor_t)


def greenhouse_air_to_mechanical_cooling_vapor_flux(states: States, setpoints: Setpoints):
    HEC_MechAir = mechanical_cooling_to_greenhouse_air_heat_exchange_coefficient(setpoints, states)
    mechcool_vp = saturation_vapor_pressure(states.mechcool_t)
    return differentiable_air_to_obj_vapor_flux(states.air_vapor_pressure, mechcool_vp, HEC_MechAir)


def above_thermal_screen_to_internal_cover_vapor_flux(states: States):
    above_thermal_screen_t = states.above_thermal_screen_t
    internal_cov_t = states.internal_cov_t
    c_HECin = Coefficients.Construction.c_HECin
    cover_area = Coefficients.Construction.cover_area
    floor_area = Coefficients.Construction.floor_area
    HEC_TopCov_in = c_HECin * (above_thermal_screen_t - internal_cov_t) ** 0.33 * cover_area / floor_area
    cov_in_vp = saturation_vapor_pressure(internal_cov_t)
    return differentiable_air_to_obj_vapor_flux(states.above_thermal_screen_vapor_pressure, cov_in_vp, HEC_TopCov_in)


def above_thermal_screen_to_outdoor_vapor_flux(states: States, setpoints: Setpoints, weather: Weather):
    above_thermal_screen_t = states.above_thermal_screen_t
    f_TopOut = total_roof_ventilation_rates(setpoints, states, weather)
    return general_vapor_flux(f_TopOut, states.above_thermal_screen_vapor_pressure, weather.outdoor_vp,
                              above_thermal_screen_t, weather.outdoor_t)
