"""Functions to account for degradation on IV curves (over time)"""
# Created by A. MATHIEU at 29/08/2023
import datetime
import os.path
import pandas as pd
import numpy as np
import warnings

import functools
import matplotlib.pyplot as plt

from copy import deepcopy
from tqdm import tqdm
from typing import Union
from scipy.optimize import curve_fit
from scipy.optimize import least_squares
from pvlib.pvsystem import max_power_point

from pv_ivcurve.config import DATA_PATH
from pv_ivcurve.iv_curve_utils import curve_plot_nparray, iv_curve_mpp_nparray, dummy_mod_parameters


def hourly_ageing(index: pd.DatetimeIndex,
                  start: Union[datetime.datetime, pd.Timestamp],
                  ageing_rate: float):
    """
    Compute the ageing degradation over time (positive values correspond to a degradation).

    :param index (pd.DatetimeIndex): Time index.
    :param start (datetime): The reference start date from which applying the aging rates.
    :param ageing_rate (float or list): Ageing rate in percentage per year.

    :return: pd.Series or pd.DataFrame: Computed ageing values.
    """
    difference_in_days = (index - start).days
    if type(ageing_rate) == float:
        ageing = difference_in_days / 365.25 * ageing_rate / 100
        ageing = pd.Series(ageing, index=index)
    elif type(ageing_rate) == list:
        ageing = np.array([difference_in_days / 365]).reshape(-1, 1) * np.array(ageing_rate).reshape(1, -1) / 100
        ageing = pd.DataFrame(ageing, index=index)

    return ageing


def get_max_mpp(rs, rsh, il, io, aref):
    """
    Compute the maximum power point (MPP) parameters.

    :param rs (float): Series resistance.
    :param rsh (float): Shunt resistance.
    :param il (float): Light-generated current.
    :param io (float): Diode saturation current.
    :param aref (float): Diode ideality factor.

    :return: tuple: (pmpp, impp, vmpp) - Maximum power, current, and voltage.
    """
    dict_mp = max_power_point(il, io, rs, rsh, aref)
    pmpp = dict_mp["p_mp"]
    impp = dict_mp["i_mp"]
    vmpp = dict_mp["v_mp"]

    return pmpp, impp, vmpp


def find_rs_rsh_il_derating_v3(stc_params, derating: float = 0.8, derating_dc: float = (1 - 2.3 / 100)):
    """
    Estimate the series resistance (Rs), shunt resistance (Rsh), and light-generated current (IL) under derating conditions.
    Version 3.

    [PhD. Manuscript A. MATHIEU 2025]
    The degradation reflects a power loss and, at the module level, appear to be mostly driven by
    a loss in Isc, short-circuit current and FF, fill factor from outdoor conditioning according to a
    study in India [1]. When looking at the median degradation rates reported worldwide
    [2], mono-Si, multi-Si and thin films have their open-circuit current Isc degradation
    rate which corresponds to roughly 75% of the total Pmax degradation, ie if Pmax has a
    degradation of 1%/year, the Isc has a degradation of 0.75%/year.

    References:
        [1] Vikrant Sharma et al. “Degradation analysis of a-Si, (HIT) hetro-junction intrinsic
        thin layer silicon and m-C-Si solar photovoltaic technologies under outdoor
        conditions”. In: Energy 72 (2014), pp. 536–546.
        [2] D Jordan, J Wohlgemuth, and Sarah Kurtz. “Technology and Climate Trends in PV
        Module Degradation”. In: Proceedings of the 27th European Photovoltaic Solar
        Energy Conference and Exhibition. Jan. 2012, pp. 3118–3124.

    :param stc_params (dict): Standard Test Conditions (STC) parameters of the PV module.
    :param derating (float, optional): Aging derating factor (default: 0.8).
    :param derating_dc (float, optional): DC derating factor (default: 1 - 2.3/100). Corresponds to 2.3% of DC loss at STC conditions.

    :return: tuple: Adjusted Rs scaling factor, 1 / adjusted Rs scaling factor, IL scaling factor.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        params = deepcopy(stc_params)
        rs0 = stc_params["R_s"]
        rsh0 = stc_params["R_sh_ref"]
        il0 = stc_params["I_L_ref"]

        # Calculate initial maximum power point under STC
        pmpp_stc, impp_stc, vmpp_stc = get_max_mpp(stc_params["R_s"], stc_params["R_sh_ref"], stc_params["I_L_ref"],
                                                   stc_params["I_o_ref"], stc_params["a_ref"])

        # Compute the combined derating factor
        derating_tot = 1 - ((1 - derating) + (1 - derating_dc))
        pmpp_aging_and_dc = pmpp_stc * derating_tot

        def func(alpha):
            """Objective function to minimize the deviation from the expected aged power output."""
            params["R_s"] = rs0 * alpha[0]
            params["R_sh_ref"] = rsh0 / alpha[0]
            params["I_L_ref"] = il0 * (1 - (1 - derating) * 0.75)

            pmpp, impp, vmpp = get_max_mpp(params["R_s"], params["R_sh_ref"], params["I_L_ref"], params["I_o_ref"],
                                           params["a_ref"])

            # Metric to minimize
            ind1 = ((pmpp - pmpp_aging_and_dc) / pmpp_stc * 100)

            return ((ind1) ** 2)

        alpha_rs_init = 1 + (1 - derating) / 0.2
        res = least_squares(func, x0=[alpha_rs_init], bounds=[[0], [np.inf]], tr_options={"tol": 1e-5})

        return res.x[0], 1 / res.x[0], (1 - (1 - derating) * 0.75)


def model_x3_v3(x, coeff1, coeff2, coeff3, coeff4):
    """Cubic polynomial model for aging regressions."""

    return coeff1 * (x) + coeff2 * (x) ** 2 + coeff3 * (x) ** 3 + coeff4


def get_partial_functions(best_fit_rs, best_fit_rsh, best_fit_il):
    """
    Generate partial functions for Rs, Rsh, and Il using the polynomial model_x3_v3 function.

    :param best_fit_rs (list): Coefficients for Rs regression model.
    :param  best_fit_rsh (list): Coefficients for Rsh regression model.
    :param best_fit_il (list): Coefficients for Il regression model.

    :return: tuple: Partial functions for Rs, Rsh, and Il.
    """
    partial_model_x3 = functools.partial(model_x3_v3)
    partial_model_rs = functools.partial(partial_model_x3, coeff1=best_fit_rs[0], coeff2=best_fit_rs[1],
                                         coeff3=best_fit_rs[2], coeff4=best_fit_rs[3])
    partial_model_rsh = functools.partial(partial_model_x3, coeff1=best_fit_rsh[0], coeff2=best_fit_rsh[1],
                                          coeff3=best_fit_rsh[2], coeff4=best_fit_rsh[3])
    partial_model_il = functools.partial(partial_model_x3, coeff1=best_fit_il[0], coeff2=best_fit_il[1],
                                         coeff3=best_fit_il[2], coeff4=best_fit_il[3])

    return partial_model_rs, partial_model_rsh, partial_model_il


def plot_derating_fit(rs, rsh, il, derating_idx, best_fit_rs, best_fit_rsh, best_fit_il, derating_dc):
    """
    Plot the derating fit curves for Rs, Rsh, and Il, along with their regression models.

    :param rs (pd.Series): Series of Rs values.
    :param rsh (pd.Series): Series of Rsh values.
    :param il (pd.Series): Series of Il values.
    :param derating_idx (numpy.ndarray): Array of derating index values.
    :param best_fit_rs (list): Coefficients for Rs regression model.
    :param best_fit_rsh (list): Coefficients for Rsh regression model.
    :param best_fit_il (list): Coefficients for Il regression model.
    :param derating_dc (float): Derating factor for DC degradation.

    :return: None
    """

    partial_model_rs, partial_model_rsh, partial_model_il = get_partial_functions(best_fit_rs, best_fit_rsh,
                                                                                  best_fit_il)

    plt.figure()
    rs.plot(marker=".", linewidth=0, label="rs", color="blue")
    rsh.plot(marker=".", linewidth=0, label="rsh", color="green")
    il.plot(marker=".", linewidth=0, label="il", color="red")

    plt.plot(derating_idx, partial_model_rs(derating_idx), color="darkblue", label="rs-regressed")
    plt.plot(derating_idx, partial_model_rsh(derating_idx), color="darkgreen", label="rsh-regressed")
    plt.plot(derating_idx, partial_model_il(derating_idx), color="darkred", label="il-regressed")

    pmpp_stc, impp_stc, vmpp_stc = get_max_mpp(stc_params["R_s"], stc_params["R_sh_ref"], stc_params["I_L_ref"],
                                               stc_params["I_o_ref"], stc_params["a_ref"])
    pmpp_ts = pd.Series(dtype=float)
    ind4 = pd.Series(dtype=float)
    for idx in np.arange(0.3, 1.2 - 1e-10, 0.001):
        pmpp_ts.loc[idx], impp, vmpp = get_max_mpp(partial_model_rs(idx) * stc_params["R_s"],
                                                   np.clip(partial_model_rsh(idx) * stc_params["R_sh_ref"],
                                                           0.01, 10000),
                                                   partial_model_il(idx) * stc_params["I_L_ref"],
                                                   stc_params["I_o_ref"],
                                                   stc_params["a_ref"])
        ind2 = (impp - impp_stc) / impp_stc * 100
        ind3 = (vmpp - vmpp_stc) / vmpp_stc * 100
        ind4.loc[idx] = (abs(ind2) / 4 - abs(ind3))

    pmpp_ts = pmpp_ts / pmpp_stc + (1 - derating_dc)

    pmpp_ts.plot(color="black", marker="o", label="p_ratio")
    plt.plot(derating_idx, derating_idx, color="grey")

    ind4.plot(color="purple", marker="o", label="i_v_loss_ratio")

    return None


def aging_regressors(stc_params: dict,
                     EgRef: float = 1.121,
                     dEgdT: float = -0.0002677,
                     store_pkl: bool = True,
                     overwrite: bool = False,
                     derating_dc: float = 1 - 2.3 / 100,
                     plot_bool: bool = False):
    """
    Get the regression models for aging effects on Rs, Rsh, and IL.

    :param stc_params (dict): STC parameters of the PV module.
    :param EgRef (float, optional): Reference bandgap energy (default: 1.121 eV).
    :param dEgdT (float, optional): Temperature coefficient for bandgap energy (default: -0.0002677 eV/K).
    :param store_pkl (bool, optional): Whether to store computed regressors as a pickle file (default: True).
    :param overwrite (bool, optional): Whether to overwrite existing files (default: False).
    :param derating_dc (float, optional): DC derating factor (default: 1 - 2.3/100). Corresponding to 2.3% of DC losses.
    :param plot_bool: (bool, optional): Whether to plot regression results (default: False).

    :return: Partial functions for Rs, Rsh, and IL aging regressions.
    """

    suffix = f"{stc_params['alpha_sc']:.2e}_{stc_params['a_ref']:.2e}_{stc_params['I_L_ref']:.2e}_" \
             f"{stc_params['I_o_ref']:.2e}_{stc_params['R_sh_ref']:.2e}_{stc_params['R_s']:.2e}_" \
             f"{stc_params['Adjust'] if ('Adjust' in stc_params.keys()) else 0:.2e}_" \
             f"{EgRef:.2e}_{dEgdT:.2e}_v3_derating{round(derating_dc, 3)}"
    path_store = str(DATA_PATH / "power_model_regressors" / f"regressor_aging_{suffix}.pkl")

    if (store_pkl) & os.path.exists(path_store) & (not overwrite):
        df = pd.read_pickle(path_store)

        best_fit_rs = df["rs"].values
        best_fit_rsh = df["rsh"].values
        best_fit_il = df["il"].values

        partial_model_rs, partial_model_rsh, partial_model_il = \
            get_partial_functions(best_fit_rs, best_fit_rsh, best_fit_il)

    else:
        derating_idx = np.arange(0.3, 1.2, 0.01)

        rs = pd.Series(index=derating_idx, dtype=float)
        rsh = pd.Series(index=derating_idx, dtype=float)
        il = pd.Series(index=derating_idx, dtype=float)
        for d in tqdm(derating_idx, desc="Estimate aging regressors"):
            rs.loc[d], rsh.loc[d], il.loc[d] = find_rs_rsh_il_derating_v3(stc_params, d, derating_dc)

        rs = rs.dropna()
        rsh = rsh.dropna()
        rsh = rsh[rsh < 5]
        il = il.dropna()

        partial_model_x3 = functools.partial(model_x3_v3)
        best_fit_rs, _ = curve_fit(partial_model_x3, rs.index, rs)
        best_fit_rsh, _ = curve_fit(partial_model_x3, rsh.index, rsh)
        best_fit_il, _ = curve_fit(partial_model_x3, il.index, il)

        partial_model_rs, partial_model_rsh, partial_model_il = \
            get_partial_functions(best_fit_rs, best_fit_rsh, best_fit_il)

        if store_pkl:
            df = pd.DataFrame(index=range(len(best_fit_rsh)))
            df["rs"] = best_fit_rs
            df["rsh"] = best_fit_rsh
            df["il"] = best_fit_il
            df.to_pickle(path_store)

        if plot_bool:
            _ = plot_derating_fit(rs, rsh, il, derating_idx, best_fit_rs, best_fit_rsh, best_fit_il, derating_dc)

    return partial_model_rs, partial_model_rsh, partial_model_il


if __name__ == "__main__":
    """Plot to illustrate aging and DC losses on IV curves"""
    plot_bool = False

    # The import is here for the illustration only, otherwise circular import
    from pv_ivcurve.iv_model import iv_quick_instant

    stc_params = dummy_mod_parameters("Hanwha_Q_CELLS_Q_PEAK_DUO_BLK_G5_300")
    v_index = np.arange(-1, 40 * 1.3, 0.01)

    rs_regr, rsh_regr, il_regr = aging_regressors(stc_params, derating_dc=1)
    rs_factors = rs_regr(pd.Series(data=[1, 0.9])).fillna(1)
    rsh_factors = rsh_regr(pd.Series(data=[1, 0.9])).fillna(1)
    il_factors = il_regr(pd.Series(data=[1, 0.9])).fillna(1)

    rs_regr, rsh_regr, il_regr = aging_regressors(stc_params, derating_dc=(1 - 2.3 / 100))
    rs_factors_derating = rs_regr(pd.Series(data=[1, 0.9])).fillna(1)
    rsh_factors_derating = rsh_regr(pd.Series(data=[1, 0.9])).fillna(1)
    il_factors_derating = il_regr(pd.Series(data=[1, 0.9])).fillna(1)

    stc_params_aged = stc_params.copy()
    # Prepare the correct stc params according to aging ("derating")
    stc_params_aged["R_s"] = stc_params["R_s"] * rs_factors.loc[1]
    stc_params_aged["R_sh_ref"] = stc_params["R_sh_ref"] * rsh_factors.loc[1]
    stc_params_aged["I_L_ref"] = stc_params["I_L_ref"] * il_factors.loc[1]

    stc_params_aged_dc = stc_params.copy()
    stc_params_aged_dc["R_s"] = stc_params["R_s"] * rs_factors_derating.loc[1]
    stc_params_aged_dc["R_sh_ref"] = stc_params["R_sh_ref"] * rsh_factors_derating.loc[1]
    stc_params_aged_dc["I_L_ref"] = stc_params["I_L_ref"] * il_factors_derating.loc[1]

    vi_curve_stc = iv_quick_instant(1000, 25, stc_params, v_index, iv_granularity=0.01)
    vi_curve_aged = iv_quick_instant(1000, 25, stc_params_aged, v_index, iv_granularity=0.01)
    vi_curve_aged_dc = iv_quick_instant(1000, 25, stc_params_aged_dc, v_index, iv_granularity=0.01)

    ax = curve_plot_nparray(vi_curve_stc, legend=f"STC curve, Pmax={round(iv_curve_mpp_nparray(vi_curve_stc))} W",
                            color="darkred", show_Pmax=True, legendPmax=False)
    ax = curve_plot_nparray(vi_curve_aged,
                            legend=f"STC curve with aging (10% loss), Pmax={round(iv_curve_mpp_nparray(vi_curve_aged))} W",
                            ax=ax,
                            show_Pmax=True, legendPmax=False)
    ax = curve_plot_nparray(vi_curve_aged_dc,
                            legend=f"STC curve with aging and DC loss (12.3% loss), Pmax={round(iv_curve_mpp_nparray(vi_curve_aged_dc))} W",
                            ax=ax, show_Pmax=True, legendPmax=False)
    plt.ylim([0, 11])
    plt.xlim([0, 41])
    plt.legend(loc="lower left")
    plt.tight_layout()

    rs_regr, rsh_regr, il_regr = aging_regressors(stc_params, derating_dc=1)
    rs_factors = rs_regr(pd.Series(data=[1, 0.9, 0.8])).fillna(1)
    rsh_factors = rsh_regr(pd.Series(data=[1, 0.9, 0.8])).fillna(1)
    il_factors = il_regr(pd.Series(data=[1, 0.9, 0.8])).fillna(1)

    stc_params_aged_20 = stc_params.copy()
    # Prepare the correct stc params according to aging ("derating")
    stc_params_aged_20["R_s"] = stc_params["R_s"] * rs_factors.loc[2]
    stc_params_aged_20["R_sh_ref"] = stc_params["R_sh_ref"] * rsh_factors.loc[2]
    stc_params_aged_20["I_L_ref"] = stc_params["I_L_ref"] * il_factors.loc[2]

    vi_curve_aged_20 = iv_quick_instant(1000, 25, stc_params_aged_20, v_index, iv_granularity=0.01)

    ax = curve_plot_nparray(vi_curve_stc, legend=f"STC curve, Pmax={round(iv_curve_mpp_nparray(vi_curve_stc))} W",
                            color="darkred", show_Pmax=True, legendPmax=False)
    ax = curve_plot_nparray(vi_curve_aged,
                            legend=f"STC curve with 10%-loss due to aging, "
                                   f"Pmax={round(iv_curve_mpp_nparray(vi_curve_aged))} W",
                            ax=ax, show_Pmax=True, legendPmax=False)
    ax = curve_plot_nparray(vi_curve_aged_20, legend=f"STC curve with 20%-loss due to aging, "
                                                     f"Pmax={round(iv_curve_mpp_nparray(vi_curve_aged_20))} W",
                            ax=ax, show_Pmax=True, legendPmax=False)
    plt.ylim([0, 11])
    plt.xlim([0, 41])
    plt.legend(loc="lower left")
    plt.tight_layout()
