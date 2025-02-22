# Eazyml Data Quality
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.26-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

## Overview
The **eazyml-dq** is a Python utility designed to evaluate the quality of datasets by performing various checks such as data shape, emptiness, outlier detection, balance, and correlation. It helps users identify potential issues in their datasets and provides detailed feedback to ensure data readiness for downstream processes.
It offers APIs for data quality assessment across multiple dimensions, including:

## Features
- **Missing Value Analysis**: Detect and impute missing values.
- **Bias Detection**: Uncover and mitigate bias in datasets.
- **Data Drift and Model Drift Analysis**: Monitor changes in data distributions over time.
- **Data Shape Quality**: Validates dataset dimensions and checks if the number of rows is sufficient relative to the number of columns.
- **Data Emptiness Check**: Identifies and reports missing values in the dataset.
- **Outlier Detection**: Detects and removes outliers based on statistical analysis.
- **Data Balance Check**: Analyzes the balance of the dataset and computes a balance score.
- **Correlation Analysis**: Identify multicollinearity, relationships between features and provides alerts for highly correlated features.
- **Summary Alerts**: Consolidates key quality issues into a single summary for quick review.
With eazyml-dq, you can ensure that your training data is clean, balanced, and ready for machine learning.

## Installation
To use the Data Quality Checker, ensure you have Python installed on your system.
### User installation
The easiest way to install data quality is using pip:
```bash
pip install -U eazyml-dq
```
### Dependencies
Eazyml Augmented Intelligence requires :
- pandas==2.0.3
- scikit-learn==1.3.2
- numpy==1.24.3
- openpyxl
- flask

## Usage

This function evaluates the quality of the dataset provided and returns a detailed report.

```python
from eazyml_dq import ez_init, ez_data_quality
# Replace 'your_license_key' with your actual EazyML license key
ez_init(license_key="your_license_key")

# Specify the file path for the dataset
file_path = 'path/to/dataset.csv'
outcome = 'outcome_column_name'
options = {
      "data_shape": "yes",
      "data_balance": "yes",
      "data_emptiness": "yes",
      "data_outliers": "yes",
      "remove_outliers": "yes",
      "outcome_correlation": "yes"
      )

# Perform data quality checks
result = ez_data_quality(filename=file_path, outcome = outcome, options = options)

# Access specific quality metrics
if result["success"]:
    print("Data Shape Quality:", result["data_shape_quality"])
    print("Outlier Quality:", result["data_outliers_quality"])
    print("Bad Quality Alerts:", result["data_bad_quality_alerts"])
else:
    print("Error:", result["message"])
```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_dq.html).


## Useful links and similar projects
- [Documentation](https://docs.eazyml.com)
- [Homepage](https://eazyml.com)
- If you have more questions or want to discuss a specific use case please book an appointment [here](https://eazyml.com/trust-in-ai)
- Here are some other EazyML's packages :

    - [eazyml](https://pypi.org/project/eazyml/): Eazyml provides a suite of APIs for training, testing and optimizing machine learning models with built-in AutoML capabilities, hyperparameter tuning, and cross-validation.
    - [eazyml-dq](https://pypi.org/project/eazyml-dq/): `eazyml-dq` provides APIs for comprehensive data quality assessment, including bias detection, outlier identification, and data drift analysis.
    - [eazyml-cf](https://pypi.org/project/eazyml-cf/): `eazyml-cf` provides APIs for counterfactual explanations, prescriptive analytics, and actionable insights to optimize predictive outcomes.
    - [eazyml-augi](https://pypi.org/project/eazyml-augi/): `eazyml-augi` provides APIs to uncover patterns, generate insights, and discover rules from training datasets.
    - [eazyml-xai](https://pypi.org/project/eazyml-xai/): `eazyml-xai` provides APIs for explainable AI (XAI), offering human-readable explanations, feature importance, and predictive reasoning.
    - [eazyml-xai-image](https://pypi.org/project/eazyml-xai-image/): eazyml-xai-image provides APIs for image explainable AI (XAI).

## License
This project is licensed under the [Proprietary License](https://github.com/EazyML/eazyml-docs/blob/master/LICENSE).

---

*Maintained by [EazyML](https://eazyml.com)*  
*© 2025 EazyML. All rights reserved.*
