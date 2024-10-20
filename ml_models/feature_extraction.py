import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .text_feature_extraction import extract_profile_features

def extract_features(profile_data):
    return extract_profile_features(profile_data)
