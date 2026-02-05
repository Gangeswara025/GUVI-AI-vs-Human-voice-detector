"""
Machine Learning model for AI voice detection
"""
import os
import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from app.config import config
from app.utils import logger


class VoiceDetectionModel:
    """AI Voice Detection ML Model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_importance = None
        self.is_loaded = False
        
    def load_model(self):
        """Load the trained model and scaler from disk"""
        try:
            model_path = config.MODEL_PATH
            scaler_path = config.SCALER_PATH
            
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found at {model_path}. Creating dummy model.")
                self._create_dummy_model()
                return
            
            # Load model
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            
            # Load scaler if exists
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info(f"Scaler loaded from {scaler_path}")
            
            # Get feature importance
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = self.model.feature_importances_
            
            self.is_loaded = True
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            logger.warning("Creating dummy model for demo purposes")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for demo purposes"""
        # Create a simple Random Forest classifier
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Create dummy training data (39 features)
        # AI voices: more uniform features
        # Human voices: more varied features
        np.random.seed(42)
        
        # Generate synthetic training data
        n_samples = 200
        n_features = 39
        
        # AI voices (class 0): more consistent feature values
        ai_voices = np.random.normal(loc=0.5, scale=0.1, size=(n_samples, n_features))
        
        # Human voices (class 1): more varied feature values
        human_voices = np.random.normal(loc=0.5, scale=0.3, size=(n_samples, n_features))
        
        # Combine datasets
        X = np.vstack([ai_voices, human_voices])
        y = np.array([0] * n_samples + [1] * n_samples)
        
        # Shuffle
        indices = np.random.permutation(len(X))
        X = X[indices]
        y = y[indices]
        
        # Train model
        self.model.fit(X, y)
        
        # No scaler for dummy model
        self.scaler = None
        
        # Get feature importance
        self.feature_importance = self.model.feature_importances_
        
        self.is_loaded = True
        logger.info("Dummy model created and trained")
    
    def predict(self, features: np.ndarray) -> tuple:
        """
        Predict if voice is AI-generated or human
        
        Args:
            features: Feature vector (39 features)
            
        Returns:
            Tuple of (classification, confidence_score, probabilities)
            classification: "AI_GENERATED" or "HUMAN"
            confidence_score: float between 0.0 and 1.0
            probabilities: array of [ai_prob, human_prob]
        """
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Reshape features to 2D array
            features = features.reshape(1, -1)
            
            # Apply scaling if scaler exists
            if self.scaler is not None:
                features = self.scaler.transform(features)
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(features)[0]
            
            # probabilities[0] = Human probability (Class 0), probabilities[1] = AI probability (Class 1)
            human_prob = probabilities[0]
            ai_prob = probabilities[1]
            
            # Determine classification
            if ai_prob > human_prob:
                classification = "AI_GENERATED"
                confidence_score = ai_prob
            else:
                classification = "HUMAN"
                confidence_score = human_prob
            
            logger.info(f"Prediction: {classification} (confidence: {confidence_score:.3f})")
            
            return classification, confidence_score, probabilities
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise Exception(f"Model prediction error: {str(e)}")
    
    def get_top_features(self, features: np.ndarray, n_top: int = 5) -> list:
        """
        Get top contributing features for explainability
        
        Args:
            features: Feature vector
            n_top: Number of top features to return
            
        Returns:
            List of tuples (feature_index, feature_value, importance)
        """
        if self.feature_importance is None:
            return []
        
        # Get top feature indices by importance
        top_indices = np.argsort(self.feature_importance)[-n_top:][::-1]
        
        # Create list of (index, value, importance)
        top_features = [
            (int(idx), float(features[idx]), float(self.feature_importance[idx]))
            for idx in top_indices
        ]
        
        return top_features
    
    def save_model(self, model_path: Path = None, scaler_path: Path = None):
        """
        Save the trained model and scaler to disk
        
        Args:
            model_path: Path to save model
            scaler_path: Path to save scaler
        """
        if model_path is None:
            model_path = config.MODEL_PATH
        
        if scaler_path is None:
            scaler_path = config.SCALER_PATH
        
        # Create directory if it doesn't exist
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler if exists
        if self.scaler is not None:
            joblib.dump(self.scaler, scaler_path)
            logger.info(f"Scaler saved to {scaler_path}")


# Create global model instance
voice_model = VoiceDetectionModel()
