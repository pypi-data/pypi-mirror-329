import numpy as np
import opendp as dp
from opendp.domains import vector_domain, atom_domain
from opendp.metrics import l2_distance
from opendp.measurements import make_gaussian
from opendp.prelude import enable_features

enable_features("contrib")


def make_gaussian_noise(d_in: float,
                        rho: float) -> dp.Measurement:
    """
    Return a Gaussian mechanism with rho (from zCDP)
    :param d_in: int -  l2 sensitivity
    :param rho: float - privacy budget (rho in zCDP)
    :return: Gaussian mechanism
    """
    # assert dtype is int or float
    assert rho > 0, f"Invalid rho budget: {rho}, must be > 0"

    input_space = vector_domain(atom_domain(T=int)), l2_distance(T=int)
    mechanism = make_gaussian(*input_space, scale=d_in / np.sqrt(2 * rho))
    return mechanism


def make_int_gaussian_noise(d_in: int,
                            rho: float) -> dp.Measurement:
    """
    Return a Gaussian mechanism with rho (from zCDP)
    :param d_in: int -  l1 sensitivity
    :param rho: float - privacy budget (rho in zCDP)
    :return: Gaussian mechanism
    """
    # assert dtype is int or float
    assert rho > 0, f"Invalid rho budget: {rho}, must be > 0"

    input_space = atom_domain(T=int), l2_distance(T=int)
    mechanism = make_gaussian(*input_space, scale=d_in / np.sqrt(2 * rho))
    return mechanism


def get_rho_from_budget(budget: tuple[float, float]) -> float:
    """
    Return rho (from zCDP) given epsilon and delta.

    :param budget: tuple[float, float] - (epsilon, delta) privacy budget
    :return: rho: float- rho privacy budget
    """
    assert budget[0] > 0, f"Invalid epsilon: {budget[0]}, must be > 0"
    assert 0 < budget[1] < 1, f"Invalid delta: {budget[1]}, must be in (0, 1)"
    assert type(budget[0]) == float, f"Invalid epsilon type: {type(budget[0])}, must be float"
    assert type(budget[1]) == float, f"Invalid delta type: {type(budget[1])}, must be float"

    epsilon = budget[0]
    delta = budget[1]
    return np.log(1 / delta) * (np.sqrt(1 + epsilon / np.log(1 / delta)) - 1) ** 2
