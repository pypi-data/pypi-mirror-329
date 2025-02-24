import numpy as np
import pandas as pd
from .differential_privacy import make_gaussian_noise, get_rho_from_budget
from .optimization import int_opt


def inf_tda(data: pd.Series,
            budget: tuple[float, float],
            contribution: int,
            privacy_type: str = "bounded",
            distinct_tuples: bool = True) -> pd.Series:
    """
    Return a differential private dataset using the InfTDA mechanism
    :param data: the sensitive dataset as a pd.Series with a MultiIndex
    :param budget: (epsilon, delta) privacy budget
    :param contribution: How many tuples a user can contribute at most to the dataset
    :param privacy_type: str - "bounded" or "unbounded" privacy
    :param distinct_tuples: bool - True if each user can contribute to only distinct tuples, False otherwise
    """
    # checks
    assert budget[0] > 0, f"Invalid epsilon: {budget[0]}, must be > 0"
    assert 0 < budget[1] < 1, f"Invalid delta: {budget[1]}, must be in (0, 1)"
    assert isinstance(budget[0], float), f"Invalid epsilon type: {type(budget[0])}, must be float"
    assert isinstance(budget[1], float), f"Invalid delta type: {type(budget[1])}, must be float"
    assert isinstance(contribution, int), f"Invalid contribution type: {type(contribution)}, must be int"
    assert isinstance(data, pd.Series), f"Invalid input type: {type(data)}, must be pd.Series"
    assert isinstance(data.index, pd.MultiIndex), f"Invalid index type: {type(data.index)}, must be pd.MultiIndex"

    if privacy_type == "unbounded":
        # Not implemented yet
        raise NotImplementedError("Unbounded privacy is not implemented yet")

    # sort intial data for higher performance
    data = data.sort_index()

    # total counts
    n = data.sum()
    T = data.index.nlevels
    # get rho from budget
    rho = get_rho_from_budget(budget)
    # get sensitivity
    sensitivity = get_sensitivity(contribution, privacy_type, distinct_tuples)
    # instantiate the differentially private mechanism
    dp_mechanism = make_gaussian_noise(d_in=sensitivity, rho=rho / T)

    c = [(None, n)]  # constraint
    levels = []  # levels (e.g., [0], [0,1], [0,1,2] up to [0,1,2,...,T-1])
    for i in range(T):
        # initialize the new constraints
        c_new = []
        # add the level to the list
        levels.append(i)
        ## computing the groupby queries
        if i == T - 1:
            # the last level is the original data
            df = data
        else:
            df: pd.Series = data.groupby(level=levels).sum()
        # iterate over the constraints
        for index, constraint in c:
            # if none, we already have the child dataframe
            df_child = df.xs(key=index, drop_level=False) if index is not None else df
            # apply the mechanism
            dp_df_values = np.array(dp_mechanism(df_child.values))
            # optimize using IntOpt
            opt_dp_df_values: np.array = int_opt(dp_df_values, constraint)
            # add the new constraints, remove the zeros
            c_new.extend([(idx, val) for idx, val in zip(df_child.index, opt_dp_df_values) if val != 0])
        # update the constraints for the next iteration
        c = c_new
    # return the final dataframe
    c_index, c_values = zip(*c)
    return pd.Series(c_values, index=pd.MultiIndex.from_tuples(c_index), dtype=int)


def get_sensitivity(m: int, privacy_type: str, distinct: bool) -> float:
    if distinct:
        if privacy_type == "bounded":
            return np.sqrt(2) * m
        elif privacy_type == "unbounded":
            return float(m)
        else:
            raise ValueError(f"Invalid privacy type: {privacy_type}, must be 'bounded' or 'unbounded'")
    else:
        if privacy_type == "bounded":
            return np.sqrt(2 * m)
        elif privacy_type == "unbounded":
            return np.sqrt(m)
        else:
            raise ValueError(f"Invalid privacy type: {privacy_type}, must be 'bounded' or 'unbounded'")
