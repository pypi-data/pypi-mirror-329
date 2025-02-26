# ALTrustworthyAI

**ALTrustworthyAI** is an open-source component of **AffectLog’s Trustworthy AI (ALT-AI)**, providing a **unified framework** for machine learning interpretability and fairness analysis. With this package, you can train interpretable “glassbox” models and explain “blackbox” systems, ensuring alignment with ethical guidelines, emerging regulations, and the design principles outlined in the [ALT-AI Design Document](https://github.com/AffectLog360/AL-TAI-Design-document).

**Interpretability** is crucial for:
- **Model debugging** – Why did my model make this mistake?  
- **Feature Engineering** – How can I improve my model?  
- **Fairness analysis** – Does my model discriminate or impact certain groups disproportionately?  
- **Regulatory compliance** – Does my model satisfy legal requirements (e.g., GDPR, EU AI Act)?  
- **High-stakes domains** – Healthcare, finance, judicial, and more.

![](https://github.com/AffectLog360/altrustworthyai.git)

---

## Installation

- **Python 3.7+** | Linux, Mac, Windows  

```bash
pip install altrustworthyai

```

---

## Introducing the Explainable Boosting Machine (EBM)

EBM is a core “glassbox” model within **AffectLog’s Trustworthy AI**. It uses **bagging**, **gradient boosting**, and **automatic interaction detection** to refine classic GAMs (Generalized Additive Models). This yields performance comparable to popular blackbox models (e.g., random forests, XGBoost) while producing **exact** explanations that domain experts can edit or scrutinize.

| Dataset / AUROC    | Domain    | Logistic Regression | Random Forest | XGBoost         | Explainable Boosting Machine |
|--------------------|-----------|:-------------------:|:-------------:|:---------------:|:----------------------------:|
| Adult Income       | Finance   | .907±.003          | .903±.002     | .927±.001       | **_.928±.002_**              |
| Heart Disease      | Medical   | .895±.030          | .890±.008     | .851±.018       | **_.898±.013_**              |
| Breast Cancer      | Medical   | **_.995±.005_**    | .992±.009     | .992±.010       | **_.995±.006_**              |
| Telecom Churn      | Business  | .849±.005          | .824±.004     | .828±.010       | **_.852±.006_**              |
| Credit Fraud       | Security  | .979±.002          | .950±.007     | **_.981±.003_** | **_.981±.003_**              |

---

## Supported Techniques

| **Interpretability Technique**                                           | **Type**             |
|--------------------------------------------------------------------------|----------------------|
| [Explainable Boosting](https://affectlog.com/docs/ebm.html)             | glassbox model       |
| [APLR](https://affectlog.com/docs/aplr.html)                             | glassbox model       |
| [Decision Tree](https://affectlog.com/docs/dt.html)                      | glassbox model       |
| [Decision Rule List](https://affectlog.com/docs/dr.html)                 | glassbox model       |
| [Linear/Logistic Regression](https://affectlog.com/docs/lr.html)         | glassbox model       |
| [SHAP Kernel Explainer](https://affectlog.com/docs/shap.html)            | blackbox explainer   |
| [LIME](https://affectlog.com/docs/lime.html)                             | blackbox explainer   |
| [Morris Sensitivity Analysis](https://affectlog.com/docs/msa.html)       | blackbox explainer   |
| [Partial Dependence](https://affectlog.com/docs/pdp.html)                | blackbox explainer   |

---

## Train a Glassbox Model

Example with an **Explainable Boosting Machine**:

```python
from altrustworthyai.glassbox import ExplainableBoostingClassifier

ebm = ExplainableBoostingClassifier()
ebm.fit(X_train, y_train)

# (EBM supports pandas dataframes, numpy arrays, and "string" data natively)
# You can also substitute with: 
#   LogisticRegression, DecisionTreeClassifier, RuleListClassifier, ...
```

**Understand the model**:

```python
from altrustworthyai import show

ebm_global = ebm.explain_global()
show(ebm_global)
```
![Global Explanation Image](./docs/readme/ebm-global.png?raw=true)

**Understand individual predictions**:

```python
ebm_local = ebm.explain_local(X_test, y_test)
show(ebm_local)
```
![Local Explanation Image](./docs/readme/ebm-local.png?raw=true)

**Compare multiple model explanations**:

```python
show([logistic_regression_global, decision_tree_global])
```
![Dashboard Image](./docs/readme/dashboard.png?raw=true)

**Differential Privacy**:

```python
from altrustworthyai.privacy import DPExplainableBoostingClassifier

dp_ebm = DPExplainableBoostingClassifier(epsilon=1, delta=1e-5) 
dp_ebm.fit(X_train, y_train)

show(dp_ebm.explain_global())
```

For more technical info on local/global explanations, fairness checks, or compliance workflows, see the [ALT-AI Design Document](https://github.com/AffectLog360/AL-TAI-Design-document) and the broader [user docs](https://affectlog.com/docs).

---

### Large-Scale / Distributed

EBMs can handle 100 million rows in a few hours on a single machine. For truly massive datasets, see the distributed version via Azure SynapseML:
- [Classification EBMs](https://learn.affectlog.com/en-us/fabric/data-science/explainable-boosting-machines-classification)
- [Regression EBMs](https://learn.affectlog.com/en-us/fabric/data-science/explainable-boosting-machines-regression)

---

## Acknowledgements

EBMs are a fast derivative of GA2M (Generalized Additive 2 Model), invented by Yin Lou, Rich Caruana, Johannes Gehrke, and Giles Hooker.

We also build on top of these great packages:

[plotly](https://github.com/plotly/plotly.py) •  
[dash](https://github.com/plotly/dash) •  
[scikit-learn](https://github.com/scikit-learn/scikit-learn) •  
[lime](https://github.com/marcotcr/lime) •  
[shap](https://github.com/slundberg/shap) •  
[SALib](https://github.com/SALib/SALib) •  
[skope-rules](https://github.com/scikit-learn-contrib/skope-rules) •  
[treeinterpreter](https://github.com/andosa/treeinterpreter) •  
[gevent](https://github.com/gevent/gevent) •  
[joblib](https://github.com/joblib/joblib) •  
[pytest](https://github.com/pytest-dev/pytest) •  
[jupyter](https://github.com/jupyter/notebook)
[altrustworthyai](https://github.com/AffectLog360/altrustworthyai/)

---

## Citations

<details>
  <summary><strong>Explainable Boosting</strong></summary>
  (Citations for EBM, GA2M, pairwise interactions, etc.)
  <hr/>
  <!-- Keep or remove as needed -->
</details>

<details>
  <summary><strong>Differential Privacy</strong></summary>
  <hr/>
  <!-- DP references here -->
</details>

<details>
  <summary><strong>LIME / SHAP / SALib / PDE</strong></summary>
  <hr/>
  <!-- Original references for third-party interpretability libraries -->
</details>

<details>
  <summary><strong>Open Source Software</strong></summary>
  <hr/>
  <!-- Additional references for scikit-learn, joblib, etc. -->
</details>

---

### License

This project is licensed under the terms of the **MIT License**. See the [LICENSE](./LICENSE) file for details.
