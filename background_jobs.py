from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from data_collection.collector import DataCollector
from ml_models.feature_extraction import extract_features
from ml_models.model import FakeProfileDetector
from ml_models.model_evaluation import evaluate_model
from services.logging_service import logging_service
from services.monitoring_service import monitoring_service
from datetime import datetime
import pandas as pd

data_collector = DataCollector()
fake_profile_detector = FakeProfileDetector()

def collect_data_and_extract_features():
    logging_service.log_info("Starting data collection and feature extraction")
    try:
        # Collect new data
        new_profiles = data_collector.collect_new_profiles()
        
        # Extract features
        for profile in new_profiles:
            features = extract_features(profile)
            # Store features in the database
            store_features_in_db(profile['id'], features)
        
        logging_service.log_info(f"Collected and processed {len(new_profiles)} new profiles")
    except Exception as e:
        logging_service.log_error(f"Error in data collection and feature extraction: {str(e)}")

def retrain_and_evaluate_model():
    logging_service.log_info("Starting model retraining and evaluation")
    try:
        # Load the latest data
        data = load_latest_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(data['features'], data['labels'], test_size=0.2, random_state=42)
        
        # Retrain the model
        fake_profile_detector.retrain(X_train, y_train)
        
        # Evaluate the model
        evaluation_results = evaluate_model(fake_profile_detector, X_test, y_test)
        
        # Log the evaluation results
        logging_service.log_info(f"Model evaluation results: {evaluation_results}")
        
        # Update the monitoring service with the new model performance
        monitoring_service.update_model_performance(evaluation_results)
    except Exception as e:
        logging_service.log_error(f"Error in model retraining and evaluation: {str(e)}")

def store_features_in_db(profile_id, features):
    # Implement this function to store features in your database
    pass

def load_latest_data():
    # Implement this function to load the latest data from your database
    pass

def start_background_jobs():
    scheduler = BackgroundScheduler()
    
    # Schedule data collection and feature extraction job to run every 6 hours
    scheduler.add_job(
        collect_data_and_extract_features,
        CronTrigger(hour='*/6')
    )
    
    # Schedule model retraining and evaluation job to run daily at 2 AM
    scheduler.add_job(
        retrain_and_evaluate_model,
        CronTrigger(hour=2, minute=0)
    )
    
    scheduler.start()
    logging_service.log_info("Background jobs scheduled and started")

if __name__ == "__main__":
    start_background_jobs()
