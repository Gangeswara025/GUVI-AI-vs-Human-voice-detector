"""
Analyze dataset for leakage and shortcut features
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from app.audio_processor import AudioProcessor
from app.feature_extractor import FeatureExtractor
import warnings
warnings.filterwarnings('ignore')

def analyze_dataset():
    print("📊 Loading dataset for analysis...")
    
    # Setup paths from your project structure
    base_path = Path("custom_dataset/voice_detection_api/data")
    ai_path = base_path / "ai"
    human_path = base_path / "human"
    
    processor = AudioProcessor()
    extractor = FeatureExtractor()
    
    data = []
    
    # Helper to process files
    def process_files(path, label_name):
        files = list(path.rglob("*.mp3")) + list(path.rglob("*.mpeg")) + list(path.rglob("*.wav"))
        print(f"Found {len(files)} {label_name} files")
        
        for f in files:
            try:
                with open(f, 'rb') as file:
                    content = file.read()
                
                # Get raw audio info BEFORE processing to check for file-level shortcuts
                file_size = len(content)
                
                # Process
                audio, sr = processor.process_audio(content)
                duration = len(audio) / sr
                
                # Features
                feats = extractor.extract_features(audio)
                
                row = {
                    "filename": f.name,
                    "label": label_name,
                    "file_size": file_size,
                    "duration": duration,
                    "sr": sr,
                    # Add standard features
                    "mfcc_mean": np.mean(feats[0:13]), # Average of MFCCs
                    "pitch_mean": feats[13],
                    "spectral_centroid": feats[23], # Approx index
                    "spectral_rolloff": feats[25],
                    "spectral_bandwidth": feats[29]
                }
                data.append(row)
            except Exception as e:
                print(f"Error {f.name}: {e}")

    process_files(ai_path, "AI")
    process_files(human_path, "HUMAN")
    
    # Analyze data
    print("\n🔍 Shortcut Analysis:")
    print("-" * 50)
    
    durations = {"AI": [], "HUMAN": []}
    sizes = {"AI": [], "HUMAN": []}
    input_data = {} # store all cols for ROC calc
    
    for row in data:
        label = row['label']
        durations[label].append(row['duration'])
        sizes[label].append(row['file_size'])
        
        for k, v in row.items():
            if k not in ['filename', 'label']:
                if k not in input_data: input_data[k] = []
                input_data[k].append(v)
            
    # 1. Duration / Size Shortcut
    for label in ["AI", "HUMAN"]:
        d = np.array(durations[label])
        s = np.array(sizes[label])
        print(f"[{label}] Duration: {np.mean(d):.2f}s (+/- {np.std(d):.2f})")
        print(f"[{label}] File Size: {np.mean(s)/1024:.2f}KB (+/- {np.std(s)/1024:.2f})")
    
    # 2. Perfect Separators?
    print("\n🔍 Single Feature Separators (ROC AUC = 1.0?):")
    from sklearn.metrics import roc_auc_score
    
    numeric_cols = ["duration", "file_size", "mfcc_mean", "pitch_mean", 
                   "spectral_centroid", "spectral_rolloff", "spectral_bandwidth"]
    
    # Create y_true
    y_true = [1 if row['label'] == 'AI' else 0 for row in data]
    
    for col in numeric_cols:
        try:
            # Extract column data
            col_data = [row[col] for row in data]
            
            score = roc_auc_score(y_true, col_data)
            # If score is < 0.5, flip it (perfect separation can be high or low)
            max_score = max(score, 1-score)
            
            print(f"{col:<20}: AUC = {max_score:.4f}")
            if max_score > 0.95:
                print(f"   ⚠️ WARNING: {col} is a potential shortcut feature!")
        except Exception as e:
            print(f"Could not calc AUC for {col}: {e}")

    print("-" * 50)
    print(f"Total Samples: {len(data)}")

if __name__ == "__main__":
    analyze_dataset()
