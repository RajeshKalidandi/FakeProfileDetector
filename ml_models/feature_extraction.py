import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .text_feature_extraction import extract_profile_features
from .image_feature_extraction import analyze_multiple_images

def extract_features(profile_data):
    features = extract_profile_features(profile_data)
    
    # Extract image features if profile pictures are available
    if 'profile_pictures' in profile_data and profile_data['profile_pictures']:
        image_features = analyze_multiple_images(profile_data['profile_pictures'])
        features.update(image_features)
    
    return features
