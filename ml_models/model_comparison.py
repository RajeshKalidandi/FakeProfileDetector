from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, AdaBoostClassifier, StackingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        'SVM': SVC(probability=True),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        'LightGBM': LGBMClassifier(),
        'KNN': KNeighborsClassifier(),
        'Logistic Regression': LogisticRegression()
    }

    results = {}

    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # Perform cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)

        # Store results
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': np.mean(cv_scores),
            'cv_std': np.std(cv_scores),
            'classification_report': classification_report(y_test, y_pred)
        }

    # Voting Classifier
    voting_clf = VotingClassifier(
        estimators=[(name, model['model']) for name, model in results.items()],
        voting='soft'
    )
    voting_clf.fit(X_train, y_train)
    voting_pred = voting_clf.predict(X_test)
    voting_accuracy = accuracy_score(y_test, voting_pred)
    voting_cv_scores = cross_val_score(voting_clf, X_train, y_train, cv=5)

    results['Voting Classifier'] = {
        'model': voting_clf,
        'accuracy': voting_accuracy,
        'cv_mean': np.mean(voting_cv_scores),
        'cv_std': np.std(voting_cv_scores),
        'classification_report': classification_report(y_test, voting_pred)
    }

    # Stacking Classifier
    base_models = [(name, model['model']) for name, model in results.items() if name != 'Logistic Regression']
    stacking_clf = StackingClassifier(
        estimators=base_models,
        final_estimator=LogisticRegression(),
        cv=5
    )
    stacking_clf.fit(X_train, y_train)
    stacking_pred = stacking_clf.predict(X_test)
    stacking_accuracy = accuracy_score(y_test, stacking_pred)
    stacking_cv_scores = cross_val_score(stacking_clf, X_train, y_train, cv=5)

    results['Stacking Classifier'] = {
        'model': stacking_clf,
        'accuracy': stacking_accuracy,
        'cv_mean': np.mean(stacking_cv_scores),
        'cv_std': np.std(stacking_cv_scores),
        'classification_report': classification_report(y_test, stacking_pred)
    }

    # AdaBoost Classifier
    adaboost_clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50, random_state=42)
    adaboost_clf.fit(X_train, y_train)
    adaboost_pred = adaboost_clf.predict(X_test)
    adaboost_accuracy = accuracy_score(y_test, adaboost_pred)
    adaboost_cv_scores = cross_val_score(adaboost_clf, X_train, y_train, cv=5)

    results['AdaBoost Classifier'] = {
        'model': adaboost_clf,
        'accuracy': adaboost_accuracy,
        'cv_mean': np.mean(adaboost_cv_scores),
        'cv_std': np.std(adaboost_cv_scores),
        'classification_report': classification_report(y_test, adaboost_pred)
    }

    return results

def ensemble_voting(models, X):
    predictions = np.array([model.predict(X) for model in models])
    return np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=predictions)

def train_ensemble(X_train, y_train, X_test, y_test, results):
    best_models = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)[:3]
    ensemble_models = [result['model'] for name, result in best_models]

    # Make ensemble predictions
    ensemble_pred = ensemble_voting(ensemble_models, X_test)

    # Calculate ensemble accuracy
    ensemble_accuracy = accuracy_score(y_test, ensemble_pred)

    # Generate classification report for ensemble
    ensemble_report = classification_report(y_test, ensemble_pred)

    return {
        'models': [name for name, _ in best_models],
        'accuracy': ensemble_accuracy,
        'classification_report': ensemble_report
    }
