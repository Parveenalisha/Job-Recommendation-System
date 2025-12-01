"""
ML Model for Fake Job Detection
This module contains the ML model to predict if a job posting is real or fake.
"""
import re
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import os
from django.conf import settings


class FakeJobDetector:
    """ML Model to detect fake job postings"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_path = os.path.join(settings.BASE_DIR, 'jobs', 'ml_models', 'fake_job_detector.pkl')
        self.vectorizer_path = os.path.join(settings.BASE_DIR, 'jobs', 'ml_models', 'vectorizer.pkl')
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
            except:
                self._create_model()
        else:
            self._create_model()
    
    def _create_model(self):
        """Create and train a new model"""
        # Simple feature extraction
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Create a simple Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Train on synthetic data (in production, use real training data)
        # For now, we'll use a simple rule-based approach
        self._train_simple_model()
    
    def _train_simple_model(self):
        """Train model with simple rule-based features"""
        # Synthetic training data
        fake_jobs = [
            "Work from home! Make $5000/week! No experience needed!",
            "Easy money! Just send us your personal information!",
            "Get rich quick! No skills required!",
            "Urgent hiring! Send money for processing!",
        ]
        
        real_jobs = [
            "We are looking for an experienced Python developer with Django knowledge.",
            "Software Engineer position requiring 3+ years of experience in web development.",
            "Full-time position with competitive salary and benefits package.",
            "Join our team as a Senior Developer. Must have experience with React and Node.js.",
        ]
        
        # Combine and create labels
        texts = fake_jobs + real_jobs
        labels = [0] * len(fake_jobs) + [1] * len(real_jobs)
        
        # Vectorize
        X = self.vectorizer.fit_transform(texts)
        
        # Train
        self.model.fit(X, labels)
        
        # Save
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
    
    def extract_features(self, title, description, requirements, company_name):
        """Extract features from job posting"""
        # Combine all text
        text = f"{title} {description} {requirements} {company_name}".lower()
        
        # Rule-based features
        features = {
            'has_salary_info': bool(re.search(r'\$\d+|\d+\s*(k|thousand|million)', text)),
            'has_experience_requirement': bool(re.search(r'\d+\+?\s*(year|yr)', text)),
            'has_skills': bool(re.search(r'(skill|experience|knowledge|proficient)', text)),
            'suspicious_words': len(re.findall(r'(urgent|guaranteed|easy money|work from home|no experience)', text)),
            'has_contact_info': bool(re.search(r'(email|phone|contact|apply)', text)),
            'text_length': len(text),
            'has_company_info': len(company_name) > 3,
        }
        
        return features
    
    def predict(self, title, description, requirements, company_name):
        """Predict if job is real or fake"""
        # Combine text for vectorization
        combined_text = f"{title} {description} {requirements} {company_name}"
        
        # Vectorize
        try:
            X = self.vectorizer.transform([combined_text])
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            confidence = max(probability)
        except:
            # Fallback to rule-based prediction
            features = self.extract_features(title, description, requirements, company_name)
            # Simple scoring
            score = 0
            if features['has_salary_info']:
                score += 1
            if features['has_experience_requirement']:
                score += 1
            if features['has_skills']:
                score += 1
            if features['has_contact_info']:
                score += 1
            if features['has_company_info']:
                score += 1
            score -= features['suspicious_words'] * 2
            
            prediction = 1 if score >= 2 else 0
            confidence = abs(score) / 5.0
        
        return {
            'is_real': bool(prediction),
            'confidence': float(confidence),
            'is_fake': not bool(prediction)
        }


# Global instance
detector = FakeJobDetector()








