from functools import partial
from multiprocessing import Pool
from typing import Tuple, Optional

import numpy as np
from pyCFS.data.util import progressbar, TimeRecord


def vkp_spectrum(K, nu, urms, epsilon, ke, kmin=0.0, kmax=1e6) -> np.ndarray:
    urms = urms
    # computed from input to satisfy homogeneous turbulence properties
    Kappae = np.sqrt(5.0 / 12.0) * ke
    Alpha = 1.452762113
    KappaEta = pow(epsilon, 0.25) * pow(nu, -3.0 / 4.0)
    r1 = K / Kappae
    r2 = K / KappaEta
    espec = Alpha * urms * urms / Kappae * pow(r1, 4) / pow(1.0 + r1 * r1, 17.0 / 6.0) * np.exp(-2.0 * r2 * r2)
    return espec


def eval_stochastic_input_mode(
    Kn, kin_viscosity, urms, tdr, K_e, DK_lin, eps_orthogonal=1e-9, rn_gen=np.random.default_rng()
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # evalEnergy (2.61)
    E = vkp_spectrum(Kn, kin_viscosity, urms, tdr, K_e)
    # calcModeAmplitude (2.60)
    u_tilde = np.sqrt(E * DK_lin)
    # angular frequency (2.67)
    omega = rn_gen.normal(loc=urms * Kn, scale=urms * Kn)

    # randomly draw alpha
    alpha = rn_gen.uniform(low=0.0, high=2 * np.pi)
    # randomly draw phi
    phi = rn_gen.uniform(low=0.0, high=2 * np.pi)
    # randomly draw psi
    psi = rn_gen.uniform(low=0.0, high=2 * np.pi)
    # randomly draw theta (4.2) - (4.4)
    theta = np.arccos(1 - 2 * rn_gen.uniform(low=0.0, high=1.0))
    # assemble wave vector
    wave_vec = np.array([Kn * np.cos(theta) * np.cos(phi), Kn * np.sin(phi), -Kn * np.sin(theta) * np.cos(phi)])
    # assemble mode direction
    sigma_vec = np.array(
        [
            -np.sin(phi) * np.cos(alpha) * np.cos(theta) + np.sin(alpha) * np.sin(theta),
            np.cos(phi) * np.cos(alpha),
            np.sin(phi) * np.cos(alpha) * np.sin(theta) + np.sin(alpha) * np.cos(theta),
        ]
    )

    # check if wave vector and mode direction are orthogonal
    wave_div = np.dot(wave_vec, sigma_vec)
    if wave_div > eps_orthogonal:
        print(f"Orthogonality check failed. Divergence in wave space: {wave_div}")

    return u_tilde, omega, psi, wave_vec, sigma_vec


def eval_stochastic_input_node(
    i,
    node_ids_process,
    kin_viscosity,
    length_scale_factor,
    tke,
    tdr,
    max_wave_number_percentage,
    min_wave_number_percentage,
    num_modes,
    urms,
    C_mu=0.09,
    vkp_scaling_const=1.452762113,
    eps_orthogonal=1e-9,
    rn_gen=np.random.default_rng(),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nid = node_ids_process[i]
    # calcLengthScale (2.68)
    turb_length_scale = length_scale_factor * C_mu * tke[nid] ** (3 / 2) / tdr[nid]  # l
    # calcMostEnergeticWaveNumber (2.70)
    K_e = 9 * np.pi / 55 * vkp_scaling_const / turb_length_scale
    # (4.9)
    K_N = max_wave_number_percentage * K_e
    # (4.8)
    K_1 = min_wave_number_percentage * K_e
    # assembleWaveNumbers (2.72)
    DK_lin = (K_N - K_1) / (num_modes - 1)
    K = np.arange(start=K_1, stop=K_N + DK_lin, step=DK_lin)

    u_tilde = np.zeros((num_modes))
    omega = np.zeros((num_modes))
    psi = np.zeros((num_modes))
    wave_vec = np.zeros((num_modes, 3))
    sigma_vec = np.zeros((num_modes, 3))

    for n in range(num_modes):
        (u_tilde[n], omega[n], psi[n], wave_vec[n, :], sigma_vec[n, :]) = eval_stochastic_input_mode(
            K[n], kin_viscosity, urms[nid], tdr[nid], K_e, DK_lin, eps_orthogonal=eps_orthogonal, rn_gen=rn_gen
        )

    return u_tilde, omega, psi, wave_vec, sigma_vec


def eval_fluct_velocity(
    i, timesteps, num_modes, u_tilde, wave_vec, coords, mean_velocity, node_ids_process, psi, omega, sigma_vec
) -> np.ndarray:
    num_nodes_process = len(node_ids_process)

    u_prime_step = np.zeros((num_nodes_process, 3))
    t = timesteps[i]
    for n in range(num_modes):
        # compute turbulent velocity fluctuations (2.66)
        u_prime_mode_contribution = (
            2
            * u_tilde[:, n]
            * np.cos(
                (wave_vec[:, n, :] * (coords[node_ids_process, :] - t * mean_velocity[node_ids_process, :])).sum(1)
                + psi[:, n]
                + omega[:, n] * t
            )
        )
        u_prime_step += u_prime_mode_contribution.reshape(num_nodes_process, 1) * sigma_vec[:, n, :]

    return u_prime_step


def compute_stochastic_velocity_fluctuations(
    coords: np.ndarray,
    mean_velocity: np.ndarray,
    tke: np.ndarray,
    tdr: np.ndarray,
    length_scale_factor: float,
    kin_viscosity: float,
    crit_tke_percentage: float,
    max_wave_number_percentage: float,
    min_wave_number_percentage: float,
    num_modes: int,
    num_steps: int,
    delta_t: float,
    C_mu=0.09,
    vkp_scaling_const=1.452762113,
    eps_orthogonal: float = 1e-9,
    rn_gen=np.random.default_rng(),
    processes: Optional[int] = None,
    mem_max: float = 4.0,
    processes_max: int = 4,
    flag_debug=False,
) -> Tuple[np.ndarray, np.ndarray]:
    num_nodes = coords.shape[0]

    k_max = max(tke)
    k_min = crit_tke_percentage * k_max

    # get tke threshold
    node_ids_process = np.where(tke > k_min)[0]

    num_nodes_process = len(node_ids_process)
    u_tilde = np.zeros((num_nodes_process, num_modes))
    omega = np.zeros((num_nodes_process, num_modes))
    psi = np.zeros((num_nodes_process, num_modes))
    wave_vec = np.zeros((num_nodes_process, num_modes, 3))  # K
    sigma_vec = np.zeros((num_nodes_process, num_modes, 3))  # sigma

    urms = np.sqrt(2.0 / 3.0 * tke)

    eval_stochastic_input_node_args = {
        "node_ids_process": node_ids_process,
        "kin_viscosity": kin_viscosity,
        "length_scale_factor": length_scale_factor,
        "tke": tke,
        "tdr": tdr,
        "max_wave_number_percentage": max_wave_number_percentage,
        "min_wave_number_percentage": min_wave_number_percentage,
        "num_modes": num_modes,
        "urms": urms,
        "C_mu": C_mu,
        "vkp_scaling_const": vkp_scaling_const,
        "eps_orthogonal": eps_orthogonal,
        "rn_gen": rn_gen,
    }

    if flag_debug:
        for i, nid in enumerate(progressbar(node_ids_process, prefix="Draw stochastic quantities (sequential)")):
            (u_tilde[i, ...], omega[i, ...], psi[i, ...], wave_vec[i, ...], sigma_vec[i, ...]) = (
                eval_stochastic_input_node(i, **eval_stochastic_input_node_args)
            )
    else:
        # RAM usage estimate
        mem_base = u_tilde.nbytes + omega.nbytes + psi.nbytes + wave_vec.nbytes + sigma_vec.nbytes
        mem_per_worker = tke.nbytes + tdr.nbytes + urms.nbytes
        print(
            f"RAM usage estimate: {mem_per_worker / (1024 ** 3):.2f} GB per worker and {mem_base / (1024 ** 3):.2f} GB base"
        )
        if processes is None:
            processes_mem_contraint = int((mem_max * (1024**3) - mem_base) / mem_per_worker)
        else:
            processes_mem_contraint = min(processes, int((mem_max * (1024**3) - mem_base) / mem_per_worker))
        processes_mem_contraint = min(max(processes_mem_contraint, 1), processes_max)

        with TimeRecord(message=f"Draw stochastic quantities ({processes_mem_contraint} processes)"):
            with Pool(processes=processes_mem_contraint) as pool:
                for i, res_node in enumerate(
                    pool.map(
                        partial(eval_stochastic_input_node, **eval_stochastic_input_node_args),
                        range(node_ids_process.size),
                    )
                ):
                    (u_tilde[i, ...], omega[i, ...], psi[i, ...], wave_vec[i, ...], sigma_vec[i, ...]) = res_node

    del tke, tdr

    # update results
    u_prime_process = np.zeros((num_steps, num_nodes_process, 3))
    timesteps = delta_t * np.arange(num_steps)

    eval_fluct_velocity_args = {
        "timesteps": timesteps,
        "num_modes": num_modes,
        "u_tilde": u_tilde,
        "wave_vec": wave_vec,
        "coords": coords,
        "mean_velocity": mean_velocity,
        "node_ids_process": node_ids_process,
        "psi": psi,
        "omega": omega,
        "sigma_vec": sigma_vec,
    }
    if flag_debug:
        for i, t in enumerate(progressbar(timesteps, prefix="Compute turbulent velocity fluctuations: ")):
            u_prime_process[i, ...] = eval_fluct_velocity(i, **eval_fluct_velocity_args)
    else:
        with Pool(processes=processes) as pool:
            with TimeRecord(message="Compute turbulent velocity fluctuations (parallel)"):
                for i, res_u_prime in enumerate(
                    pool.map(
                        partial(
                            eval_fluct_velocity,
                            **eval_fluct_velocity_args,
                        ),
                        range(timesteps.size),
                    )
                ):
                    u_prime_process[i, ...] = res_u_prime

    u_prime = np.zeros((num_steps, num_nodes, 3))
    u_prime[:, node_ids_process, :] = u_prime_process

    return u_prime, timesteps
