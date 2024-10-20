from backend.models import User

class FeatureToggle:
    def __init__(self):
        self.basic_features = {
            "profile_scanning": True,
            "result_export": True,
            "history_access": True,
            "basic_analytics": True
        }
        
        self.earned_features = {
            "advanced_analytics": {
                "required_points": 50,
                "duration": 48 * 3600  # 48 hours in seconds
            },
            "bulk_scanning": {
                "required_points": 30,
                "duration": 24 * 3600  # 24 hours in seconds
            },
            "api_access": {
                "required_points": 100,
                "duration": 72 * 3600  # 72 hours in seconds
            }
        }

    def get_user_features(self, user: User):
        features = self.basic_features.copy()
        for feature, config in self.earned_features.items():
            if user.contributions.total_points >= config["required_points"]:
                features[feature] = True
        return features

    def unlock_feature(self, user: User, feature: str):
        if feature not in self.earned_features:
            return False
        
        config = self.earned_features[feature]
        if user.contributions.total_points >= config["required_points"]:
            # Implement logic to grant temporary access to the feature
            # This might involve updating the user's rewards or a separate feature access tracking system
            return True
        return False

feature_toggle = FeatureToggle()
