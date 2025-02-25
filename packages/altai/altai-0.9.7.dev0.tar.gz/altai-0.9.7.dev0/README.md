## Table of Contents

* [Installation and Usage](#installation-and-usage)
* [Supported Methods](#supported-methods)
  * [Model Explanations](#model-explanations)
  * [Model Confidence](#model-confidence)
  * [Prototypes](#prototypes)
  * [References and Examples](#references-and-examples)
* [Citations](#citations)
* [License and Notice](#license-and-notice)

## Installation and Usage
altai can be installed from:

- PyPI or GitHub source (using `pip`)
- Anaconda (using `conda`/`mamba`)

### With pip

- To install altai from [PyPI](https://pypi.org/project/altai):
  ```bash
  pip install altai
  ```
  
- Alternatively, install the development version:
  ```bash
  pip install git+https://github.com/roy-saurabh/altai.git
  ```
  
- For distributed computation support (with ray):
  ```bash
  pip install altai[ray]
  ```
  
- For SHAP support:
  ```bash
  pip install altai[shap]
  ```

### Usage
The altai explanation API is inspired by scikit-learn’s style, using distinct initialize, fit, and explain steps:

```python
from affectlog_tai.explainers import AnchorTabular

# Initialize and fit the explainer with your prediction function and data
explainer = AnchorTabular(predict_fn, feature_names=feature_names, categorical_names=category_map)
explainer.fit(X_train)

# Explain an instance
explanation = explainer.explain(x)
```

The returned `Explanation` object contains `meta` (metadata and hyperparameters) and `data` (the computed explanation). For AnchorTabular, for example, you can access the anchor conditions via `explanation.data['anchor']`.

## Supported Methods

### Model Explanations
| Method | Models | Explanations | Classification | Regression | Tabular | Text | Images | Categorical features | Train set required | Distributed |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [ALE](https://docs.affectlog.com/projects/altai/en/stable/methods/ALE.html) | BB | global | ✔ | ✔ | ✔ | | | | | |
| [Partial Dependence](https://docs.affectlog.com/projects/altai/en/stable/methods/PartialDependence.html) | BB WB | global | ✔ | ✔ | ✔ | | | ✔ | | |
| [PD Variance](https://docs.affectlog.com/projects/altai/en/stable/methods/PartialDependenceVariance.html) | BB WB | global | ✔ | ✔ | ✔ | | | ✔ | | |
| [Permutation Importance](https://docs.affectlog.com/projects/altai/en/stable/methods/PermutationImportance.html) | BB | global | ✔ | ✔ | ✔ | | | ✔ | | |
| [Anchors](https://docs.affectlog.com/projects/altai/en/stable/methods/Anchors.html) | BB | local | ✔ | | ✔ | ✔ | ✔ | ✔ | For Tabular | |
| [CEM](https://docs.affectlog.com/projects/altai/en/stable/methods/CEM.html) | BB* TF/Keras | local | ✔ | | ✔ | | ✔ | | Optional | |
| [Counterfactuals](https://docs.affectlog.com/projects/altai/en/stable/methods/CF.html) | BB* TF/Keras | local | ✔ | | ✔ | | ✔ | | No | |
| [Prototype Counterfactuals](https://docs.affectlog.com/projects/altai/en/stable/methods/CFProto.html) | BB* TF/Keras | local | ✔ | | ✔ | | ✔ | ✔ | Optional | |
| [Counterfactuals with RL](https://docs.affectlog.com/projects/altai/en/stable/methods/CFRL.html) | BB | local | ✔ | | ✔ | | ✔ | ✔ | ✔ | |
| [Integrated Gradients](https://docs.affectlog.com/projects/altai/en/stable/methods/IntegratedGradients.html) | TF/Keras | local | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Optional | |
| [Kernel SHAP](https://docs.affectlog.com/projects/altai/en/stable/methods/KernelSHAP.html) | BB | local/global | ✔ | ✔ | ✔ | | | ✔ | ✔ | ✔ |
| [Tree SHAP](https://docs.affectlog.com/projects/altai/en/stable/methods/TreeSHAP.html) | WB | local/global | ✔ | ✔ | ✔ | | | ✔ | Optional | |
| [Similarity explanations](https://docs.affectlog.com/projects/altai/en/stable/methods/Similarity.html) | WB | local | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |

### Model Confidence
These methods provide instance-specific scores that measure the model’s confidence.

| Method | Models | Classification | Regression | Tabular | Text | Images | Categorical Features | Train set required |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Trust Scores](https://docs.affectlog.com/projects/altai/en/stable/methods/TrustScores.html) | BB | ✔ |  | ✔ | ✔(1) | ✔(2) |  | Yes |
| [Linearity Measure](https://docs.affectlog.com/projects/altai/en/stable/methods/LinearityMeasure.html) | BB | ✔ | ✔ | ✔ |  | ✔ |  | Optional |

*Key:*  
- **BB** – Black-box (only require a prediction function)  
- **BB\*** – Black-box but assume model is differentiable  
- **WB** – White-box (access to model internals)  
- **TF/Keras** – TensorFlow models via the Keras API  
- **Local** – Explains a single prediction  
- **Global** – Explains overall model behavior  
- **(1)** and **(2)** – Model-dependent requirements  

### Prototypes
These methods distill a dataset into a 1-KNN interpretable classifier.

| Method | Classification | Regression | Tabular | Text | Images | Categorical Features | Train set labels |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [ProtoSelect](https://docs.affectlog.com/projects/altai/en/latest/methods/ProtoSelect.html) | ✔ |  | ✔ | ✔ | ✔ | ✔ | Optional |

---

## References and Examples
- **Accumulated Local Effects (ALE):**  
  * [Documentation](https://docs.affectlog.com/projects/altai/en/stable/methods/ALE.html)  
  * Examples: [California housing dataset](https://docs.affectlog.com/projects/altai/en/stable/examples/ale_regression_california.html), [Iris dataset](https://docs.affectlog.com/projects/altai/en/stable/examples/ale_classification.html)

- **Partial Dependence:**  
  * [Documentation](https://docs.affectlog.com/projects/altai/en/stable/methods/PartialDependence.html)  
  * Example: [Bike rental](https://docs.affectlog.com/projects/altai/en/stable/examples/pdp_regression_bike.html)

- **Permutation Importance:**  
  * [Documentation](https://docs.affectlog.com/projects/altai/en/stable/methods/PermutationImportance.html)  
  * Example: [Who's Going to Leave Next?](https://docs.affectlog.com/projects/altai/en/stable/examples/permutation_importance_classification_leave.html)

- **Anchors:**  
  * [Documentation](https://docs.affectlog.com/projects/altai/en/stable/methods/Anchors.html)  
  * Examples: [Adult income prediction](https://docs.affectlog.com/projects/altai/en/stable/examples/anchor_tabular_adult.html), [Iris dataset](https://docs.affectlog.com/projects/altai/en/stable/examples/anchor_tabular_iris.html), [Movie sentiment classification](https://docs.affectlog.com/projects/altai/en/stable/examples/anchor_text_movie.html)
