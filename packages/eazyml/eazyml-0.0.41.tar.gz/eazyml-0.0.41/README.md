## Eazyml Modeling
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.41-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

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
# Replace 'your_license_key' with your actual EazyML license key
ez_init(license_key="your_license_key")

ez_init_model(
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

