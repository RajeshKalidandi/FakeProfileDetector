import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class LoggingService:
    def __init__(self):
        self.logger = logging.getLogger('FakeProfileDetector')
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create a rotating file handler
        file_handler = RotatingFileHandler(
            'logs/app.log', maxBytes=10485760, backupCount=5)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_prediction(self, user_id, profile_url, prediction, confidence):
        self.logger.info(f"Prediction: user_id={user_id}, profile_url={profile_url}, prediction={prediction}, confidence={confidence}")

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

logging_service = LoggingService()
