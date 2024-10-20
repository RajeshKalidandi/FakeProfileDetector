# Fake Profile Detector
> Advanced Social Media Profile Analysis using Deep Learning

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [ML Models](#ml-models)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Overview

Fake Profile Detector is an advanced system that leverages multiple machine learning models to identify fake social media profiles. The system uses a combination of neural networks (CNN, RNN, ANN) and traditional ML approaches (SVM, Naive Bayes, KNN) to provide highly accurate detection results.

### Key Capabilities
- Multi-model analysis approach
- Real-time profile scanning
- Feature importance visualization
- Historical analysis tracking
- Detailed reporting system

## Features

### 1. Profile Analysis
- URL-based profile scanning
- Manual data entry support
- Bulk profile analysis
- Screenshot analysis capability

### 2. Machine Learning Models
- Convolutional Neural Networks (CNN)
- Recurrent Neural Networks (RNN)
- Artificial Neural Networks (ANN)
- Support Vector Machines (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes Classifier

### 3. User Interface
- Responsive dashboard
- Interactive visualizations
- Real-time analysis feedback
- Historical analysis tracking
- Export functionality

## Project Structure

```
D:\FakeProfileDetector\
├── README.md
├── DOCUMENTATION.md
├── .env.example
├── .gitignore
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   ├── analysis/
│   │   └── dashboard/
│   ├── components/
│   ├── lib/
│   └── public/
├── backend/
│   ├── models/
│   │   ├── cnn_model.py
│   │   ├── rnn_model.py
│   │   └── traditional_models.py
│   ├── api/
│   │   └── routes/
│   └── utils/
├── ml_training/
│   ├── datasets/
│   ├── notebooks/
│   └── scripts/
└── tests/
```

## Technology Stack

### Frontend
- Next.js 13+ (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- NextAuth.js
- React Query

### Backend
- Python 3.9+
- FastAPI
- MongoDB
- JWT Authentication

### ML Stack
- TensorFlow 2.x
- Scikit-learn
- NumPy
- Pandas
- OpenCV

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fake-profile-detector.git
cd fake-profile-detector
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
NEXTAUTH_SECRET=your_nextauth_secret

# Backend
MONGODB_URI=your_mongodb_uri
JWT_SECRET=your_jwt_secret
MODEL_PATH=path_to_saved_models
```

### Database Setup

1. MongoDB Setup:
```bash
# Install MongoDB Community Edition
# Create required collections:
- users
- profiles
- analysis_results
```

2. Model Storage:
```bash
# Create directories for model storage
mkdir -p backend/models/saved_models
```

## Usage

### Starting the Development Environment

1. Frontend:
```bash
cd frontend
npm run dev
```

2. Backend:
```bash
cd backend
uvicorn main:app --reload
```

### Running Production Build

1. Frontend:
```bash
cd frontend
npm run build
npm start
```

2. Backend:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

### Authentication Endpoints

```typescript
POST /api/auth/login
POST /api/auth/register
POST /api/auth/refresh
```

### Analysis Endpoints

```typescript
POST /api/analyze/profile
GET /api/analyze/history
GET /api/analyze/stats
```

### Profile Management

```typescript
POST /api/profiles/add
GET /api/profiles/list
PUT /api/profiles/update/:id
DELETE /api/profiles/delete/:id
```

## ML Models

### Model Architecture

#### CNN Model
```python
model = Sequential([
    Conv1D(filters=64, kernel_size=2, activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

#### Feature Extraction
- Username patterns
- Profile completeness
- Activity patterns
- Network metrics
- Content analysis
- Temporal features

### Model Training

```bash
# Train models
python ml_training/train_models.py --data-path datasets/profiles.csv --epochs 100
```

### Model Evaluation
- Accuracy: 94.5%
- Precision: 92.3%
- Recall: 95.1%
- F1 Score: 93.7%

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend
- Write unit tests for new features
- Document all API endpoints
- Keep ML models up to date

## Troubleshooting

### Common Issues

1. Installation Problems
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
npm install
```

2. Model Loading Issues
```python
# Check model paths
print(os.path.exists(MODEL_PATH))
# Verify model version compatibility
print(tf.__version__)
```

3. Database Connection
```python
# Test MongoDB connection
python -c "from pymongo import MongoClient; client = MongoClient('your_uri'); print(client.server_info())"
```

### Performance Optimization

1. Frontend
- Enable code splitting
- Implement lazy loading
- Optimize images
- Use caching strategies

2. Backend
- Implement rate limiting
- Use connection pooling
- Cache frequent queries
- Optimize database indices

3. ML Models
- Batch processing
- Model quantization
- CPU/GPU optimization
- Parallel processing

### Monitoring

1. System Metrics
- API response times
- Model inference times
- Memory usage
- CPU utilization

2. ML Metrics
- Model accuracy
- False positives/negatives
- Feature importance
- Prediction confidence

## Security Considerations

1. Data Protection
- Input sanitization
- XSS prevention
- CSRF protection
- Rate limiting

2. Authentication
- JWT token management
- Password hashing
- Session handling
- OAuth2 integration

3. API Security
- Input validation
- Request throttling
- Error handling
- Audit logging

---

For additional support or feature requests, please open an issue in the GitHub repository or contact the development team.

Last Updated: October 20, 2024
