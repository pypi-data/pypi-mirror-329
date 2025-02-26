import numpy as np
from typing import Dict, List, Tuple
from pyCFS.util.lib_types import pyCFSparamVec, resultVec
from .param_functions import (
    param_init_funcs,
    mat_switch_funcs,
    threshold_funcs,
)

GRAD_TOKEN = "gradParam"
P = "p"
PSTAR = "pstar"
DPSTAR_DP = "dpstar_dp"


class Topt:
    def __init__(
        self,
        sim,
        geometry_type: str,
        design_domain: str,
        param_data: Dict[str, Dict[str, float]],
        param_to_grad_map: Dict[str, int] = {},
        param_init_strategy: str = "ones",
        void_material: str = "V_air",
        mat_switch_method: str = "on-off",
        threshold_method: str = "sigmoid",
    ) -> None:
        self.sim = sim
        self.geometry_type = geometry_type
        self.design_domain = design_domain
        self.param_data = param_data
        self.void_material = void_material

        if param_init_strategy not in param_init_funcs.keys():
            raise KeyError(f"[pyCFS.topt] {param_init_strategy} not defined!")

        if mat_switch_method not in mat_switch_funcs.keys():
            raise KeyError(f"[pyCFS.topt] {mat_switch_method} not defined!")

        if threshold_method not in threshold_funcs.keys():
            raise KeyError(f"[pyCFS.topt] {threshold_method} not defined!")

        self.param_init_strategy = param_init_strategy
        self.mat_switch_method = mat_switch_method
        self.threshold_method = threshold_method

        self.regions_element_parameters: Dict[str, Dict[str, pyCFSparamVec]] = {}
        self.n_design_elems = 0
        self.p_vector = np.array([])
        self.param_history: List[Dict[str, pyCFSparamVec]] = []
        self.iter = 0  # iteration number
        self.history_dump_path = "./data_dump/topt_history.npy"
        self.param_to_grad_map = param_to_grad_map

        # run initializers :
        self._init_functions()
        self._init_topt_setup()
        self._init_element_parameters()

    def _init_functions(self) -> None:
        self.param_init_fun = param_init_funcs[self.param_init_strategy]
        self._mat_switch_fun, self._mat_switch_fun_deriv = mat_switch_funcs[self.mat_switch_method]
        self.threshold_fun, self.threshold_fun_deriv = threshold_funcs[self.threshold_method]

    def _init_topt_setup(self) -> None:
        self.sim.init_topopt_setup(geom_type=self.geometry_type)

    def _init_element_parameters(self) -> None:
        """Initializes a dictionary containing for each passed region in regions_data
        an array filled with the values given in param_data.

        """
        regions_data = self.sim._get_topt_regions(list(self.param_data.keys()))

        for region in regions_data:
            self.regions_element_parameters[region.Name] = {}
            n_elems = len(region.Elements)

            p_vector = self.param_init_fun((n_elems,))

            # initialize parameter state dict :
            param_state = self._init_param_state(p_vector)

            # perform thresholding step :
            self._do_thresholding(param_state)

            if region.Name not in self.param_data.keys():
                raise KeyError(f"[pyCFS.topt] {region.Name} not found in param_data!")

            for param, v_on in self.param_data[region.Name].items():
                # perform mat switch and update element parameters :
                self.regions_element_parameters[region.Name][param] = self._do_mat_switch(param, v_on, param_state)

            # update history state only if design domain
            # only tracking parameters from design domain
            if region == self.design_domain:
                # set number of elements in design domain
                self.n_design_elems = n_elems

                # update history state :
                self._update_hist_state(param_state)

        # write parameter file for cfs :
        self.sim.set_topopt_params(self.regions_element_parameters)

    @staticmethod
    def _construct_param_keys(param: str) -> Tuple[str, str]:
        key = f"{param}"
        deriv_key = f"d{param}_dpstar"
        return key, deriv_key

    @staticmethod
    def _init_param_state(p_vector: pyCFSparamVec) -> Dict[str, pyCFSparamVec]:
        return {P: p_vector}

    def _do_thresholding(self, param_state: Dict[str, pyCFSparamVec]) -> None:
        # p to p* (thresholding step) :
        param_state[PSTAR] = self.threshold_fun(param_state[P])
        param_state[DPSTAR_DP] = self.threshold_fun_deriv(param_state[P])

    def _do_mat_switch(self, param_name: str, param_val: float, param_state: Dict[str, pyCFSparamVec]) -> pyCFSparamVec:
        # get key names :
        param_key, param_deriv_key = self._construct_param_keys(param_name)
        v_off = self.param_data[self.void_material][param_name]

        # p* to material_param (mat switch function) :
        param_state[param_key] = self._mat_switch_fun(param_state[PSTAR], param_val, v_off)
        param_state[param_deriv_key] = self._mat_switch_fun_deriv(param_state[PSTAR], param_val, v_off)

        return param_state[param_key]

    def _update_hist_state(self, state: Dict[str, pyCFSparamVec]) -> None:
        self.param_history.append(state)
        self.iter += 1

    def update_design_parameters(self, p_vector: pyCFSparamVec) -> None:

        # initialize parameter state dict :
        param_state = self._init_param_state(p_vector)

        # perform thresholding step :
        self._do_thresholding(param_state)

        for param, v_on in self.param_data[self.design_domain].items():

            # perform mat switch and update element parameters :
            self.regions_element_parameters[self.design_domain][param] = self._do_mat_switch(param, v_on, param_state)

        # update history state :
        self._update_hist_state(param_state)

        # write parameter file for cfs :
        self.sim.set_topopt_params(self.regions_element_parameters)

    @staticmethod
    def filter_grad_keys(keys_list: List[str]) -> List[str]:
        grad_keys = []
        for key in keys_list:
            if GRAD_TOKEN in key:
                grad_keys.append(key)

        return grad_keys

    def _extract_mat_gradients(self, domain: str) -> resultVec:

        results = self.sim.results[0][1]
        grad_keys = Topt.filter_grad_keys(results.keys())
        n_elems = results[grad_keys[0]][domain].shape[1]

        gradients = np.zeros((n_elems, len(grad_keys)))

        for ind, grad_key in enumerate(grad_keys):
            # take only real parts of the computed gradients
            gradients[:, ind] = np.real(results[grad_key][domain][0, :, 0])

        return gradients

    def compute_gradient(self) -> resultVec:
        grads = self._extract_mat_gradients(self.design_domain)

        for p_name, grad_ind in self.param_to_grad_map.items():
            _, grad_key = self._construct_param_keys(p_name)

            # dg_dmat * dmat_dpstar
            grads[:, grad_ind] *= self.param_history[self.iter - 1][grad_key]  # type: ignore[operator]

        # dg_dp = dg_dpstar * dpstar_dp
        dg_dp = grads.sum(axis=1) * self.param_history[self.iter - 1][DPSTAR_DP]

        return dg_dp

    def dump_history(self) -> None:
        np.save(self.history_dump_path, self.param_history, allow_pickle=True)  # type: ignore[arg-type]
