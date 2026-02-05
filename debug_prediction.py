"""
Debug script to trace specific audio prediction
"""
import sys
import numpy as np
import joblib
from pathlib import Path
from app.audio_processor import AudioProcessor
from app.feature_extractor import FeatureExtractor
from app.config import config

def debug_prediction(file_path):
    print(f"\n🔍 Debugging prediction for: {file_path}")
    
    # Load model and scaler
    model = joblib.load(config.MODEL_PATH)
    scaler = joblib.load(config.SCALER_PATH)
    print("✅ Model and scaler loaded")
    
    # Process audio
    processor = AudioProcessor()
    extractor = FeatureExtractor()
    
    with open(file_path, 'rb') as f:
        audio_bytes = f.read()
    
    audio_array, sr = processor.process_audio(audio_bytes)
    print(f"📊 Audio processed: Shape={audio_array.shape}, SR={sr}")
    
    # Extract features
    features = extractor.extract_features(audio_array)
    print("\n📈 Feature Values:")
    print("-" * 50)
    
    feature_names = [
        "MFCC (13)", "Pitch Mean", "Pitch Std", "Pitch Min", "Pitch Max", "Pitch Range",
        "RMS Mean", "RMS Std", "ZCR Mean", "ZCR Std",
        "Spectral Centroid Mean", "Spectral Centroid Std",
        "Spectral Rolloff Mean", "Spectral Rolloff Std",
        "Spectral Flatness Mean", "Spectral Flatness Std",
        "Spectral Bandwidth Mean", "Spectral Bandwidth Std",
        "Spectral Contrast Mean", "Spectral Contrast Std",
        "Onset Mean", "Onset Std", "Tempo", "Autocorr Mean", 
        "Autocorr Std", "Harmonic Ratio", "Percussive Ratio"
    ]
    
    # Map features to names (approximate mapping based on feature_extractor.py)
    # The first 13 are MFCC, then the rest follow the order in extract_features
    
    current_idx = 0
    # MFCC
    print(f"MFCCs (1-13): {features[0:13]}")
    current_idx = 13
    
    # Rest
    remaining_names = feature_names[1:]
    for i, val in enumerate(features[13:]):
        name = remaining_names[i] if i < len(remaining_names) else f"Feature {i+14}"
        print(f"{name:<25}: {val:.4f}")

    # Scale
    features_reshaped = features.reshape(1, -1)
    features_scaled = scaler.transform(features_reshaped)
    
    # Predict
    prob = model.predict_proba(features_scaled)[0]
    pred = model.predict(features_scaled)[0]
    
    class_map = {0: "HUMAN", 1: "AI_GENERATED"} # Note: Check mapping in train script!
    
    # WAIT! Check mapping in train_with_custom_data.py
    # Lines 100-106: AI=1, HUMAN=0
    # But let's verify what the model thinks.
    
    print("\n🧠 Model Prediction:")
    print("-" * 50)
    print(f"Raw Prediction: {pred}")
    print(f"Probabilities: Human={prob[0]:.4f}, AI={prob[1]:.4f}")
    print(f"Result: {class_map.get(pred, 'UNKNOWN')}")
    
    # Feature contribution (simple heuristic)
    # Compare with mean values if possible, or just look at scaled values
    print("\n⚖️ Scaled Feature Analysis (High absolute values drive decisions):")
    for i, val in enumerate(features_scaled[0]):
        if abs(val) > 2.0:  # Z-score > 2
            name = "MFCC" if i < 13 else remaining_names[i-13]
            print(f"Running high/low: {name} = {val:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_prediction.py <path_to_audio_file>")
        # Try to find a sample file to default to
        sample_dir = Path("d:/Guvi-Hackathon/custom_dataset/voice_detection_api/data/human")
        if sample_dir.exists():
            files = list(sample_dir.rglob("*.mpeg")) + list(sample_dir.rglob("*.mp3"))
            if files:
                print(f"Using default file: {files[0]}")
                debug_prediction(str(files[0]))
    else:
        debug_prediction(sys.argv[1])
