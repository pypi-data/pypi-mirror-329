## Eazyml Explainable AI
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.63-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

`eazyml-xai` is a Python package designed to make machine learning predictions more transparent and interpretable. It provides human-readable explanations for predictions.

### Features
- Gain insights into **local feature importance and global feature impacts**.
- Understand **why a specific prediction was made**.
- Evaluate predictions with **explainability scores**.    

`eazyml-xai` is a key tool for building trust in AI systems by providing clear, actionable explanations.

## Installation
### User installation
The easiest way to install EazyML Explainable AI is using pip:
```bash
pip install -U eazyml-xai
```
### Dependencies
Eazyml Augmented Intelligence requires :
- pandas==2.0.3
- scikit-learn==1.3.2
- werkzeug==3.0.2
- Unidecode==1.3.8
- pydot==1.4.2
- numpy==1.24.3
- pyyaml

## Usage
Get explainability score for test data.
```python
from eazyml_augi import ez_init, ez_augi

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

response = ez_explain(
            mode='classification',
            outcome='target',
            train_file_path='train.csv',
            test_file_path='test.csv',
            model=my_model,
            data_type_dict=data_type_dict,
            selected_features_list=lis_of_derived_features,
            options={"data_source": "parquet", "record_number": [1, 2, 3]})

explainations = response['explainations']
```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_xai.html).


## Useful links, other packages from EazyML family
- [Documentation](https://docs.eazyml.com)
- [Homepage](https://eazyml.com)
- If you have questions or would like to discuss a use case, please contact us [here](https://eazyml.com/trust-in-ai)
- Here are the other packages from EazyML suite:

    - [eazyml-automl](https://pypi.org/project/eazyml/): eazyml-automl provides a suite of APIs for training, optimizing and validating machine learning models with built-in AutoML capabilities, hyperparameter tuning, and cross-validation.
    - [eazyml-data-quality](https://pypi.org/project/eazyml-dq/): eazyml-data-quality provides APIs for comprehensive data quality assessment, including bias detection, outlier identification, and drift analysis for both data and models.
    - [eazyml-counterfactuals](https://pypi.org/project/eazyml-cf/): eazyml-counterfactuals provides APIs for optimal prescriptive analytics, counterfactual explanations, and actionable insights to optimize predictive outcomes to align with your objectives.
    - [eazyml-insight](https://pypi.org/project/eazyml-augi/): eazyml-insight provides APIs to discover patterns, generate insights, and mine rules from your datasets.
    - [eazyml-xai](https://pypi.org/project/eazyml-xai/): eazyml-xai provides APIs for explainable AI (XAI), offering human-readable explanations, feature importance, and predictive reasoning.
    - [eazyml-xai-image](https://pypi.org/project/eazyml-xai-image/): eazyml-xai-image provides APIs for image explainable AI (XAI).

## License
This project is licensed under the [Proprietary License](https://github.com/EazyML/eazyml-docs/blob/master/LICENSE).

---

Maintained by [EazyML](https://eazyml.com)  
© 2025 EazyML. All rights reserved.