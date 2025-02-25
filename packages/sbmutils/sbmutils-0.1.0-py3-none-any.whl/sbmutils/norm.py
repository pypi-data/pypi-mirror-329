import numpy as np
from scipy.stats import rankdata
import warnings


def quantilenorm(x, average="mean"):
    """
    Performs 2d quantile normalization. (over columns)

    Arguments:
        x: np.ndarray
            input array.
        average: str, default="mean"
            average method. "mean" or "median".

    Returns:
        x_norm: np.ndarray
            normalized array.

    Raises:
        TypeError: if x not np.ndarray.
        ValueError: if average not "mean" or "median".
    """

    if not isinstance(x, np.ndarray):
        raise TypeError(f"x must be np.ndarray not {type(x)}.")

    if average == "mean":
        average_func = np.mean
    elif average == "median":
        average_func = np.median
    else:
        raise ValueError(f"average must be either 'mean' of 'median' not {average}.")

    x = x.copy()
    x_norm = x.copy()

    r, c = x.shape
    x_nan = np.isnan(x)
    num_nans = np.sum(x_nan, axis=0)

    x[np.isnan(x)] = np.inf

    rr = []
    x_sorted = np.sort(x, axis=0)
    idx_sorted = np.argsort(x, axis=0)
    x_ranked = np.zeros([r, c])
    for i in range(c):
        ranked = rankdata(x[:, i][~x_nan[:, i]])
        rr.append(np.sort(ranked))

        m = r - num_nans[i]
        try:
            x_ranked[:, i] = np.interp(np.arange(1, r + 1),
                                       np.arange(1, r + 1, (r - 1) / (m - 1)),
                                       x_sorted[0:m, i])
        except ValueError:
            warnings.warn(f"{i}th column cannot be interpolated.")
            continue

    mean_val = average_func(x_ranked, axis=1)

    for i in range(c):
        m = r - num_nans[i]
        replace_idx = idx_sorted[:, i][0:m]
        x_norm[:, i][replace_idx] = np.interp(1 + ((r - 1) * (rr[i] - 1) / (m - 1)),
                                              np.arange(1, r + 1),
                                              mean_val)

    return x_norm
