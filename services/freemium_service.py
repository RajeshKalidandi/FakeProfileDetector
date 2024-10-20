from backend.models.user import User
from datetime import datetime, timedelta

DAILY_SCAN_LIMIT = 10

class FreemiumService:
    def __init__(self):
        self.community_system = {
            "activities": {
                "profile_verification": {
                    "points": 10,
                    "daily_limit": 20,
                    "accuracy_threshold": 0.85
                },
                "fake_reporting": {
                    "points": 5,
                    "daily_limit": 10,
                    "validation_required": True
                },
                "feedback_submission": {
                    "points": 2,
                    "daily_limit": 30,
                    "minimum_length": 50
                }
            },
            "leaderboard": {
                "update_frequency": timedelta(hours=1),
                "display_metrics": [
                    "total_points",
                    "verified_profiles",
                    "valid_reports"
                ],
                "rewards": {
                    "top_10_weekly": "UNLIMITED_SCANNING",
                    "top_50_monthly": "ADVANCED_ML"
                }
            }
        }

    def record_activity(self, user: User, activity_type: str):
        activity_config = self.community_system["activities"].get(activity_type)
        if not activity_config:
            raise ValueError("Invalid activity type")

        # Check daily limit
        if user.daily_activity_count.get(activity_type, 0) >= activity_config["daily_limit"]:
            return False

        # Record the activity and award points
        user.contributions["total_points"] += activity_config["points"]
        user.daily_activity_count[activity_type] = user.daily_activity_count.get(activity_type, 0) + 1

        # Update specific contribution counters
        if activity_type == "profile_verification":
            user.contributions["verified_profiles"] += 1
        elif activity_type == "fake_reporting":
            user.contributions["valid_reports"] += 1
        elif activity_type == "feedback_submission":
            user.contributions["feedback_count"] += 1

        # Save user changes
        user.save()
        return True

    def update_leaderboard(self):
        # Implement leaderboard update logic
        pass

    def get_total_scans(self) -> int:
        # Implement logic to count total scans across all users
        return User.get_total_scans()

    def get_total_contributions(self) -> int:
        # Implement logic to count total contributions across all users
        return User.get_total_contributions()

    def track_analytics(self, metric_type: str, data: dict):
        # Implement analytics tracking logic
        pass

    def check_scan_limit(self, user: User) -> bool:
        if user.tier == 'pro':
            return True
        user.update_daily_scans()
        return user.daily_scans <= DAILY_SCAN_LIMIT

    def add_contribution(self, user: User, contribution_type: str) -> bool:
        user.add_contribution(contribution_type)
        self.check_rewards(user)
        return True

    def check_rewards(self, user: User):
        if user.contributions['verifiedProfiles'] >= 50:
            self.grant_reward(user, 'UNLIMITED_SCANNING', timedelta(days=7))
        if user.contributions['validReports'] >= 10:
            self.grant_reward(user, 'ADVANCED_ML', timedelta(days=3))
        if user.contributions['feedbackCount'] >= 30:
            self.grant_reward(user, 'BULK_UPGRADE', timedelta(days=2))

    def grant_reward(self, user: User, reward_type: str, duration: timedelta):
        expiry = datetime.utcnow() + duration
        user.rewards.append({
            'type': reward_type,
            'granted_at': datetime.utcnow(),
            'expires_at': expiry,
            'status': 'active'
        })
        user.save()

    def get_total_scans(self):
        return sum(user['daily_scans'] for user in User.users_collection.find())

    def get_total_contributions(self):
        return sum(user['contributions']['total_points'] for user in User.users_collection.find())

freemium_service = FreemiumService()

# ... (other existing freemium service functions)
