<!-- <img src="logo.png" alt="Logo" width="110" align="left" style="margin-right: 15px;">  

# PkTree:
_Incorporating Prior Knowledge into Tree-Based Models_
 -->

<table>
<tr>
<td>
<img src="https://github.com/DEIB-GECO/pktree/blob/a9253cf0bd35b22e157889012dc172061fd12652/logo.png?raw=true" alt="Logo" width="300" style="margin-right: 15px;">
</td>
<td>
<h1 align="left">PkTree</h1>
<h4 align="left" style="font-weight: medium; color: gray;">
A Python package for incorporating prior domain knowledge into tree-based models
</h3>
</td>
</tr>
</table>


**PkTree** is a Python package that enables the integration of prior knowledge into Decision Trees (DT) and Random Forests (RF). By prioritizing relevant features, this package enhances interpretability and aligns predictive models with prior insights.  

The enhancements in **PkTree** build upon the `scikit-learn` library.

---

## **Features**  

### 1. **Prior-Informed Decision Trees**  
We introduce two key modifications to the traditional Decision Tree algorithm to prioritize relevant features during tree construction:  
- **Feature Sampling**: Weighted feature sampling during training. A hyperparameter `k` controls the influence of prior knowledge score `w_prior` on sampling.  
- **Impurity Improvement**: Adjusting impurity calculations based on prior knowledge scores. An additional hyperparameter `v` controls the strength of the prior knowledge score's (`w_prior`) impact. 

The modified models include a parameter `pk_configuration`, which can take the following values:  
- `'no_gis'`: Standard tree without knowledge.  
- `'on_feature_sampling'`: Applies prior knowledge-informed feature sampling.  
- `'on_impurity_improvement'`: Incorporates prior knowledge scores in impurity computations.  
- `'all'`: Combines both feature sampling and impurity improvement.  


### 2. **Prior-Informed Random Forest**  
The modificationsabove can be seamlessly extended to the Random Forest model, which functions as an ensemble of Decision Trees. We also introduces an additional modification for Random Forests which leverages the Out-of-Bag (OOB) samples. This modification is activated with parameters `oob_score=True` and `on_oob=True`.
#### **Out-of-Bag (OOB) Weights**  
This approach leverages Out-of-Bag predictions for weighting individual estimators in the Random Forest ensemble:  
- For each tree, calculate:
  - `f_score`: Accuracy on OOB samples.  
  - `s_prior`: Average prior-knowledge relevance of selected features.  
- Compute weights for each tree based on these scores and normalize them.  
- A hyperparameter `r` increases the weight differences across trees, enhancing the influence of prior-knowledge scores. 

#### **Weighted Voting**  
During prediction Tree predictions are weighted based on their normalized scores and aggregated.  

#### **Prior-knowledge Score**
The prior knowledge score `w_prior` is assumed to be in the range [0,1], where higher values indicate greater relevance based on the prior knowledge considered. If the `w_prior`score does not fall within this range, it is first normalized. Then, the score is transformed using a predefined function (`pk_function`) to obtain a reversed interpretation, where higher values indicate lower relevance. Check [here](https://github.com/DEIB-GECO/pktree/blob/main/pktree/tree/_classes.py) for the different implemented forms of the `pk_function`.

---

## **Getting Started**  

### **Installation**  
Install the package via `pip`:  
```bash
pip install pktree
```

### **Example Usage**  
Here’s how to use **PkTree** packageto build and train prior-knowledge informed Decision Tree or Random Forest models:

### **Toy Dataset**
Build a toy dataset and generate prior knowledge score `w_prior`.
```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression

# Generate w_prior
def assign_feature_scores(n_features = 50):
    scores = np.round(np.random.uniform(0.01, 0.99, size=n_features), 5)
    return scores

# Generate toy dataset
def generate_dataset(task_type, n_samples = 100, n_features = 50, noise_level = 0.1):
    
    if task_type == 'classification':
        X, y = make_classification(
            n_samples=n_samples, 
            n_features=n_features, 
            n_informative=int(n_features * 0.7), 
            n_redundant=int(n_features * 0.2), 
            n_classes=2, 
            random_state=42
        )

        X += np.random.normal(0, noise_level, X.shape)
        
    elif task_type == 'regression':
        X, y = make_regression(
            n_samples=n_samples, 
            n_features=n_features, 
            noise=noise_level, 
            random_state=42
        )
    return X, y


w_prior = assign_feature_scores()
X_classification, y_classification = generate_dataset('classification')
X_regression, y_regression = generate_dataset('regression')
        
```
### **Decision Trees**
Build a Decision Tree classifier: 
```python
from pktree import tree

X_train, X_test, y_train, y_test = train_test_split(X_classification, y_classfication, test_size=0.2, random_state=42)

model = tree.DecisionTreeClassifier(random_state=42, pk_configuration='all', w_prior=w_prior, k=2, v=0.5, pk_function='reciprocal')

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
Build a Decision Tree regressor: 
```python
X_train, X_test, y_train, y_test = train_test_split(X_regression, y_regression, test_size=0.2, random_state=42)

model = tree.DecisionTreeRegressor(random_state=42, pk_configuration='on_impurity_improvement', w_prior=w_prior, k=2, v=0.5,pk_function='reciprocal')

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
### **Random Forest**
Build a Random Forest classifier: 
```python
from pktree import ensemble


X_train, X_test, y_train, y_test = train_test_split(X_classification, y_classfication, test_size=0.2, random_state=42)

forest = ensemble.RandomForestClassifier(random_state=42, pk_configuration='on_feature_sampling', oob_score=True, on_oob=True, w_prior=w_prior, r=3)

forest.fit(X_train, y_train)
predictions = forest.predict(X_test)
```
Build a Random Forest Regressor: 
```python
#
X_train, X_test, y_train, y_test = train_test_split(X_regression, y_regression, test_size=0.2, random_state=42)

forest = ensemble.RandomForestRegressor(random_state=42, pk_configuration='on_impurity_improvement', w_prior=w_prior)

forest.fit(X_train, y_train)
predictions = forest.predict(X_test)
```

---

## **Compatibility**  
- Built on top of `scikit-learn`.  
- Compatible with both classification and regression tasks.  

---

## **License**  
This package is open-source and distributed under the [MIT License](LICENSE).  

