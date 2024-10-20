import pandas as pd
from ml_models import preprocess_data, train_model

# Load your dataset
data = pd.read_csv('path_to_your_dataset.csv')

# Preprocess the data
X_train, X_test, y_train, y_test, _ = preprocess_data(data)

# Train the model
model = train_model(X_train, y_train, X_test, y_test)

# Save the trained model
model.save_model('trained_model.joblib')
