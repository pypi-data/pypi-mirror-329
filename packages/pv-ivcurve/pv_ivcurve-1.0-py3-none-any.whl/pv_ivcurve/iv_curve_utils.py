"""IV utils functions around the IV-curve"""
# Created by A. MATHIEU at 16/06/2022
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy.interpolate import interp1d
from pvlib.pvsystem import retrieve_sam


def dummy_mod_parameters(module_str: str = 'Hanwha_Q_CELLS_Q_PEAK_DUO_G5_SC_325'):
    """
    Get dummy module CEC model parameters.

    :return: Dictionary containing module parameters.
    """
    parameters = retrieve_sam('cecmod')[module_str].loc[
        ["alpha_sc", "a_ref", "I_L_ref", "I_o_ref", "R_sh_ref", "R_s", "Adjust"]].to_dict()
    return parameters


def iv_curve_mpp_nparray(curve: np.ndarray, iv_max: bool = False, fast=False, inv_range=None, derating=None):
    """
     Calculate the Maximum Power Point (MPP) from an IV curve.

    :param curve: (np.ndarray): A 2D NumPy array where curve[0] represents voltage (V) and curve[1] represents current (I).
    :param iv_max: If True, returns voltage and current at MPP in addition to power. Defaults to False.
    :param fast: If True, uses a simplified approach for faster computation. Defaults to False.
    :param inv_range (dict, optional): Dictionary with optional constraints:
            - "v_min": Minimum voltage constraint.
            - "v_max": Maximum voltage constraint.
            - "i_max": Maximum current constraint.
            - "p_max": Maximum power constraint.
    :param derating (float, optional): A factor (0-1) to limit power output based on maximum power found. Defaults to None.

    :return: float or tuple: If iv_max is False, returns maximum power (float).
             If iv_max is True, returns (maximum power, current at MPP, voltage at MPP).
    """
    curve_tmp = curve.copy()

    # Fast computation mode: Finds max power using simple array operations
    if fast:
        p = curve_tmp[1] * curve_tmp[0]  # Power = Voltage * Current
        p_mpp = p.max()
        if iv_max:
            if np.isnan(p_mpp):
                i_mpp, v_mpp = np.nan, np.nan
            else:
                v_mpp = curve_tmp[0][np.argmax(p)]
                i_mpp = curve_tmp[1][np.argmax(p)]
            return np.maximum(p_mpp, 0), i_mpp, v_mpp
        else:
            return np.maximum(p_mpp, 0)

    else:
        # Interpolation-based computation for more accuracy
        p = curve_tmp[1] * curve_tmp[0]
        i_interp = interp1d(curve_tmp[0], curve_tmp[1], kind='linear', fill_value="extrapolate")
        p_mpp = np.nan
        if len(curve_tmp) > 0 and (len(p) > 0):
            if (curve_tmp[0].max() > -100000):
                v_mpp_init = curve_tmp[0][np.argmax(p)]

                # Define voltage search range
                resolution = 10000
                v_min = (v_mpp_init * 0.5)
                v_max = (v_mpp_init * 1.5)
                if not inv_range is None:
                    v_min = inv_range["v_min"] if ("v_min" in inv_range.keys()) else (v_mpp_init * 0.5)
                if not inv_range is None:
                    v_max = inv_range["v_max"] if ("v_max" in inv_range.keys()) else (v_mpp_init * 1.5)
                if not inv_range is None:
                    resolution = np.maximum(resolution, int((v_max - v_min) / 0.1))

                v_index = np.linspace(v_min, v_max, resolution)
                i_index = i_interp(v_index)

                # Apply current constraints
                if not inv_range is None:
                    if ("i_max" in inv_range.keys()):
                        filter_tmp = (i_index < inv_range["i_max"])
                        i_index = i_index[filter_tmp]
                        v_index = v_index[filter_tmp]

                # Apply derating factor
                p_index = v_index * i_index
                if not derating is None:
                    filter_tmp = (p_index < (derating * p_index.max()))
                    v_index = v_index[filter_tmp]
                    p_index = p_index[filter_tmp]

                # Apply power constraints
                if not inv_range is None:
                    if "p_max" in inv_range:
                        filter_tmp = (p_index < (inv_range["p_max"]))
                        v_index = v_index[filter_tmp]
                        p_index = p_index[filter_tmp]

                # Determine max power point
                if len(p_index) > 0:
                    p_mpp = p_index.max()
                else:
                    p_mpp = np.nan
        if iv_max:
            if not np.isnan(p_mpp):
                v_mpp = v_index[np.argmax(p_index)]
                i_mpp = p_mpp / v_mpp
                return np.maximum(p_mpp, 0), i_mpp, v_mpp
            else:
                return np.nan, np.nan, np.nan
        else:
            return p_mpp


def iv_curve_voc_nparray(curve, tol=1e-5, i_lim=0.2):
    """
    Get the open-circuit voltage (Voc) from an IV curve.

    :param curve: IV-array with two columns ["v", "i"].
    :param tol: Tolerance level to identify Voc.
    :param i_lim: Current limit for Voc estimation.
    :return: Open-circuit voltage (Voc).
    """
    curve_tmp = np.array(
        [curve[0][pd.Series(curve[1]).between(-tol, +tol)], curve[1][pd.Series(curve[1]).between(-tol, +tol)]])
    if len(curve_tmp[0]) > 0:
        v_oc = curve[0][abs(curve[1]) == abs(curve[1]).min()][0]
    else:
        v_oc = iv_curve_oc_lingress_nparray(curve, i_lim, return_rs0=False)
    return v_oc


def iv_curve_oc_lingress_nparray(curve, i_lim=0.2, return_rs0=True):
    """
    Estimate the open-circuit voltage (Voc) using linear regression around the open-circuit point.

    :param curve: IV-array with two columns ["v", "i"].
    :param i_lim: Current limit for regression range.
    :param return_rs0: If True, returns series resistance estimate.
    :return: Voc (float) or (series resistance, Voc) if return_rs0 is True.
    """
    p_mpp, i_mpp, v_mpp = iv_curve_mpp_nparray(curve, True)

    curve_tmp = np.array(
        [curve[0][(curve[1] > 0) & (curve[1] < i_lim * i_mpp)], curve[1][(curve[1] > 0) & (curve[1] < i_lim * i_mpp)]])

    # Fit linear curve
    coeffs = np.polyfit(x=curve_tmp[1], y=curve_tmp[0], deg=1)  # v = coeff_1 + coeff_0 * i
    v_oc = coeffs[1]  # axis intercept

    if return_rs0:
        rs0 = - coeffs[0]  # Serial resistance 0 (not the one from the single diode model)
        return rs0, v_oc
    else:
        return v_oc


def curve_plot_nparray(curve: np.array,
                       legend: str = None,
                       show_Pmax: bool = True,
                       legendPmax: bool = True,
                       marker: bool = False,
                       positive_quadrant: bool = False,
                       color: str = None,
                       show_P: bool = False,
                       ax=None,
                       color_Pmax: str = "red"):
    """
    Plot IV curve.

    :param curve: IV-array with two columns ["v", "i"].
    :param legend: Customized legend.
    :param show_Pmax: Show the max power point?
    :param legendPmax: Add max power point to the legend?
    :param marker: Use markers?
    :param positive_quadrant: Show the positive (generator) quadrant only?
    :param color: Curve color.
    :param show_P: Show the P vs V curve.
    :param ax: Figure axis.
    :param color_Pmax: Color of the max power point.
    :return: Axis object of the plot.
    """

    fig, ax = plt.subplots() if ax is None else (None, ax)
    ax.plot(curve[0], curve[1], label=legend, marker="+" if marker else None, color=color)

    if show_P:
        ax2 = ax.twinx()
        p = curve[0] * curve[1]
        ax2.plot(curve[0], p, label="Power", marker="+" if marker else None, color="red")
        ax2.set_ylabel("Power [W]")

    if show_Pmax:
        Pmax, I_max, V_max = iv_curve_mpp_nparray(curve, iv_max=True)
        ax.plot(V_max, I_max,
                label=(legend + "-IVmpp" if (legend is not None and legendPmax) else None), linewidth=0,
                color=color_Pmax, marker="o")
        if show_P:
            ax2.plot(V_max, Pmax,
                     label=(legend + "-Pmpp" if (legend is not None and legendPmax) else None), linewidth=0,
                     color=color_Pmax, marker="o")

    plt.title("IV Curve")
    ax.set_ylabel("Intensity [A]")
    ax.set_xlabel("Voltage [V]")
    ax.legend() if legend is not None else None
    if show_P:
        ax2.legend() if legend is not None else None

    if positive_quadrant:
        filter = (curve[1] > 0) & (curve[0] > 0)
        plt.autoscale()
        plt.xlim(left=0, right=curve[0][filter].max() * 1.1)
        ax.set_ylim(bottom=0, top=curve[1][filter].max() * 1.1)
        if show_P:
            ax2.set_ylim(bottom=0, top=p.max() * 1.1)

    return ax


def combine_series2_nparray(dfs, i_min=None, i_max=None, granularity=0.01):
    """
    Combine IV curves in series by aligning currents and summing voltages.
    Version 2.

    :param dfs: List of IV curves.
    :param i_min: Minimum current range.
    :param i_max: Maximum current range.
    :param granularity: Step size for interpolation.

    :return: Combined IV curve.
    """

    if i_min is None and i_max is None:
        i_min = 0
        i_max = 0.1
        for df in dfs:
            i_min = df[0].min() if i_min > df[0].min() else i_min
            i_max = df[0].max() if i_max < df[0].max() else i_max

    i_index = np.arange(i_min, i_max, granularity)
    values = [0] * len(i_index)
    j = 0

    # df_all=pd.DataFrame(index=i_index)
    for df in dfs:
        i_interp = interp1d(df[1], df[0], kind='linear', fill_value="extrapolate")
        values += i_interp(i_index)
        j += 1
        # print(i_interp(0))
    #     df_all[j] =  i_interp(i_index)
    #
    # plt.plot(df_all.iloc[:, 0], i_index, marker=".")
    # plt.plot(df_all.iloc[:, 1], i_index, marker=".")
    iv_all = np.array([values, i_index])

    return iv_all


def combine_parallel2_nparray(dfs, v_min=None, v_max=None, granularity=0.01, n_points=1000):
    """
    Combine IV curves in parallel by aligning voltages and summing currents.
    Version 2.

    :param dfs: List of IV curves.
    :param v_min: Minimum voltage range.
    :param v_max: Maximum voltage range.
    :param granularity: Step size for interpolation.
    :param n_points: Number of points in interpolation.

    :return: Combined IV curve.
    """

    if len(dfs) > 1:
        if v_min is None and v_max is None:
            v_min = 0
            v_max = 0.1
            for df in dfs:
                v_min = df[0].min() if v_min > df[0].min() else v_min
                v_max = df[0].max() if v_max < df[0].max() else v_max

        v_index = np.linspace(v_min, v_max, n_points)
        v_index = (v_index / granularity).round() * granularity
        v_index = np.unique(v_index)
        values = [0] * len(v_index)
        iv_all = np.array([v_index, values])

        for df in dfs:
            if ((df[0] * df[1]) > 0).any():
                i_interp = interp1d(df[0], df[1], kind='linear', fill_value="extrapolate")
                values += i_interp(v_index)
        iv_all[1] = values

    else:
        iv_all = dfs[0]

    return iv_all


def add_diode(iv_curve, voltage=-0.5, granularity=0.01):
    """
    Add a diode effect to an IV curve.

    :param iv_curve: IV-array with two columns ["v", "i"].
    :param voltage: Diode activation voltage.
    :param granularity: Step size for interpolation.
    :return: Modified IV curve with diode effect.
    """

    iv_curve = np.array([iv_curve[0][iv_curve[0].argsort()], iv_curve[1][iv_curve[0].argsort()]])

    iv_curve = np.array([np.array(iv_curve[0][iv_curve[0] > voltage]), np.array(iv_curve[1][iv_curve[0] > voltage])])

    # Voltage
    if len(iv_curve[1]) > 0:
        iv_curve = np.array(
            [np.append(voltage - granularity, iv_curve[0]), np.append(+ iv_curve[1][0] + granularity, iv_curve[1])])
        iv_curve = np.array(
            [np.append(voltage - 2 * granularity, iv_curve[0]), np.append(+1e10, iv_curve[1])])

    else:
        v_array = np.array([voltage - 2 * granularity, voltage - granularity, 0.6 * 120])
        i_array = np.array([+1e10, 0, -granularity])
        iv_curve = np.array([v_array, i_array])
    return iv_curve
