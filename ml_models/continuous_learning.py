from typing import Dict, List, Any, Union
import pandas as pd
from sklearn.model_selection import train_test_split
from .feature_extraction import extract_features
from .preprocessing import preprocess_data
from .model_comparison import train_and_evaluate_models, train_ensemble
from .model_evaluation import evaluate_model
import joblib
import schedule
import time
from datetime import datetime

class ContinuousLearning:
    def __init__(self, db: Any, analyses_collection: Any, feedback_collection: Any):
        self.db = db
        self.analyses_collection = analyses_collection
        self.feedback_collection = feedback_collection
        self.current_model = joblib.load('best_model.joblib')
        self.model_version = 1

    def collect_feedback(self, analysis_id: str, user_feedback: str) -> None:
        feedback = {
            'analysis_id': analysis_id,
            'user_feedback': user_feedback,
            'timestamp': datetime.utcnow()
        }
        self.feedback_collection.insert_one(feedback)

    def get_new_training_data(self) -> List[Tuple[Dict[str, Any], int]]:
        # Fetch recent analyses and their corresponding feedback
        analyses = list(self.analyses_collection.find().sort('created_at', -1).limit(1000))
        feedback = list(self.feedback_collection.find())

        feedback_dict = {f['analysis_id']: f['user_feedback'] for f in feedback}

        training_data = []
        for analysis in analyses:
            if analysis['_id'] in feedback_dict:
                features = analysis['features']
                label = 1 if feedback_dict[analysis['_id']] == 'fake' else 0
                training_data.append((features, label))

        return training_data

    def retrain_model(self) -> None:
        new_data = self.get_new_training_data()
        if not new_data:
            print("No new data available for retraining.")
            return

        features, labels = zip(*new_data)
        feature_df = pd.DataFrame(features)
        X, y = preprocess_data(feature_df, labels)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
        ensemble_result = train_ensemble(X_train, y_train, X_test, y_test, results)

        best_model_name = max(results, key=lambda x: results[x]['accuracy'])
        new_model = results[best_model_name]['model']

        # Compare new model with current model
        current_model_score = evaluate_model(self.current_model, X_test, y_test)
        new_model_score = evaluate_model(new_model, X_test, y_test)

        if new_model_score['accuracy'] > current_model_score['accuracy']:
            self.current_model = new_model
            self.model_version += 1
            joblib.dump(new_model, f'best_model_v{self.model_version}.joblib')
            print(f"Model updated to version {self.model_version}")
        else:
            print("Current model performs better. No update needed.")

    def schedule_retraining(self, interval_hours: int = 24) -> None:
        schedule.every(interval_hours).hours.do(self.retrain_model)

        while True:
            schedule.run_pending()
            time.sleep(1)

# Initialize the ContinuousLearning instance
# Note: You'll need to pass the correct db, analyses_collection, and feedback_collection
# continuous_learner = ContinuousLearning(db, analyses_collection, feedback_collection)
