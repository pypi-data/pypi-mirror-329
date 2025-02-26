## EazyML Responsible-AI: Augmented Intelligence
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.46-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

A collection of APIs from EazyML family to discover patterns, generate insights, or mine rules from your datasets. Each discovered pattern is expressed as a set of conditions on feature variables - each with a trust-score to reflect confidence in the insight, allowing you to analyze and apply these insights to your data. Ideal for pattern recognition, interpretable AI, and augmented intelligence workflows.

### Features
**Pattern Mining**: Discover meaningful rules from the  datasets.
**Insight Generation**: Generate high-value insights with associated trust scores.
**Application of Rules**: Apply discovered patterns to datasets for further analysis.

Ideal for use cases like interpretability, training data analysis, and building solutions with augmented intelligence.

## Installation
### User installation
The easiest way to install this package for augmented intelligence is using pip:bash
pip install -U eazyml-insight### Dependencies
This package requires:
werkzeug,
unidecode,
pandas,
scikit-learn,
nltk,
pyyaml,
requests

## Usage
Here's an example of how you can use the APIs from this package.
```python
from eazyml_augi import ez_init, ez_augi

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

# discover insights for given dataset using EazyML.
response = ez_augi(mode='classification',
            outcome='target',
            data='train.csv')

# the response object contains insights/patterns that you can explore to integrate in your augmented intelligence workflows.You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_augi.html).
```

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