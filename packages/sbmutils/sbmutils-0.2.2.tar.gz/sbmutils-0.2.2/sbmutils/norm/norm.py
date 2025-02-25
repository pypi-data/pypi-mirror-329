import numpy as np
import pandas as pd
from scipy.stats import rankdata
import warnings


def quantilenorm(x, average="mean"):
    """
    Quantile normalize a 2D array or pandas DataFrame across its columns.

    This function aligns the distributions of each column in a 2D numpy array or 
    DataFrame by mapping the sorted values of each column to a common distribution.
    The common distribution is computed as the element-wise average (using either the 
    mean or median) across all columns.

    Args:
        x (np.ndarray or pd.DataFrame): A 2D array or DataFrame of data to be normalized.
        average (str, optional): The method to compute the common distribution.
            Must be either "mean" (default) for the arithmetic mean or "median" for 
            the median value.

    Returns:
        np.ndarray or pd.DataFrame: A quantile normalized array or DataFrame with columns 
        aligned to a common distribution. If the input is a DataFrame, the output will 
        preserve its index and column labels.

    Raises:
        TypeError: If `x` is not a numpy.ndarray or pandas DataFrame.
        ValueError: If `average` is not "mean" or "median", or if one or more columns 
                    in `x` have fewer than 2 non-NaN values.

    Example:
        >>> import pandas as pd
        >>> x = pd.DataFrame([[1, 4], [2, 5], [3, 6]])
        >>> quantilenorm(x, average="mean")
             0    1
        0  2.5  2.5
        1  3.5  3.5
        2  4.5  4.5
    """
    # Check input type.
    if not isinstance(x, (np.ndarray, pd.DataFrame)):
        raise TypeError(f"x must be np.ndarray or pd.DataFrame, not {type(x)}.")

    # Determine if input is a DataFrame.
    is_dataframe = isinstance(x, pd.DataFrame)
    # Convert to a NumPy array and force float conversion.
    x_array = x.values.copy().astype(np.float64) if is_dataframe else x.copy().astype(np.float64)

    if average == "mean":
        average_func = np.mean
    elif average == "median":
        average_func = np.median
    else:
        raise ValueError(f"average must be either 'mean' or 'median' not {average}.")

    # Copy array for normalization.
    x_norm = x_array.copy()

    r, c = x_array.shape
    x_nan = np.isnan(x_array)
    num_nans = np.sum(x_nan, axis=0)
    
    # Ensure each column has at least 2 non-NaN values.
    valid_counts = r - num_nans
    if np.any(valid_counts < 2):
        raise ValueError("One or more columns have less than 2 non-NaN values, cannot interpolate.")

    # Replace NaNs with infinity for sorting purposes.
    x_array[np.isnan(x_array)] = np.inf

    rr = []
    x_sorted = np.sort(x_array, axis=0)
    idx_sorted = np.argsort(x_array, axis=0)
    x_ranked = np.zeros((r, c))
    for i in range(c):
        ranked = rankdata(x_array[:, i][~x_nan[:, i]])
        rr.append(np.sort(ranked))

        m = valid_counts[i]
        # Use linspace to safely generate interpolation points.
        x_ranked[:, i] = np.interp(
            np.arange(1, r + 1),
            np.linspace(1, r, m),
            x_sorted[0:m, i]
        )

    # Compute the common distribution (mean or median of the ranked values).
    mean_val = average_func(x_ranked, axis=1)

    for i in range(c):
        m = valid_counts[i]
        replace_idx = idx_sorted[:, i][0:m]
        x_norm[replace_idx, i] = np.interp(
            1 + ((r - 1) * (rr[i] - 1) / (m - 1)),
            np.arange(1, r + 1),
            mean_val
        )

    # If input was a DataFrame, convert the result back to a DataFrame.
    if is_dataframe:
        return pd.DataFrame(x_norm, index=x.index, columns=x.columns)
    return x_norm


def stacked_quantilenorm(x, batch, average="mean"):
    """
    Stacked quantile normalize a 2D array or pandas DataFrame across groups defined by batch.

    This function performs quantile normalization on data that is divided into batches, aligning the distributions
    of each group of columns defined by `batch`. For each batch, the function:
      1. Separates the columns belonging to each batch.
      2. Stacks the batch data into a common 2D array.
      3. Applies quantile normalization (using the `quantilenorm` function) across the stacked data.
      4. Reconstructs the normalized array or DataFrame with columns corresponding to the original input order.

    Args:
        x (np.ndarray or pd.DataFrame): A 2D array or DataFrame of data to be normalized. If a DataFrame is provided,
            its index and column labels will be preserved in the output.
        batch (array-like): An array-like object of batch labels for each column of `x`. Columns with the same batch 
            label will be normalized together.
        average (str, optional): The method to compute the common distribution during quantile normalization.
            Must be either "mean" (default) for the arithmetic mean or "median" for the median value.

    Returns:
        np.ndarray or pd.DataFrame: A quantile normalized array or DataFrame with columns aligned to a common distribution 
        within each batch, preserving the original column order. If `x` is a DataFrame, the output will maintain the same 
        index and column labels.

    Raises:
        TypeError: If `x` is not a numpy.ndarray or pandas DataFrame.
        ValueError: If the number of columns in `x` does not match the length of `batch`, if `average` is not "mean" or "median",
                    or if one or more columns in `x` have fewer than 2 non-NaN values (in the underlying quantile normalization).

    Example:
        >>> import pandas as pd
        >>> x = pd.DataFrame([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        >>> batch = [0, 0, 1]
        >>> stacked_quantilenorm(x, batch, average="mean")
             0    1     2
        0  4.0  6.1  4.00
        1  4.7  6.8  5.75
        2  5.4  7.5  7.50
    """

    # Determine if input is a DataFrame.
    is_dataframe = isinstance(x, pd.DataFrame)
    # Convert to a NumPy array and force float conversion.
    x_array = x.values.astype(np.float64) if is_dataframe else x.copy().astype(np.float64)

    batch = np.asarray(batch)
    if x_array.shape[1] != len(batch):
        raise ValueError("The number of columns in x must match the length of batch.")

    # Get unique batch labels (sorted) and group columns by batch.
    batch_set = np.unique(batch)
    x_batch = {b: x_array[:, batch == b] for b in batch_set}

    # Determine maximum number of columns across batches and number of rows.
    max_c = max(v.shape[1] for v in x_batch.values())
    r = x_array.shape[0]

    # Initialize array for stacked normalization.
    x_quantilenorm = np.full((max_c * r, len(x_batch)), np.nan, dtype=np.float64)
    for i, d in enumerate(x_batch.values()):
        c = d.shape[1]
        x_quantilenorm[: r * c, i] = d.flatten()

    # Apply quantile normalization on the stacked data.
    x_quantilenorm = quantilenorm(x_quantilenorm, average=average)

    # Prepare the normalized output array.
    x_norm = np.full_like(x_array, np.nan, dtype=np.float64)
    for i, d in enumerate(x_batch.values()):
        c = d.shape[1]
        # Assign normalized values back to the columns corresponding to the original batch,
        # preserving the original order via boolean indexing.
        x_norm[:, np.array(batch) == batch_set[i]] = x_quantilenorm[: r * c, i].reshape(r, c)

    # If the input was a DataFrame, convert the result back to a DataFrame preserving index and columns.
    if is_dataframe:
        return pd.DataFrame(x_norm, index=x.index, columns=x.columns)
    return x_norm
