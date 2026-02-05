"""
Configuration management for the AI Voice Detection API
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    API_KEY = os.getenv("API_KEY", "hackathon_demo_key_2026")
    
    # Model Configuration
    BASE_DIR = Path(__file__).parent.parent
    MODEL_PATH = BASE_DIR / os.getenv("MODEL_PATH", "model/ai_voice_classifier.pkl")
    SCALER_PATH = BASE_DIR / os.getenv("SCALER_PATH", "model/feature_scaler.pkl")
    
    # Audio Processing
    MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "10"))
    MAX_AUDIO_SIZE_BYTES = MAX_AUDIO_SIZE_MB * 1024 * 1024
    SUPPORTED_LANGUAGES = os.getenv(
        "SUPPORTED_LANGUAGES", 
        "Tamil,English,Hindi,Malayalam,Telugu"
    ).split(",")
    
    # Audio Processing Parameters
    SAMPLE_RATE = 22050  # Standard sample rate for audio processing
    N_MFCC = 13  # Number of MFCC coefficients
    N_FFT = 2048  # FFT window size
    HOP_LENGTH = 512  # Hop length for STFT
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Thresholds
    CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for classification
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        assert cls.API_KEY, "API_KEY must be set"
        assert len(cls.SUPPORTED_LANGUAGES) > 0, "At least one language must be supported"
        return True


# Create config instance
config = Config()
