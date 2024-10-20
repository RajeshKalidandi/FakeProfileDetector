from sklearn.ensemble import RandomForestClassifier
import joblib

class FakeProfileDetector:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.feature_names_ = None

    def train(self, X, y):
        self.model.fit(X, y)
        self.feature_names_ = X.columns.tolist() if hasattr(X, 'columns') else None

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def save_model(self, filename):
        joblib.dump({'model': self.model, 'feature_names': self.feature_names_}, filename)

    @classmethod
    def load_model(cls, filename):
        data = joblib.load(filename)
        detector = cls()
        detector.model = data['model']
        detector.feature_names_ = data['feature_names']
        return detector
