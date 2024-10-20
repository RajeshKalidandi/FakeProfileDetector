import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .text_feature_extraction import extract_profile_features
from .image_feature_extraction import analyze_multiple_images
from .network_feature_extraction import extract_network_features
from .temporal_feature_extraction import extract_temporal_features

def extract_features(user_data):
    features = {}
    
    # Extract profile features
    profile_features = extract_profile_features(user_data)
    features.update(profile_features)
    
    # Extract image features if profile pictures are available
    if 'profile_pictures' in user_data and user_data['profile_pictures']:
        image_features = analyze_multiple_images(user_data['profile_pictures'])
        features.update(image_features)
    
    # Add network features
    network_features = extract_network_features(
        user_data['id'],
        user_data['followers_count'],
        user_data['following_count'],
        user_data['connections']
    )
    features.update(network_features)
    
    # Add temporal features
    temporal_features = extract_temporal_features(user_data['user'])
    features.update(temporal_features)
    
    return features
