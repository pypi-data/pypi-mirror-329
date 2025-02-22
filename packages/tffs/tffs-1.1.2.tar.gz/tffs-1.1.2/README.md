# TFFS

## Description
TFFS (**Feature Selection based on Top Frequency**) is a feature selection method that leverages **Random Forest** to identify the most frequently important features across multiple model runs. This method helps in reducing dimensionality while retaining significant features for better model performance.

## Installation

```bash
pip install tffs
```

## 🔥 Functionality
The library provides multiple feature selection functions that combine **TFFS** with classical selection techniques:

### 🏷 Core Function:
```python
get_frequency_of_feature_by_percent(df, number_of_runs, percent, n_estimators)
```

## 📌 Parameters
The function `get_frequency_of_feature_by_percent()` accepts the following parameters:

| Parameter          | Type               | Description |
|--------------------|--------------------|-------------|
| **`df`**          | `pandas.DataFrame`  | The input dataset containing features and target variables. The first column should be the class label. |
| **`number_of_runs`** | `int`             | The number of times a Random Forest model is built to compute feature importance. |
| **`percent`**     | `float`             | The percentage of top important features to retain (e.g., `percent=20` keeps the top 20% most important features). |
| **`n_estimators`** | `int`              | The number of decision trees in the Random Forest model. |

## 📤 Return
The function returns:
- A **NumPy array** containing the **indices** of the selected features that are among the top `percent%` most important features across multiple Random Forest runs.

### 🔄 Example Return:
```python
array([0, 2, 4, 7, 9])
```

## 📌 Example Usage
```python
import pandas as pd
from tffs import get_features_by_forward_and_tffs

# Create a sample DataFrame
data = pd.DataFrame({
    'class': [0, 1, 0, 1, 2, 0, 1, 2, 0, 1],
    'feature_1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    'feature_2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'feature_3': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    'feature_4': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'feature_5': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    'feature_6': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'feature_7': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'feature_8': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'feature_9': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
})

# Run the function
selected_features = get_features_by_forward_and_tffs(
    data,
    percent_tffs=50,
    number_run=10,
    n_estimators=100,
    percent_forward=30
)

print("Selected features:", selected_features)
```

## Author
**Vu Thi Kieu Anh** 

---
© 2025

