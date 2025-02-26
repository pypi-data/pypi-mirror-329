import numpy as np
from pyCFS.util.lib_types import pyCFSparamVec

# p* to mat functions (material switching) :


def switch_fun_onoff(p: pyCFSparamVec, v_on: float, v_off: float) -> pyCFSparamVec:
    return p * (v_on - v_off) + v_off  # type: ignore[operator]


def switch_fun_onoff_deriv(p: pyCFSparamVec, v_on: float, v_off: float) -> pyCFSparamVec:
    return np.ones_like(p) * (v_on - v_off)  # type: ignore[operator]


# p to p* functions (thresholding) :


def sigmoid(p: pyCFSparamVec, a: float = 50, b: float = 0.5) -> pyCFSparamVec:
    return 1 / (1 + np.exp(-a * (p - b)))  # type: ignore[operator]


def sigmoid_deriv(p: pyCFSparamVec, a: float = 50, b: float = 0.5) -> pyCFSparamVec:
    return a * np.exp(-a * (p - b)) * 1 / (1 + np.exp(-a * (p - b))) ** 2  # type: ignore[operator]


param_init_funcs = {
    "ones": np.ones,
    "zeros": np.zeros,
}

mat_switch_funcs = {
    "on-off": (switch_fun_onoff, switch_fun_onoff_deriv),
}

threshold_funcs = {"sigmoid": (sigmoid, sigmoid_deriv)}
