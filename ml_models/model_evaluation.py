from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import numpy as np
import shap
import lime
import lime.lime_tabular

def evaluate_model(model, X, y, cv=5):
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    scores = {
        'accuracy': [],
        'precision': [],
        'recall': [],
        'f1': [],
        'roc_auc': []
    }

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        scores['accuracy'].append(accuracy_score(y_test, y_pred))
        scores['precision'].append(precision_score(y_test, y_pred))
        scores['recall'].append(recall_score(y_test, y_pred))
        scores['f1'].append(f1_score(y_test, y_pred))
        scores['roc_auc'].append(roc_auc_score(y_test, y_pred_proba))

    return {k: np.mean(v) for k, v in scores.items()}

def hyperparameter_tuning(X, y, model_type='rf'):
    if model_type == 'rf':
        model = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
    elif model_type == 'xgb':
        model = XGBClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5],
            'learning_rate': [0.01, 0.1, 0.3]
        }
    elif model_type == 'lgbm':
        model = LGBMClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5],
            'learning_rate': [0.01, 0.1, 0.3]
        }
    else:
        raise ValueError("Unsupported model type")

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X, y)

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

def interpret_model(model, X, feature_names):
    # SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # LIME
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        X,
        feature_names=feature_names,
        class_names=['Real', 'Fake'],
        mode='classification'
    )
    lime_exp = lime_explainer.explain_instance(X[0], model.predict_proba)

    return shap_values, lime_exp
