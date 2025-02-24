# MSE - Mean Squared Error Calculation Package

## Overview

**Mean_Squared_Error** is a Python package for calculating the Mean Squared Error (MSE), a common metric for evaluating regression models. This package provides a simple and efficient way to compute MSE for model predictions.

## Installation

You can install **Mean_Squared_Error** using pip:

```bash
pip install Mean_Squared_Error
```

## Usage

```python
from Mean_Squared_Error import MSE

# Example usage
result = MSE([1, 2, 3], [4, 5, 6])
print(result)
```


### MSE(y_true, y_pred)

Calculates the Mean Squared Error between true values and predicted values.

**Parameters:**
- `y_true` (list/array): Ground truth values
- `y_pred` (list/array): Predicted values

**Returns:**
- float: The calculated Mean Squared Error

## Examples

```python
# Basic usage
true_values = [1, 2, 3, 4, 5]
predicted_values = [1.1, 2.2, 2.9, 4.1, 5.2]
error = MSE(true_values, predicted_values)
print(f"Mean Squared Error: {error}")

# Using with numpy arrays
import numpy as np
y_true = np.array([1.0, 2.0, 3.0])
y_pred = np.array([1.1, 1.9, 3.2])
error = MSE(y_true, y_pred)
print(f"Mean Squared Error: {error}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.