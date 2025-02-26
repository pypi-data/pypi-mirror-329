"""Functions to calculate current/voltage characteristics of a PV module from environmental data (effective irradiance and cell temperature)"""
# Created by A. MATHIEU at 08/05/2022
import pandas as pd
import numpy as np

from copy import deepcopy
from tqdm import tqdm
from typing import Union
from pvlib import pvsystem

from pv_ivcurve.iv_curve_utils import curve_plot_nparray, iv_curve_mpp_nparray, iv_curve_voc_nparray, \
    dummy_mod_parameters
from pv_ivcurve.iv_degradation import aging_regressors


def clean_iv(vi_curve: np.ndarray) -> np.ndarray:
    """
    Make sure they are unique current values in the IV curve.
    Keep only the highest current duplicates to correctly calculate the maximum power point.

    :param vi_curve: np.ndarray:
        vi_curve[0]: Voltage [V]
        vi_curve[1]: Current [A]
    :param iv_granularity: Granularity Voltage/Current of the IV curve

    :return: vi_curve with unique current indices
    """
    first_line = np.array([vi_curve[0][0], vi_curve[1][0]])

    # Get the voltages/current from the highest to the lowest to use the np.unique function
    # that gets the unique current indices with the highest values (when flipped only)
    v_inversed = np.flip(vi_curve[0])
    i_inversed = np.flip(vi_curve[1])
    _, unique_idx = np.unique(i_inversed, axis=0, return_index=True)

    # Keep the first line and add the rest "unique" IV-curve
    vi_curve = np.array([np.append(np.array([first_line[0]]), np.flip(v_inversed[np.sort(unique_idx)])[1:]),
                         np.append(np.array([first_line[1]]), np.flip(i_inversed[np.sort(unique_idx)])[1:])])

    return vi_curve


def iv_quick_instant(irr_eff_dt: float,
                     temp_cell_dt: float,
                     params: dict,
                     v_index: np.ndarray,
                     iv_granularity: float = 0.01,
                     EgRef: float = 1.121,
                     dEgdT: float = -0.0002677,
                     clean: bool = True) -> np.ndarray:
    """
    Generates the IV curve from the CEC model for given irradiance and temperature.

    :param irr_eff_dt (float): Effective irradiance at the given timestamp.
    :param temp_cell_dt (float): Cell temperature at the given timestamp.
    :param params (dict): Dictionary of photovoltaic system parameters.
    :param v_index (numpy.ndarray): Voltage values for which current is calculated.
    :param iv_granularity (float, optional): Granularity for rounding the current values. Default is 0.01.
    :param EgRef (float, optional): Reference bandgap energy. Default is 1.121 eV for silicon.
    :param dEgdT: (float, optional): Temperature coefficient for bandgap energy. Default is -0.0002677 eV/K for silicon.
    :param clean: (bool, optional): Whether to clean the IV curve using `clean_iv` function. Default is True.

    :return: numpy.ndarray: A 2D array representing the voltage-current (VI) curve.
            vi_curve[0]: Voltage [V]
            vi_curve[1]: Current [A]
    """

    # Calculate Single Diode parameters
    IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_cec(irr_eff_dt, temp_cell_dt, **params, EgRef=EgRef, dEgdT=dEgdT)

    # Generate I according to V
    i = pvsystem.i_from_v(v_index, IL, I0, Rs, Rsh, nNsVth)

    # Round to IV-granularity
    i_pred = (i / iv_granularity).astype(float).round() * iv_granularity

    # Build up the VI-curve
    vi_curve = np.array([v_index, i_pred])

    if clean:
        vi_curve = clean_iv(vi_curve)

    return vi_curve


def iv_quick(irr_eff: pd.Series,
             temp_cell: pd.Series,
             stc_params: dict,
             iv_granularity: float = 0.01,
             EgRef: float = 1.121,
             dEgdT: float = -0.0002677,
             print_bool: bool = False,
             derating: Union[None, pd.Series, float] = None,
             derating_dc: Union[None, float] = None,
             rs_plus_derating: Union[None, pd.Series] = None,
             pos: bool = True):
    """
    Generates IV curves over the two time series of irradiance and temperature data. They should have the same index

    :param irr_eff (pandas.Series): Time-series effective irradiance data.
    :param temp_cell (pandas.Series): Time-series cell temperature data.
    :param stc_params (dict): Standard test condition parameters. Expect 6 keys:

    :param iv_granularity (float, optional): Granularity for minimum IV curve voltage/current steps. Default is 0.01.
    :param EgRef (float, optional): Reference bandgap energy. Default is 1.121 eV for silicon.
    :param dEgdT: (float, optional): Temperature coefficient for bandgap energy. Default is -0.0002677 eV/K for silicon.
    :param print_bool (bool, optional): Whether to print progress using tqdm. Default is False.
    :param derating (float or pandas.Series, optional): Aging-related derating factors. Default is None.
    :param derating_dc (float, optional): Derating factor for DC power. Default value corresponds to 2.3 % DC losses.
    :param rs_plus_derating: (float or pandas.Series, optional): Additional derating for series resistance (from corrosion). Default is None.
    :param pos (bool, optional): Whether to filter out non-positive irradiance values. Default is True.

    :return: A dictionary where keys are timestamps and values are IV curves as 2D numpy arrays.
    """

    # Calculate the Voc to later adapt the voltage index (to save computation time)
    vi_curve_stc = iv_quick_instant(1000, 25, stc_params, np.arange(-1, 200, 0.001), iv_granularity=iv_granularity,
                                    EgRef=EgRef, dEgdT=dEgdT)
    v_oc = iv_curve_voc_nparray(vi_curve_stc)

    # Prepare the recipients
    irr_eff_pos = irr_eff[irr_eff > 0] if pos else irr_eff
    vi_curves = {dt: None for dt in irr_eff_pos.index}

    # Calculate the derating factors due to aging/dc loss/corrosion
    rs_factors, rsh_factors, il_factors, rs_plus_derating_ts = \
        derating_factors(irr_eff_pos.index, stc_params, derating_dc, EgRef, dEgdT, derating, rs_plus_derating)

    for dt in tqdm(irr_eff_pos.index, disable=(len(irr_eff.index) < 1000) or (not print_bool),
                   desc="Generate IV curves"):
        # Prepare v_index
        irr_eff_dt = irr_eff.loc[dt]
        temp_cell_dt = temp_cell.loc[dt] if not np.isnan(temp_cell.loc[dt]) else 25
        v_oc_rel = v_oc * (1 - 0.5 / 100 * (temp_cell_dt - 25)) * 1.1
        v_index = np.arange(-1, v_oc_rel, iv_granularity).round(4)

        # Prepare the correct stc params according to aging ("derating")
        stc_params_aged = deepcopy(stc_params)
        if not derating is None:
            stc_params_aged["R_s"] = stc_params["R_s"] * rs_factors.loc[dt]
            stc_params_aged["R_sh_ref"] = stc_params["R_sh_ref"] * rsh_factors.loc[dt]
            stc_params_aged["I_L_ref"] = stc_params["I_L_ref"] * il_factors.loc[dt]
        if not rs_plus_derating is None:
            stc_params_aged["R_s"] += stc_params["R_s"] * (1 - rs_plus_derating.loc[dt])

        # Generate IV curve and store it
        vi_curve = iv_quick_instant(irr_eff_dt, temp_cell_dt, stc_params_aged, v_index, iv_granularity=iv_granularity)
        vi_curves[dt] = vi_curve

    return vi_curves


def derating_factors(index: pd.DatetimeIndex,
                     stc_params: dict,
                     derating_dc: Union[pd.Series, float] = 1 - 2.3 / 100,
                     EgRef: float = 1.121,
                     dEgdT: float = -0.0002677,
                     derating: Union[None, pd.Series, float] = None,
                     rs_plus_derating: Union[None, pd.Series] = None):
    """
    Computes derating factors for series resistance, shunt resistance, and photocurrent.

    :param index (pandas.Index): Index for time-series data.
    :param stc_params (dict): Standard test condition parameters.
    :param derating_dc (float, optional): Default derating factor for DC power. Default value corresponds to 2.3 % DC losses.
    :param EgRef (float, optional): Reference bandgap energy. Default is 1.121 eV for silicon.
    :param dEgdT: (float, optional): Temperature coefficient for bandgap energy. Default is -0.0002677 eV/K for silicon.
    :param derating: (float or pandas.Series, optional): Aging-related derating factors. Default is None.
    :param rs_plus_derating: (float or pandas.Series, optional): Additional derating for series resistance (from corrosion). Default is None.

    :return:  uple: (rs_factors, rsh_factors, il_factors, rs_plus_derating_ts)
        - rs_factors (pandas.Series): Scaling factors for series resistance.
        - rsh_factors (pandas.Series): Scaling factors for shunt resistance.
        - il_factors (pandas.Series): Scaling factors for photocurrent.
        - rs_plus_derating_ts (pandas.Series): Additional derating factors for series resistance. (from corrosion)

    """

    rs_factors = pd.Series(index=index, data=1)
    rsh_factors = pd.Series(index=index, data=1)
    il_factors = pd.Series(index=index, data=1)

    # If there is derating, calculate the rs/rsh/il factors.
    if (not derating is None) and (derating_dc != 1):
        # If a pd.Series is provided, calculate the derating factors over the whole time range.
        if type(derating) is pd.Series:
            rs_regr, rsh_regr, il_regr = aging_regressors(stc_params, EgRef, dEgdT, derating_dc=derating_dc)
            rs_factors = rs_regr(derating).fillna(1)
            rsh_factors = rsh_regr(derating).fillna(1)
            il_factors = il_regr(derating).fillna(1)

        # If a float is provided, calculate the derating one and applies the same values over the whole time range.
        elif type(derating) is float:
            if derating != 1:
                derating_ts = pd.Series(index=index, data=derating)
                rs_regr, rsh_regr, il_regr = aging_regressors(stc_params, EgRef, dEgdT, derating_dc=derating_dc)
                rs_factors = rs_regr(derating_ts).fillna(1)
                rsh_factors = rsh_regr(derating_ts).fillna(1)
                il_factors = il_regr(derating_ts).fillna(1)

    # Calculate addition rs derating if not None
    rs_plus_derating_ts = pd.Series(index=index, data=1)
    if not rs_plus_derating is None:
        if type(rs_plus_derating) is float:
            if rs_plus_derating != 1:
                rs_plus_derating_ts = pd.Series(index=index, data=rs_plus_derating)

    return rs_factors, rsh_factors, il_factors, rs_plus_derating_ts


if __name__ == "__main__":
    # Soiling cleaning effect example
    pv_params = dummy_mod_parameters()
    v_index = np.arange(-1, 45, 0.01)
    vi_curve = iv_quick_instant(600, 15, pv_params, v_index)
    vi_curve2 = iv_quick_instant(600 * 1.04, 15, pv_params, v_index)
    vi_curve3 = iv_quick_instant(600 * 1.04, 15 + 2, pv_params, v_index)

    plot_bool = False
    if plot_bool:
        ax = curve_plot_nparray(vi_curve, legend="Before cleaning", positive_quadrant=True)
        curve_plot_nparray(vi_curve2, legend="After cleaning with optical gain [4%]", positive_quadrant=True, ax=ax)
        curve_plot_nparray(vi_curve3, legend="After cleaning, including heating effect [+2°C]", positive_quadrant=True,
                           ax=ax)

        iv_curve_mpp_nparray(vi_curve, True)
        iv_curve_mpp_nparray(vi_curve2, True)
        iv_curve_mpp_nparray(vi_curve3, True)
