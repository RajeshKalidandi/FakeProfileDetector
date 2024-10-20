import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from ml_models.feature_extraction import extract_features
from ml_models.preprocessing import preprocess_data
import joblib

# Load your dataset
# Assuming you have a CSV file with user data and labels
data = pd.read_csv('user_data.csv')

# Extract features
features = []
labels = []

for _, row in data.iterrows():
    user_data = row.to_dict()
    extracted_features = extract_features(user_data)
    features.append(extracted_features)
    labels.append(row['is_fake'])  # Assuming 'is_fake' is the label column

# Convert features to DataFrame
feature_df = pd.DataFrame(features)

# Preprocess the data
X, y = preprocess_data(feature_df, labels)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Save the model
joblib.dump(model, 'trained_model.joblib')
print("Model saved as 'trained_model.joblib'")
