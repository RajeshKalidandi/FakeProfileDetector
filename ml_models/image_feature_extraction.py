import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import face_recognition
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from scipy.fftpack import dct
import os

# Initialize ResNet50 model
resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Custom CNN for profile picture classification
def create_custom_cnn():
    model = Sequential([
        ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3)),
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

custom_cnn = create_custom_cnn()
# TODO: Train this model with your dataset of real and fake profile pictures

def detect_faces(img_path):
    image = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return len(face_locations), face_encodings

def extract_image_metadata(img_path):
    image = Image.open(img_path)
    exif_data = {}
    info = image._getexif()
    if info:
        for tag_id, value in info.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_data[tag] = value
    return exif_data

def extract_deep_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = resnet_model.predict(x)
    return features.flatten()

def detect_image_manipulation(img_path):
    img = cv2.imread(img_path, 0)
    dct_result = dct(dct(img.T, norm='ortho').T, norm='ortho')
    return np.sum(np.abs(dct_result))

def classify_profile_picture(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    prediction = custom_cnn.predict(x)
    return prediction[0][0]

def extract_image_features(img_paths):
    features = {}
    
    for i, img_path in enumerate(img_paths):
        # Face detection and recognition
        face_count, face_encodings = detect_faces(img_path)
        features[f'face_count_{i}'] = face_count
        features[f'face_encoding_{i}'] = face_encodings[0].tolist() if face_encodings else []
        
        # Image metadata
        metadata = extract_image_metadata(img_path)
        features[f'has_exif_{i}'] = len(metadata) > 0
        features[f'camera_make_{i}'] = metadata.get('Make', 'Unknown')
        features[f'camera_model_{i}'] = metadata.get('Model', 'Unknown')
        features[f'date_taken_{i}'] = metadata.get('DateTimeOriginal', 'Unknown')
        
        # Deep learning features
        deep_features = extract_deep_features(img_path)
        for j, value in enumerate(deep_features):
            features[f'deep_feature_{i}_{j}'] = value
        
        # Image manipulation detection
        features[f'manipulation_score_{i}'] = detect_image_manipulation(img_path)
        
        # Profile picture classification
        features[f'profile_pic_score_{i}'] = classify_profile_picture(img_path)
    
    return features

def analyze_multiple_images(image_paths):
    all_features = extract_image_features(image_paths)
    
    # Aggregate features from multiple images
    aggregated_features = {
        'total_images': len(image_paths),
        'avg_face_count': np.mean([all_features[f'face_count_{i}'] for i in range(len(image_paths))]),
        'avg_manipulation_score': np.mean([all_features[f'manipulation_score_{i}'] for i in range(len(image_paths))]),
        'avg_profile_pic_score': np.mean([all_features[f'profile_pic_score_{i}'] for i in range(len(image_paths))]),
    }
    
    return {**all_features, **aggregated_features}
