from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from .model import FakeProfileDetector

def train_model(X_train, y_train, X_test, y_test):
    detector = FakeProfileDetector()
    detector.train(X_train, y_train)

    # Evaluate the model
    y_pred = detector.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

    return detector
