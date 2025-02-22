# get_features_by_backward_and_tffs

## Description
The `get_features_by_backward_and_tffs` function performs feature selection based on **Backward Selection** combined with **Feature Selection based on Top Frequency (TFFS)**. This function helps identify important features in a dataset by leveraging the **TFFS** algorithm from the [pypi-tffs](https://github.com/VuKieuAnh/pypi-tffs) repository and Backward Selection.

## Parameters

| Parameter         | Data Type         | Description |
|------------------|------------------|--------------------------------------------------------------------------------------|
| `data`          | `pd.DataFrame`    | The input dataset containing features to be selected. The first column should represent the class label for the classification process. |
| `percent_tffs`  | `float`           | The percentage of features to retain after applying **TFFS**. This value should be greater than `percent_backward` to ensure effective selection. |
| `number_run`    | `int`             | The number of times the Random Forest model is built during the TFFS process. |
| `n_estimators`  | `int`             | The number of decision trees in the Random Forest model used to assess feature importance. |
| `percent_backward` | `float`          | The percentage of features to retain after applying Backward Selection. |

## Workflow
1. **Feature Selection based on Top Frequency (TFFS)**:
   - Apply the TFFS algorithm from [pypi-tffs](https://github.com/VuKieuAnh/pypi-tffs) to identify features that frequently appear as important across multiple Random Forest model runs.
   - Retain the top `percent_tffs`% most frequently selected features.

2. **Backward Selection**:
   - Iteratively remove the least important features and evaluate model performance to identify those with the least impact.

3. **Backward Selection**:
   - From the set of features selected in the TFFS step, retain `percent_backward`% of the most impactful features.

## Return Value
The function returns a list of the most important features after applying both the TFFS and Backward Selection methods.

## Example Usage
```python
import pandas as pd
from hybridtffs import get_features_by_backward_and_tffs

# Create a sample DataFrame with the target column as the first column
data = pd.DataFrame({
    'target': [0, 1, 0, 1],
    'feature_1': [0.1, 0.2, 0.3, 0.4],
    'feature_2': [1, 2, 3, 4],
    'feature_3': [5, 6, 7, 8]
})

# Run the function
selected_features = get_features_by_backward_and_tffs(
    data,
    percent_tffs=50,
    number_run=10,
    n_estimators=100,
    percent_backward=30
)

print("Selected features:", selected_features)
```

## Author
**Vu Thi Kieu Anh** 

---
© 2025,

