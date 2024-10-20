import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_data(data):
    # Convert data to DataFrame if it's not already
    df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data

    # Handle missing values
    df = df.fillna(0)

    # Convert categorical variables to numerical
    df = pd.get_dummies(df, columns=['account_type'])

    # Split features and target
    X = df.drop('is_fake', axis=1)
    y = df['is_fake']

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
