## EazyML Modeling
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.45-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

`EazyML` is a comprehensive Python package designed to simplify machine learning workflows for data scientists, engineers, and developers. With **AutoML capabilities**, eazyml enables automated feature selection, model training, hyperparameter optimization, and cross-validation, all with minimal code. The package trains multiple models in the background, ranks them by performance metrics, and recommends the best model for your use case.

### Features
- **Global Feature Importance**: Get insights into the most impactful features in your dataset.
- **Confidence Scoring**: Enhance predictive reliability with confidence scores.

`EazyML` is perfect for users looking to streamline the development of robust and efficient machine learning models.

## Installation
### User installation
The easiest way to install eazyml modeling is using pip:
```bash
pip install -U eazyml
```
### Dependencies
Eazyml Augmented Intelligence requires :
- werkzeug,
- unidecode,
- pandas,
- scikit-learn,
- nltk,
- pyyaml,
- requests

## Usage
Initialize and build a predictive model based on the provided dataset and options. 
Perform prediction on the given test data based on model options.

```python
from eazyml_augi import ez_init, ez_augi

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

ez_build_model(
            df='train_dataframe'
            options={
                "model_type": "predictive",
                "accelerate": "yes",
                "outcome": "target",
                "remove_dependent": "no",
                "derive_numeric": "yes",
                "derive_text": "no",
                "phrases": {"*": []},
                "text_types": {"*": ["sentiments"]},
                "expressions": []
            }
    )
ez_predict(
            test_data ='test_dataframe'
            options={
                "extra_info": {
                },
                "model": "Specified model to be used for prediction",
                "outcome": "target",
            }
    )

```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_model.html).


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
