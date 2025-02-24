import numpy as np


def int_opt(x: np.array(int), c: int) -> np.array:
    """
    From Algorithm 3 in the Appendix
    Args:
        x: np.array: array of integer
        c: int: constraint

    Returns: y: np.array: array of integer

    """
    # handle base case
    if c == 0:
        return np.zeros(len(x))

    a = (c - x.sum()) / len(x)
    constrait = int(c - x.sum())
    # round
    a_int = int(np.ceil(a))
    z = np.ones(len(x)) * a_int
    # clip
    z = np.maximum(z, -x).astype(int)
    t = max(abs(z))  # smallest value in z that is allowed
    I = np.argsort(x)  # get indices of x in ascending order
    I = I[z[I] > -x[I]]
    z_sum = z.sum()
    i = 0
    while z_sum > constrait:
        R = int(z.sum() - c + x.sum())
        z_new = max(z[I[i]] - R, -x[I[i]], -t)
        reduction = z[I[i]] - z_new
        z[I[i]] = z_new
        z_sum -= reduction
        i += 1
        if i == len(I):
            I = I[z[I] > -x[I]]
            g = len(I)
            r = int((1 / g) * (z_sum - constrait))
            t += max(1, r)
            i = 0
    return z + x
