# Irrectum - Metrics for Evaluating Model Quality

## Description
Irrectum provides a set of metrics for evaluating the quality of machine learning model predictions. These metrics include both standard and specialized indicators that help analyze model performance and identify its strengths and weaknesses.

### Features
- **RMSE (Root Mean Square Error)**: Assesses the error of the model's values relative to the actual values.
- **NRMSE (Normalized RMSE)**: Normalizes RMSE, allowing for comparison of models with different scales.
- **Pearson Correlation Coefficient**: Measures the degree of linear dependence between predicted and actual values.
- **Covariance**: Evaluates how two variables change together.
- **Coefficient of Determination (R²)**: Shows the proportion of variance in the dependent variable explained by the model.
- **Adjusted R²**: Takes into account the number of predictors in the model, allowing for comparison of models with different numbers of factors.
- **Residual Sum of Squares (RSS)**: Assesses the total error of the model.
- **MAPE (Mean Absolute Percentage Error)**: Measures the percentage error of the model relative to the original.
- **MAE (Mean Absolute Error)**: Evaluates the average error between predicted and actual values.
- **AIC & BIC**: Information criteria for comparing models considering their complexity.

## Installation
To install the necessary dependencies, use the following command:

```bash
pip install irrectum
```


Example of using the metrics:
``` python
import numpy as np
from abc_metrics import RMSE, MAE

# Example data
testTarget = np.array([3, -0.5, 2, 7])
testPrediction = np.array([2.5, 0.0, 2, 8])

# Creating instances of the metrics
rmse_metric = RMSE()
mae_metric = MAE()

# Evaluating model quality
rmse_value = rmse_metric.test(testTarget, testPrediction)
mae_value = mae_metric.test(testTarget, testPrediction)

print(f"RMSE: {rmse_value}, MAE: {mae_value}")
```

## Support
If you have any questions or need assistance, please create an issue in the repository.

## Contributing
We welcome contributions! Please refer to our contribution guidelines.

## Authors and Acknowledgment
Show your appreciation to those who have contributed to the project.

## License
This project is licensed under the MIT License.