import pandas as pd
from ml_models import preprocess_data, train_model, extract_features

# Load your dataset
data = pd.read_csv('path_to_your_dataset.csv')

# Extract features for each profile in the dataset
features = []
for _, row in data.iterrows():
    profile_data = row.to_dict()
    profile_data['profile_pictures'] = profile_data['profile_pictures'].split(',')  # Assuming comma-separated image paths
    profile_features = extract_features(profile_data)
    features.append(profile_features)

features_df = pd.DataFrame(features)

# Combine features with the original dataset
combined_data = pd.concat([data, features_df], axis=1)

# Preprocess the data
X_train, X_test, y_train, y_test, _ = preprocess_data(combined_data)

# Train the model
model = train_model(X_train, y_train, X_test, y_test)

# Save the trained model
model.save_model('trained_model.joblib')
