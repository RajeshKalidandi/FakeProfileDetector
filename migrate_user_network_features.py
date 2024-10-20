from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['fake_profile_detector']
users_collection = db['users']

def migrate_user_features():
    # Update all user documents to include new network-related and temporal fields
    result = users_collection.update_many(
        {},
        {
            "$set": {
                "followers_count": 0,
                "following_count": 0,
                "connections": [],
                "follower_following_ratio": 0.0,
                "degree_centrality": 0.0,
                "betweenness_centrality": 0.0,
                "closeness_centrality": 0.0,
                "clustering_coefficient": 0.0,
                "network_score": 0.0,
                "created_at": datetime.utcnow(),
                "last_login": None,
                "post_count": 0,
                "activity_times": []
            }
        },
        upsert=False
    )

    print(f"Modified {result.modified_count} documents")

if __name__ == "__main__":
    migrate_user_features()
