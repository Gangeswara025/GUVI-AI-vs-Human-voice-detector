
import os
import numpy as np
import librosa
import pandas as pd
from pathlib import Path
from tabulate import tabulate
import warnings

# Suppress librosa warnings
warnings.filterwarnings("ignore")

DATASET_PATH = Path("custom_dataset/voice_detection_api/data")

def get_audio_info(file_path):
    try:
        # Load with original sampling rate
        y, sr = librosa.load(file_path, sr=None)
        
        # Duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Silence (simple energy-based)
        # Split into short frames
        rms = librosa.feature.rms(y=y)[0]
        # Define silence threshold (e.g., -60dB relative to peak, or just absolute low energy)
        # Here we use a relative threshold of 1% of the max RMS
        silence_thresh = np.max(rms) * 0.01
        silence_frames = np.sum(rms < silence_thresh)
        total_frames = len(rms)
        silence_pct = (silence_frames / total_frames) * 100 if total_frames > 0 else 0
        
        return {
            "sr": sr,
            "duration": duration,
            "silence_pct": silence_pct
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def analyze_dataset():
    data = []
    
    for label_name in ["ai", "human"]:
        class_dir = DATASET_PATH / label_name
        if not class_dir.exists():
            continue
            
        for lang_dir in class_dir.iterdir():
            if not lang_dir.is_dir():
                continue
                
            language = lang_dir.name
            
            for audio_file in lang_dir.iterdir():
                if audio_file.suffix.lower() not in ['.mp3', '.wav', '.mpeg', '.m4a']:
                    continue
                    
                info = get_audio_info(audio_file)
                if info:
                    data.append({
                        "filename": audio_file.name,
                        "class": label_name,
                        "language": language,
                        "extension": audio_file.suffix.lower(),
                        "original_sr": info["sr"],
                        "duration": info["duration"],
                        "silence_pct": info["silence_pct"]
                    })
    
    df = pd.DataFrame(data)
    
    if df.empty:
        print("No audio files found.")
        return

    print("\n=== DATA DATASET ANALYSIS ===")
    
    print("\n1. File Extension Distribution:")
    print(tabulate(pd.crosstab(df["class"], df["extension"]), headers="keys", tablefmt="grid"))
    
    print("\n2. Language Distribution:")
    print(tabulate(pd.crosstab(df["class"], df["language"]), headers="keys", tablefmt="grid"))
    
    print("\n3. Original Sample Rates (Mean/Std):")
    sr_stats = df.groupby("class")["original_sr"].agg(['mean', 'std', 'min', 'max'])
    print(tabulate(sr_stats, headers="keys", tablefmt="grid"))
    
    print("\n4. Duration Statistics (Seconds):")
    dur_stats = df.groupby("class")["duration"].agg(['mean', 'std', 'min', 'max'])
    print(tabulate(dur_stats, headers="keys", tablefmt="grid"))

    print("\n5. Silence Percentage Statistics:")
    sil_stats = df.groupby("class")["silence_pct"].agg(['mean', 'std', 'min', 'max'])
    print(tabulate(sil_stats, headers="keys", tablefmt="grid"))
    
    # Check for bias
    print("\n=== POTENTIAL BIASES DETECTED ===")
    
    # Extension Bias
    ext_counts = pd.crosstab(df["class"], df["extension"])
    if len(ext_counts.columns) > 1: # If multiple extensions exist
        print("Warning: Check if one class uses a specific extension exclusively.")
        
    # SR Bias
    means = df.groupby("class")["original_sr"].mean()
    if abs(means.get("ai", 0) - means.get("human", 0)) > 4000:
        print(f"CRITICAL: Major sample rate difference! AI: {means.get('ai', 0):.0f} vs Human: {means.get('human', 0):.0f}")
        
    
if __name__ == "__main__":
    analyze_dataset()
