from . import dnpdata as _dnpdata, dnpdata_collection
import numpy as _np
from scipy.optimize import curve_fit


def t1_function(t_axis, T1, M_0, M_inf):
    return M_0 - M_inf * _np.exp(-1.0 * t_axis / T1)


def t2_function_stretch(x_axis, M_0, T2, p):
    return M_0 * _np.exp(-2.0 * (x_axis / T2) ** p)


def t2_function_nostretch(x_axis, M_0, T2):
    return M_0 * _np.exp(-2.0 * (x_axis / T2) ** 1.0)


def exp_fit_func_1(x_axis, C1, C2, tau):
    return C1 + C2 * _np.exp(-1.0 * x_axis / tau)


def exp_fit_func_2(x_axis, C1, C2, tau1, C3, tau2):
    return C1 + C2 * _np.exp(-1.0 * x_axis / tau1) + C3 * _np.exp(-1.0 * x_axis / tau2)


def exponentialFit(all_data, type="mono", stretched=False, dim="t2"):
    """Fits various forms of exponential functions

    .. math::

        f(t) = M_0 - M_{\infty} e^{-t/T_1}
        f(t) = M_0 e^{(-2(t/T_2)^p}
        f(t) = M_0 e^{(-2(t/T_2)}
        f(t) = C1 + C2 e^{-x/tau}
        f(t) = C1 + C2 e^{-x/tau1} + C3 e^{-x/tau2}

    Args:
        all_data (dnpdata, dict): data container after processing inversion recovery data, after integration with dnpNMR.integrate
        type (str) : "T1" for inversion recovery fit, "T2" for stretched exponential, "mono", or "bi"
        stretch (boolean) : if False "p" is set to 1, if True "p" is a fit parameter
        dim (str) : dimension to fit down

    Returns:
        dnpdata_collection or dnpdata: Processed data in container, updated with fit data
        attributes: "T1" value and "T1_stdd" standard deviation for type="T1", "T2" value and "T2_stdd" standard deviation for type="T2", or "tau" and "tau_stdd" for type="mono", "tau1", "tau1_stdd", "tau2", and "tau2_stdd" for type="bi"

    """

    isDict = False
    if isinstance(all_data, (dict, dnpdata_collection)):
        data = all_data["proc"].copy()
        isDict = True
    elif isinstance(all_data, dnpdata):
        data = all_data.copy()
    else:
        raise TypeError("Invalid data")

    if dim == "t2":
        ind_dim = "t1"
    elif dim == "t1":
        ind_dim = "t2"

    x_axis = data.coords[ind_dim]
    new_axis = _np.r_[_np.min(x_axis) : _np.max(x_axis) : 100j]
    inputData = _np.real(data.values)

    if type == "T1":

        x0 = [1.0, inputData[-1], inputData[-1]]
        out, cov = curve_fit(t1_function, x_axis, inputData, x0, method="lm")
        stdd = _np.sqrt(_np.diag(cov))
        fit = t1_function(new_axis, out[0], out[1], out[2])

        fitData = _dnpdata(fit, [new_axis], [ind_dim])
        fitData.attrs["T1"] = out[0]
        fitData.attrs["T1_stdd"] = stdd[0]
        fitData.attrs["M_0"] = out[1]
        fitData.attrs["M_inf"] = out[2]

    elif type == "T2":

        if stretched:
            x0 = [inputData[0], 1.0, 1.0]
            out, cov = curve_fit(t2_function_stretch, x_axis, inputData, x0, method="lm")
            stdd = _np.sqrt(_np.diag(cov))
            fit = t2_function_stretch(new_axis, out[0], out[1], out[2])
        else:
            x0 = [inputData[0], 1.0]
            out, cov = curve_fit(t2_function_nostretch, x_axis, inputData, x0, method="lm")
            stdd = _np.sqrt(_np.diag(cov))
            fit = t2_function_nostretch(new_axis, out[0], out[1])

        fitData = _dnpdata(fit, [new_axis], [ind_dim])
        fitData.attrs["T2"] = out[1]
        fitData.attrs["T2_stdd"] = stdd[1]
        fitData.attrs["M_0"] = out[0]
        if stretched:
            fitData.attrs["p"] = out[2]

    elif type == "mono":

        x0 = [inputData[-1], 1.0, 100]
        out, cov = curve_fit(exp_fit_func_1, x_axis, inputData, x0, method="lm")
        stdd = _np.sqrt(_np.diag(cov))
        fit = exp_fit_func_1(new_axis, out[0], out[1], out[2])

        fitData = _dnpdata(fit, [new_axis], [ind_dim])
        fitData.attrs["tau"] = out[2]
        fitData.attrs["tau_stdd"] = stdd[2]
        fitData.attrs["C1"] = out[0]
        fitData.attrs["C2"] = out[1]

    elif type == "bi":

        x0 = [inputData[-1], 1.0, 100, 1.0, 100]
        out, cov = curve_fit(exp_fit_func_2, x_axis, inputData, x0, method="lm")
        stdd = _np.sqrt(_np.diag(cov))
        fit = exp_fit_func_2(new_axis, out[0], out[1], out[2], out[3], out[4])

        fitData = _dnpdata(fit, [new_axis], [ind_dim])
        fitData.attrs["tau1"] = out[2]
        fitData.attrs["tau1_stdd"] = stdd[2]
        fitData.attrs["tau2"] = out[4]
        fitData.attrs["tau2_stdd"] = stdd[4]
        fitData.attrs["C1"] = out[0]
        fitData.attrs["C2"] = out[1]
        fitData.attrs["C3"] = out[3]

    else:
        raise TypeError("Invalid fit type")

    if isDict:
        all_data["fit"] = fitData
        return all_data
    else:
        return fitData


def enhancementFunction(powerArray, E_max, power_half):
    return E_max * powerArray / (power_half + powerArray)


def enhancementFit(dataDict):
    """Fits enhancement curves to return Emax and power and one half maximum saturation

    .. math::

        f(p) = E_{max} p / (p_{1/2} + p)

    Args:
        workspace

    Returns:
        all_data (dnpdata, dict): Processed data in container, updated with fit data
        attributes: Emax value and Emax standard deviation

                    p_one_half value and p_one_half standard deviation

    Example::

        ### INSERT importing and processing ###
        dnplab.dnpNMR.integrate(workspace, {})

        workspace.new_dim('power', power_list)

        dnplab.dnpFit.enhancementFit(workspace)

        Emax_value = workspace['fit'].attrs['E_max']
        Emax_standard_deviation = workspace['fit'].attrs['E_max_stdd']
        p_one_half_value = workspace['fit'].attrs['p_half']
        p_one_half_standard_deviation = workspace['fit'].attrs['p_half_stdd']
        Emax_fit = workspace['fit'].values
        Emax_fit_xaxis = workspace['fit'].coords

    """

    isDict = False
    if isinstance(dataDict, (dict, dnpdata_collection)):
        data = dataDict["proc"].copy()
        isDict = True
    elif isinstance(dataDict, _dnpdata):
        data = dataDict.copy()
    else:
        raise TypeError("Incompatible data type")

    power_axes = data.coords["power"]

    inputData = _np.real(data.values)

    x0 = [inputData[-1], 0.1]

    out, cov = curve_fit(enhancementFunction, power_axes, inputData, x0, method="lm")
    stdd = _np.sqrt(_np.diag(cov))

    fit = enhancementFunction(power_axes, out[0], out[1])

    fitData = _dnpdata(fit, [power_axes], ["power"])
    fitData.attrs["E_max"] = out[0]
    fitData.attrs["E_max_stdd"] = stdd[0]
    fitData.attrs["power_half"] = out[1]
    fitData.attrs["power_half_stdd"] = stdd[1]

    if isDict:
        dataDict["fit"] = fitData
        return dataDict
    else:
        return fitData
