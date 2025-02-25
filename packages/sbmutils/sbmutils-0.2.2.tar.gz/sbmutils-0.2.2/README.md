# sbmutils

A collection of utility functions for data analysis.

## Installation

```bash
pip install sbmutils
```

## Usage

### Quantile Normalization

```python
import numpy as np
from sbmutils.norm import quantilenorm

# Create sample data
data = np.random.rand(10, 3)  # 10 rows, 3 columns

# Perform quantile normalization
normalized_data = quantilenorm(data, average="mean")
```

## Features

- `quantilenorm`: Performs 2D quantile normalization over columns
  - Supports both mean and median averaging methods
  - Handles missing values (NaN)
  - Input validation and error handling

## Requirements

- Python >= 3.6
- NumPy
- SciPy

## License

This project is licensed under the MIT License. 