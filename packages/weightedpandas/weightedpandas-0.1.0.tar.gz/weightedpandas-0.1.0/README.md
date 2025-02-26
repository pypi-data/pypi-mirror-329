# WeightedPandas

WeightedPandas extends pandas Series and DataFrame classes to support weighted operations. It provides drop-in replacements for pandas objects that automatically handle weights in statistical operations.

## Installation

```bash
pip install weightedpandas
```

## Requirements

- Python 3.8+
- pandas 1.4.0+
- numpy 1.20.0+

## Features

- Weighted versions of common statistical operations:
  - `sum()`, `mean()`, `var()`, `std()`
  - `median()`, `quantile()`
  - `corr()`, `cov()`
- Preserves weights through arithmetic operations
- Familiar pandas interface
- Supports both Series and DataFrame objects

## Usage

```python
import pandas as pd
import numpy as np
from weightedpandas import WeightedSeries, WeightedDataFrame

# Create a weighted series
data = [1, 2, 3, 4, 5]
weights = [5, 4, 3, 2, 1]
ws = WeightedSeries(data, weights=weights)

# Calculate weighted statistics
print(f"Weighted sum: {ws.sum()}")
print(f"Weighted mean: {ws.mean()}")
print(f"Weighted median: {ws.median()}")
print(f"Weighted standard deviation: {ws.std()}")

# Create a weighted dataframe
df_data = {
    'A': [1, 2, 3, 4, 5],
    'B': [5, 4, 3, 2, 1]
}
wdf = WeightedDataFrame(df_data, weights=weights)

# Calculate weighted statistics
print(wdf.sum())
print(wdf.mean())
print(wdf.corr())

# Weights are preserved through operations
ws2 = ws * 2 + 1
print(ws2.weights)  # Same as original weights
```

## How Weights are Applied

In weighted calculations:

- `sum()`: Each value is multiplied by its weight before summing
- `mean()`: The weighted sum divided by the sum of weights
- `var()` and `std()`: Each squared deviation is weighted
- `quantile()`: The quantile is determined from the weighted cumulative distribution

## Helper Functions

For convenience, you can use the following helper functions:

```python
from weightedpandas import weighted_series, weighted_dataframe

# These are equivalent to the constructor calls
ws = weighted_series(data, weights=weights)
wdf = weighted_dataframe(df_data, weights=weights)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.