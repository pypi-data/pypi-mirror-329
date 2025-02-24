# drift-detect

`drift-detect` is a Python package that helps detect distributional drift between two datasets.

 It provides functionality for drift detection using univariate statistical tests for  both numerical and categorical features. The package also tracks if the distribution of NULL values has changed. The package also includes adjustment for multiple hypothesis testing via Bonferroni and False Discovery Rate (FDR) corrections.


## Key Features 

### Non-Parametric Univariate Statistical Tests:

- **Detect differences in the distribution of numerical features** using the Kolmogorov-Smirnov Test (KS Test)

-  **Identifies if category frequencies differ** significantly across categorical features using the Chi-squared Test of Independance. 

- **Assesses if the distribution of NULL values has changed**  using the Fisher's Exact Test


### Correction Methods for Multiple Testing:

- **Bonferroni Correction**: Adjusts p-values for multiple hypothesis testing by dividing the significance level by the number of tests performed.

- **False Discovery Rate (FDR)**: Adjusts p-values using the Benjamini-Hochberg procedure to control the false discovery rate. Unlike Bonferroni, FDR is less conservative and  allows for an expected fraction of false positives to occur. 


## Installation

You can install the `drift-detect` package using pip:

```bash 
pip install drift-detect
```

## Usage/Examples

```python
import pandas as pd
from detectdrift import DetectDrift

# Create Sample Datasets
sample_size = 1000
categories = ['A', 'B', 'C']
probabilities = [0.5, 0.3, 0.2]  
data1 = pd.DataFrame({
            'numerical_feature': np.random.normal(0, 1, 1000), 
            'categorical_feature' :  np.random.choice(categories, size=sample_size, p=probabilities)
        })
data2 = pd.DataFrame({
    'numerical_feature': np.random.normal(0, 1, 1000),  
     'categorical_feature' :  np.random.choice(categories, size=sample_size, p=probabilities)
    })

# List columns to be tested
numerical_cols = ['numerical_feature']
categorical_cols = ['categorical_feature']

# Initialize DetectDrift with the data and feature columns
drift_detector = DetectDrift(data1, data2, numerical_cols, categorical_cols)

# Perform drift detection
drift_detected = drift_detector.detect_drift()

# Output the result
if drift_detected:
    print("Distribution Drift Detected!")
else:
    print("No Drift Detected.")
```