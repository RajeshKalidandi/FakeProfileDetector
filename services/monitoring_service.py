from datetime import datetime, timedelta
from typing import List, Dict
from pymongo import MongoClient
import os
from services.alert_service import alert_service

class MonitoringService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['fake_profile_detector']
        self.analyses_collection = self.db['analyses']

    def get_system_performance(self, days: int = 7) -> Dict:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        pipeline = [
            {
                '$match': {
                    'created_at': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_analyses': {'$sum': 1},
                    'avg_confidence': {'$avg': '$confidence'},
                    'fake_profiles': {
                        '$sum': {
                            '$cond': [{'$eq': ['$result', 'fake']}, 1, 0]
                        }
                    }
                }
            }
        ]

        result = list(self.analyses_collection.aggregate(pipeline))

        if result:
            performance = result[0]
            performance['fake_profile_ratio'] = performance['fake_profiles'] / performance['total_analyses']
            del performance['_id']
        else:
            performance = {
                'total_analyses': 0,
                'avg_confidence': 0,
                'fake_profiles': 0,
                'fake_profile_ratio': 0
            }

        return performance

    def get_daily_analysis_count(self, days: int = 30) -> List[Dict]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        pipeline = [
            {
                '$match': {
                    'created_at': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$group': {
                    '_id': {
                        '$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]

        return list(self.analyses_collection.aggregate(pipeline))

    def check_for_anomalies(self):
        performance = self.get_system_performance(days=1)
        
        # Example anomaly detection rules
        if performance['total_analyses'] < 10:
            alert_service.send_alert(
                "Low Analysis Count",
                f"Only {performance['total_analyses']} analyses performed in the last 24 hours."
            )
        
        if performance['avg_confidence'] < 0.7:
            alert_service.send_alert(
                "Low Confidence Score",
                f"Average confidence score has dropped to {performance['avg_confidence']:.2f} in the last 24 hours."
            )
        
        if performance['fake_profile_ratio'] > 0.5:
            alert_service.send_alert(
                "High Fake Profile Ratio",
                f"Fake profile ratio has increased to {performance['fake_profile_ratio']:.2f} in the last 24 hours."
            )

monitoring_service = MonitoringService()
