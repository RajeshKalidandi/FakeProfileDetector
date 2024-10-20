from typing import Dict, List, Any, Union
import joblib
import json
import numpy as np
import tensorflow as tf
import torch
import dgl
from .cnn_model import create_cnn_model
from .rnn_model import create_rnn_model
from .gnn_model import GNNModel
from .ann_model import create_ann_model

class FakeProfileDetector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FakeProfileDetector, cls).__new__(cls)
            cls._instance.load_models()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'models_loaded'):
            self.load_models()

    def load_models(self):
        self.best_model = joblib.load('best_model.joblib')
        self.voting_classifier = joblib.load('voting_classifier_model.joblib')
        self.stacking_classifier = joblib.load('stacking_classifier_model.joblib')
        self.adaboost_classifier = joblib.load('adaboost_classifier_model.joblib')
        self.feature_names_ = self.best_model.feature_names_
        self.models_loaded = True

    def predict(self, features):
        best_pred = self.best_model.predict(features)
        voting_pred = self.voting_classifier.predict(features)
        stacking_pred = self.stacking_classifier.predict(features)
        adaboost_pred = self.adaboost_classifier.predict(features)

        all_predictions = np.array([best_pred, voting_pred, stacking_pred, adaboost_pred])
        final_pred = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=all_predictions)

        return final_pred

    def predict_proba(self, features):
        best_proba = self.best_model.predict_proba(features)[:, 1]
        voting_proba = self.voting_classifier.predict_proba(features)[:, 1]
        stacking_proba = self.stacking_classifier.predict_proba(features)[:, 1]
        adaboost_proba = self.adaboost_classifier.predict_proba(features)[:, 1]

        final_proba = np.mean([best_proba, voting_proba, stacking_proba, adaboost_proba], axis=0)

        return final_proba

    @classmethod
    def load_model(cls):
        return cls()

    def retrain(self, X_train, y_train):
        # Implement the retraining logic here
        pass
