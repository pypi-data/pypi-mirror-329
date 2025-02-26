from typing import Any, Callable, Optional, Union

import numpy as np
import pandas as pd


class WeightedSeries(pd.Series):
    """
    A pandas Series that supports weighted operations.
    """

    _metadata = pd.Series._metadata + ["_weights"]

    def __init__(
        self,
        data=None,
        index=None,
        dtype=None,
        name=None,
        copy=False,
        weights=None,
        **kwargs,
    ):
        super().__init__(
            data=data, index=index, dtype=dtype, name=name, copy=copy, **kwargs
        )

        if weights is None:
            self._weights = pd.Series(np.ones(len(self)), index=self.index)
        elif isinstance(weights, (pd.Series, WeightedSeries)):
            if not weights.index.equals(self.index):
                weights = weights.reindex(self.index)
            self._weights = pd.Series(weights)
        else:
            self._weights = pd.Series(weights, index=self.index)

    @property
    def weights(self) -> pd.Series:
        """Return the weights as a pandas Series."""
        return self._weights

    def set_weights(self, weights) -> "WeightedSeries":
        """Set new weights for this series."""
        result = self.copy()
        if isinstance(weights, (pd.Series, WeightedSeries)):
            if not weights.index.equals(self.index):
                weights = weights.reindex(self.index)
            result._weights = pd.Series(weights)
        else:
            result._weights = pd.Series(weights, index=self.index)
        return result

    @property
    def _constructor(self):
        return WeightedSeries

    @property
    def _constructor_expanddim(self):
        return WeightedDataFrame

    def sum(self, *args, **kwargs) -> float:
        """Return the weighted sum."""
        return pd.Series(self.values * self._weights.values).sum(*args, **kwargs)

    def mean(self, *args, **kwargs) -> float:
        """Return the weighted mean."""
        weights_sum = self._weights.sum(*args, **kwargs)
        if weights_sum == 0:
            return np.nan
        return (
            pd.Series(self.values * self._weights.values).sum(*args, **kwargs)
            / weights_sum
        )

    def var(self, ddof: int = 1, *args, **kwargs) -> float:
        """Return the weighted variance."""
        weights_sum = self._weights.sum(*args, **kwargs)
        if weights_sum == 0:
            return np.nan

        wmean = self.mean(*args, **kwargs)
        return pd.Series(((self.values - wmean) ** 2) * self._weights.values).sum(
            *args, **kwargs
        ) / (weights_sum - ddof)

    def std(self, ddof: int = 1, *args, **kwargs) -> float:
        """Return the weighted standard deviation."""
        return np.sqrt(self.var(ddof=ddof, *args, **kwargs))

    def quantile(self, q: float = 0.5, *args, **kwargs) -> float:
        """Return the weighted quantile."""
        if not 0 <= q <= 1:
            raise ValueError("Quantile must be between 0 and 1")

        # Sort values and corresponding weights
        sorted_indices = np.argsort(self.values)
        sorted_values = self.values[sorted_indices]
        sorted_weights = self._weights.values[sorted_indices]

        # Normalize weights
        weight_sum = sorted_weights.sum()
        if weight_sum == 0:
            return np.nan

        cumsum = np.cumsum(sorted_weights) / weight_sum

        # Find index where cumulative sum exceeds q
        idx = np.searchsorted(cumsum, q, side="right")
        if idx == 0:
            return sorted_values[0]
        if idx >= len(sorted_values):
            return sorted_values[-1]

        return sorted_values[idx]

    def median(self, *args, **kwargs) -> float:
        """Return the weighted median."""
        return self.quantile(0.5, *args, **kwargs)

    def _apply_binary_operator(self, other, op):
        """Apply a binary operator."""
        result = op(self, other)
        if isinstance(result, pd.Series):
            if isinstance(result, WeightedSeries):
                return result
            return WeightedSeries(result, weights=self._weights)
        return result

    def __add__(self, other):
        return self._apply_binary_operator(other, pd.Series.__add__)

    def __sub__(self, other):
        return self._apply_binary_operator(other, pd.Series.__sub__)

    def __mul__(self, other):
        return self._apply_binary_operator(other, pd.Series.__mul__)

    def __truediv__(self, other):
        return self._apply_binary_operator(other, pd.Series.__truediv__)

    def __floordiv__(self, other):
        return self._apply_binary_operator(other, pd.Series.__floordiv__)

    def __mod__(self, other):
        return self._apply_binary_operator(other, pd.Series.__mod__)

    def __pow__(self, other):
        return self._apply_binary_operator(other, pd.Series.__pow__)

    # Reverse operations
    def __radd__(self, other):
        return self._apply_binary_operator(other, pd.Series.__radd__)

    def __rsub__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rsub__)

    def __rmul__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rmul__)

    def __rtruediv__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rtruediv__)

    def __rfloordiv__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rfloordiv__)

    def __rmod__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rmod__)

    def __rpow__(self, other):
        return self._apply_binary_operator(other, pd.Series.__rpow__)

    # Comparison operations
    def __lt__(self, other):
        return self._apply_binary_operator(other, pd.Series.__lt__)

    def __le__(self, other):
        return self._apply_binary_operator(other, pd.Series.__le__)

    def __gt__(self, other):
        return self._apply_binary_operator(other, pd.Series.__gt__)

    def __ge__(self, other):
        return self._apply_binary_operator(other, pd.Series.__ge__)

    def __eq__(self, other):
        return self._apply_binary_operator(other, pd.Series.__eq__)

    def __ne__(self, other):
        return self._apply_binary_operator(other, pd.Series.__ne__)


class WeightedDataFrame(pd.DataFrame):
    """
    A pandas DataFrame that supports weighted operations.
    """

    _metadata = pd.DataFrame._metadata + ["_weights"]

    def __init__(
        self,
        data=None,
        index=None,
        columns=None,
        dtype=None,
        copy=False,
        weights=None,
        **kwargs,
    ):
        super().__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy, **kwargs
        )

        if weights is None:
            self._weights = pd.Series(np.ones(len(self)), index=self.index)
        elif isinstance(weights, (pd.Series, WeightedSeries)):
            if not weights.index.equals(self.index):
                weights = weights.reindex(self.index)
            self._weights = pd.Series(weights)
        else:
            self._weights = pd.Series(weights, index=self.index)

    @property
    def weights(self) -> pd.Series:
        """Return the weights as a pandas Series."""
        return self._weights

    def set_weights(self, weights) -> "WeightedDataFrame":
        """Set new weights for this dataframe."""
        result = self.copy()
        if isinstance(weights, (pd.Series, WeightedSeries)):
            if not weights.index.equals(self.index):
                weights = weights.reindex(self.index)
            result._weights = pd.Series(weights)
        else:
            result._weights = pd.Series(weights, index=self.index)
        return result

    @property
    def _constructor(self):
        return WeightedDataFrame

    @property
    def _constructor_sliced(self):
        return WeightedSeries

    def sum(self, axis=0, *args, **kwargs):
        """Return the weighted sum along the specified axis."""
        if axis == 0:
            result = {}
            for col in self.columns:
                values = self[col].values
                weights = self._weights.values
                result[col] = np.sum(values * weights, *args, **kwargs)
            return pd.Series(result)
        return super().sum(axis=axis, *args, **kwargs)

    def mean(self, axis=0, *args, **kwargs):
        """Return the weighted mean along the specified axis."""
        if axis == 0:
            result = {}
            weights_sum = self._weights.sum(*args, **kwargs)
            if weights_sum == 0:
                return pd.Series({col: np.nan for col in self.columns})

            for col in self.columns:
                values = self[col].values
                weights = self._weights.values
                result[col] = np.sum(values * weights, *args, **kwargs) / weights_sum
            return pd.Series(result)
        return super().mean(axis=axis, *args, **kwargs)

    def var(self, axis=0, ddof=1, *args, **kwargs):
        """Return the weighted variance along the specified axis."""
        if axis == 0:
            result = {}
            weights_sum = self._weights.sum(*args, **kwargs)
            if weights_sum == 0:
                return pd.Series({col: np.nan for col in self.columns})

            wmeans = self.mean(axis=0, *args, **kwargs)

            for col in self.columns:
                values = self[col].values
                weights = self._weights.values
                result[col] = np.sum(
                    ((values - wmeans[col]) ** 2) * weights, *args, **kwargs
                ) / (weights_sum - ddof)
            return pd.Series(result)
        return super().var(axis=axis, ddof=ddof, *args, **kwargs)

    def std(self, axis=0, ddof=1, *args, **kwargs):
        """Return the weighted standard deviation along the specified axis."""
        if axis == 0:
            return self.var(axis=axis, ddof=ddof, *args, **kwargs).apply(np.sqrt)
        return super().std(axis=axis, ddof=ddof, *args, **kwargs)

    def quantile(self, q=0.5, axis=0, *args, **kwargs):
        """Return the weighted quantile along the specified axis."""
        if axis == 0:
            result = {}
            for col in self.columns:
                series = WeightedSeries(self[col].values, weights=self._weights.values)
                result[col] = series.quantile(q, *args, **kwargs)
            return pd.Series(result)
        return super().quantile(q=q, axis=axis, *args, **kwargs)

    def median(self, axis=0, *args, **kwargs):
        """Return the weighted median along the specified axis."""
        return self.quantile(q=0.5, axis=axis, *args, **kwargs)

    def corr(self, method="pearson", min_periods=1):
        """Return the weighted correlation matrix."""
        if method != "pearson":
            raise ValueError(
                "Only Pearson correlation is implemented for weighted DataFrames"
            )

        # Calculate the weighted means
        wmeans = self.mean()

        # Initialize covariance and standard deviation containers
        wcov = pd.DataFrame(0.0, index=self.columns, columns=self.columns)
        wstd = pd.Series(0.0, index=self.columns)

        # Calculate weighted standard deviations and covariances
        for i in self.columns:
            # Standard deviation for column i
            wstd[i] = np.sqrt(
                np.sum(((self[i].values - wmeans[i]) ** 2) * self._weights.values)
                / self._weights.sum()
            )

            for j in self.columns:
                # Covariance between columns i and j
                wcov.loc[i, j] = (
                    np.sum(
                        (self[i].values - wmeans[i])
                        * (self[j].values - wmeans[j])
                        * self._weights.values
                    )
                    / self._weights.sum()
                )

        # Calculate correlation matrix
        wcorr = pd.DataFrame(0.0, index=self.columns, columns=self.columns)
        for i in self.columns:
            for j in self.columns:
                if wstd[i] == 0 or wstd[j] == 0:
                    wcorr.loc[i, j] = np.nan
                else:
                    wcorr.loc[i, j] = wcov.loc[i, j] / (wstd[i] * wstd[j])

        return wcorr

    def cov(self, min_periods=None):
        """Return the weighted covariance matrix."""
        # Calculate the weighted means
        wmeans = self.mean()

        # Initialize covariance container
        wcov = pd.DataFrame(0.0, index=self.columns, columns=self.columns)

        # Calculate weighted covariances
        weights_sum = self._weights.sum()
        if weights_sum == 0:
            return pd.DataFrame(np.nan, index=self.columns, columns=self.columns)

        factor = weights_sum / (weights_sum - (1 if min_periods else 0))

        for i in self.columns:
            for j in self.columns:
                wcov.loc[i, j] = (
                    np.sum(
                        (self[i].values - wmeans[i])
                        * (self[j].values - wmeans[j])
                        * self._weights.values
                    )
                    / weights_sum
                    * factor
                )

        return wcov

    def __getitem__(self, key):
        """Get item with the same weights."""
        result = super().__getitem__(key)
        if isinstance(result, pd.Series):
            if isinstance(result, WeightedSeries):
                return result
            return WeightedSeries(result, weights=self._weights)
        elif isinstance(result, pd.DataFrame):
            if isinstance(result, WeightedDataFrame):
                return result
            return WeightedDataFrame(result, weights=self._weights)
        return result


def weighted_series(data, weights=None, **kwargs):
    """Create a WeightedSeries."""
    return WeightedSeries(data, weights=weights, **kwargs)


def weighted_dataframe(data, weights=None, **kwargs):
    """Create a WeightedDataFrame."""
    return WeightedDataFrame(data, weights=weights, **kwargs)
