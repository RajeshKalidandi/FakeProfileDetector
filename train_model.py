import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from ml_models.feature_extraction import extract_features
from ml_models.preprocessing import preprocess_data
from ml_models.model_comparison import train_and_evaluate_models, train_ensemble
from ml_models.model_evaluation import evaluate_model, hyperparameter_tuning, interpret_model
import joblib
import json
import matplotlib.pyplot as plt
import shap

# Load and preprocess data
data = pd.read_csv('user_data.csv')
features = []
labels = []

for _, row in data.iterrows():
    user_data = row.to_dict()
    extracted_features = extract_features(user_data)
    features.append(extracted_features)
    labels.append(row['is_fake'])

feature_df = pd.DataFrame(features)
X, y = preprocess_data(feature_df, labels)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train and evaluate models
results = train_and_evaluate_models(X_train, X_test, y_train, y_test)

# Print results for all models
for name, result in results.items():
    print(f"\n{name}:")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Cross-validation mean: {result['cv_mean']:.4f} (+/- {result['cv_std'] * 2:.4f})")
    print("Classification Report:")
    print(result['classification_report'])

# Train ensemble
ensemble_result = train_ensemble(X_train, y_train, X_test, y_test, results)

print("\nEnsemble Model Result:")
print(f"Models used: {', '.join(ensemble_result['models'])}")
print(f"Accuracy: {ensemble_result['accuracy']:.4f}")
print("Classification Report:")
print(ensemble_result['classification_report'])

# Hyperparameter tuning for the best model
best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model, best_params, best_score = hyperparameter_tuning(X_train, y_train, model_type=best_model_name.lower().replace(' ', '_'))

print(f"\nBest {best_model_name} params:", best_params)
print(f"Best {best_model_name} score:", best_score)

# Evaluate the best model
best_model_scores = evaluate_model(best_model, X_test, y_test)
print(f"\nBest {best_model_name} scores:", best_model_scores)

# Model interpretation for the best model
feature_names = feature_df.columns.tolist()
shap_values, lime_exp = interpret_model(best_model, X_test, feature_names)

# Plot SHAP summary plot
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, plot_type="bar")
plt.title(f"{best_model_name} SHAP Feature Importance")
plt.tight_layout()
plt.savefig(f"{best_model_name.lower().replace(' ', '_')}_shap_importance.png")

# Save models
joblib.dump(best_model, f'best_{best_model_name.lower().replace(" ", "_")}_model.joblib')
joblib.dump(results['Voting Classifier']['model'], 'voting_classifier_model.joblib')
joblib.dump(results['Stacking Classifier']['model'], 'stacking_classifier_model.joblib')
joblib.dump(results['AdaBoost Classifier']['model'], 'adaboost_classifier_model.joblib')

print("\nAll models trained, evaluated, and saved successfully.")
