from datetime import datetime

def extract_temporal_features(user):
    account_age = user.get_account_age()
    posting_frequency = user.get_posting_frequency()
    activity_pattern = user.get_activity_pattern()

    # Calculate the variance in activity pattern
    mean_activity = sum(activity_pattern) / 24
    variance = sum((x - mean_activity) ** 2 for x in activity_pattern) / 24

    # Calculate the ratio of night activity (10 PM to 6 AM) to day activity
    night_activity = sum(activity_pattern[22:] + activity_pattern[:6])
    day_activity = sum(activity_pattern[6:22])
    night_day_ratio = night_activity / day_activity if day_activity > 0 else 0

    return {
        'account_age': account_age,
        'posting_frequency': posting_frequency,
        'activity_variance': variance,
        'night_day_ratio': night_day_ratio,
    }
