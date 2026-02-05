"""
Simple training script for AI voice detection using custom dataset
Uses RandomForestClassifier with 80/20 train-test split
Dataset: 26 real audio samples (10 AI + 16 Human) across 5 languages
"""
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import sys

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent))

from app.config import config
from app.utils import logger
from app.feature_extractor import FeatureExtractor
from app.audio_processor import AudioProcessor
import librosa # Required for augmentation

class AudioAugmentor:
    """Helper class for audio data augmentation"""
    
    @staticmethod
    def add_noise(data, noise_factor=0.005):
        noise = np.random.randn(len(data))
        augmented_data = data + noise_factor * noise
        return augmented_data

    @staticmethod
    def change_pitch(data, sr, n_steps=2):
        return librosa.effects.pitch_shift(y=data, sr=sr, n_steps=n_steps)

    @staticmethod
    def change_speed(data, rate=1.0):
        return librosa.effects.time_stretch(y=data, rate=rate)


class CustomDatasetTrainer:
    """Train AI voice detector using real custom audio dataset"""
    
    def __init__(self, dataset_path: str):
        """
        Initialize trainer
        
        Args:
            dataset_path: Path to dataset root (contains 'ai' and 'human' folders)
        """
        self.dataset_path = Path(dataset_path)
        self.audio_processor = AudioProcessor()
        self.feature_extractor = FeatureExtractor()
        
        # Supported audio formats
        self.audio_extensions = ['.mp3', '.wav', '.mpeg', '.m4a']
        
    def get_file_list(self) -> tuple:
        """
        Scan directory for all audio files and return them with labels
        
        Returns:
            Tuple of (file_paths, labels)
        """
        file_paths = []
        labels = []
        
        # Load AI-generated voices (label = 1)
        ai_path = self.dataset_path / 'ai'
        if ai_path.exists():
            for ext in self.audio_extensions:
                for f in ai_path.rglob(f'*{ext}'):
                    file_paths.append(f)
                    labels.append(1)
        
        # Load human voices (label = 0)
        human_path = self.dataset_path / 'human'
        if human_path.exists():
            for ext in self.audio_extensions:
                for f in human_path.rglob(f'*{ext}'):
                    file_paths.append(f)
                    labels.append(0)
                    
        return np.array(file_paths), np.array(labels)

    def process_file(self, file_path, label, perform_augmentation=False) -> tuple:
        """
        Process a single file: load, extract features, and optionally augment
        
        Returns:
            Tuple of (features_list, labels_list)
        """
        features_list = []
        labels_list = []
        
        try:
            # Read audio file
            with open(file_path, 'rb') as f:
                audio_bytes = f.read()
            
            # Convert to WAV and extract features (handles .mpeg, .mp3, .wav)
            # This handles Strict Resampling via AudioProcessor
            audio_array, sr = self.audio_processor.process_audio(audio_bytes)
            
            # Extract features from ORIGINAL
            orig_features = self.feature_extractor.extract_features(audio_array)
            if len(orig_features) == 39:
                features_list.append(orig_features)
                labels_list.append(label)
            
            if perform_augmentation:
                # 1. Add heavy noise (Anti-Silence Cheat)
                noise_audio = AudioAugmentor.add_noise(audio_array, noise_factor=0.02)
                features_list.append(self.feature_extractor.extract_features(noise_audio))
                labels_list.append(label)
                
                # 2. Pitch Shift Up (Anti-Memorization)
                pitch_up = AudioAugmentor.change_pitch(audio_array, sr, n_steps=2)
                features_list.append(self.feature_extractor.extract_features(pitch_up))
                labels_list.append(label)
                
                # 3. Pitch Shift Down
                pitch_down = AudioAugmentor.change_pitch(audio_array, sr, n_steps=-2)
                features_list.append(self.feature_extractor.extract_features(pitch_down))
                labels_list.append(label)
                
                # 4. Speed Up (New Augmentation)
                speed_up = AudioAugmentor.change_speed(audio_array, rate=1.1)
                features_list.append(self.feature_extractor.extract_features(speed_up))
                labels_list.append(label)
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to process {file_path.name}: {e}")
            
        return features_list, labels_list

    def prepare_data(self):
        """
        Prepare Train/Test splits ensuring NO leakage.
        Augmentation is applied ONLY to Training data.
        """
        # 1. Get all files
        files, labels = self.get_file_list()
        
        if len(files) == 0:
            raise ValueError("No audio files found!")
            
        logger.info(f"files found: {len(files)}")
            
        # 2. Split FILES first (Strict separation)
        train_files, test_files, train_labels, test_labels = train_test_split(
            files, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        logger.info(f"Split: {len(train_files)} Training Files, {len(test_files)} Test Files")
        
        # 3. Process Training Data (With Augmentation)
        X_train = []
        y_train = []
        logger.info("Processing Training Data (With Augmentation)...")
        for f, l in zip(train_files, train_labels):
            feats, labs = self.process_file(f, l, perform_augmentation=True)
            X_train.extend(feats)
            y_train.extend(labs)
            
        # 4. Process Test Data (NO Augmentation - Real world scenario)
        X_test = []
        y_test = []
        logger.info("Processing Test Data (Originals only)...")
        for f, l in zip(test_files, test_labels):
            feats, labs = self.process_file(f, l, perform_augmentation=False)
            X_test.extend(feats)
            y_test.extend(labs)
            
        return np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)
    
    def train_model(self, X_train, X_test, y_train, y_test):
        """
        Train RandomForestClassifier with prepared splits
        """
        logger.info("\n🔧 Training RandomForestClassifier...")
        logger.info(f"   Final Train Samples: {len(X_train)}")
        logger.info(f"   Final Test Samples: {len(X_test)}")
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train RandomForestClassifier
        model = RandomForestClassifier(
            n_estimators=100,           # Standard
            max_depth=7,               # Slightly constrained
            min_samples_split=4,       
            min_samples_leaf=2,        
            max_features='sqrt',       
            random_state=42,           
            n_jobs=-1,                 
            class_weight='balanced'    
        )
        
        logger.info("   Fitting model...")
        model.fit(X_train_scaled, y_train)
        
        # Evaluate on test set
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"\n✅ Training Complete!")
        logger.info(f"   Test Accuracy: {accuracy:.2%}")
        
        # Classification Report
        logger.info(f"\n📊 Classification Report:")
        logger.info("\n" + classification_report(
            y_test, y_pred, 
            target_names=['HUMAN', 'AI_GENERATED'],
            zero_division=0
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"\n📈 Confusion Matrix:")
        logger.info(f"   {cm}")
        
        return model, scaler
    
    def save_model(self, model, scaler):
        model_path = config.MODEL_PATH
        scaler_path = config.SCALER_PATH
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        logger.info(f"\n💾 Saved to: {model_path}")


def main():
    logger.info("🚀 Starting Hardened Training Pipeline\n")
    
    dataset_path = "custom_dataset/voice_detection_api/data"
    trainer = CustomDatasetTrainer(dataset_path)
    
    try:
        # Prepare Data
        X_train, X_test, y_train, y_test = trainer.prepare_data()
        
        # Train
        model, scaler = trainer.train_model(X_train, X_test, y_train, y_test)
        
        # Save
        trainer.save_model(model, scaler)
        
        logger.info("\n✅ Hardened Model Training Complete!")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
