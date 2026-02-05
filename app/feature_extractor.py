"""
Audio feature extraction for AI voice detection
"""
import numpy as np
import librosa
from app.config import config
from app.utils import logger
import scipy.signal

# Monkeypatch for scipy >= 1.9.0 compatibility
if not hasattr(scipy.signal, 'hann'):
    logger.info("Monkeypatching scipy.signal.hann for compatibility")
    scipy.signal.hann = scipy.signal.windows.hann


class FeatureExtractor:
    """Extract audio features for ML model"""
    
    def __init__(self):
        self.sample_rate = config.SAMPLE_RATE
        self.n_mfcc = config.N_MFCC
        self.n_fft = config.N_FFT
        self.hop_length = config.HOP_LENGTH
    
    def extract_features(self, audio_array: np.ndarray) -> np.ndarray:
        """
        Extract comprehensive audio features
        
        Args:
            audio_array: Audio signal array
            
        Returns:
            Feature vector (39 features)
        """
        features = []
        
        try:
            # 1. MFCC features (13 coefficients)
            mfcc_features = self._extract_mfcc(audio_array)
            features.extend(mfcc_features)
            
            # 2. Pitch/F0 features (5 features)
            pitch_features = self._extract_pitch_features(audio_array)
            features.extend(pitch_features)
            
            # 3. Energy features (4 features)
            energy_features = self._extract_energy_features(audio_array)
            features.extend(energy_features)
            
            # 4. Spectral features (10 features)
            spectral_features = self._extract_spectral_features(audio_array)
            features.extend(spectral_features)
            
            # 5. Prosody features (7 features)
            prosody_features = self._extract_prosody_features(audio_array)
            features.extend(prosody_features)
            
            feature_vector = np.array(features)
            logger.info(f"Extracted {len(feature_vector)} features")
            
            return feature_vector
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise Exception(f"Feature extraction error: {str(e)}")
    
    def _extract_mfcc(self, audio_array: np.ndarray) -> list:
        """
        Extract MFCC (Mel-frequency cepstral coefficients)
        AI voices often have more uniform MFCC patterns
        
        Returns:
            13 MFCC features (mean values)
        """
        mfcc = librosa.feature.mfcc(
            y=audio_array,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        
        # Take mean across time for each coefficient
        mfcc_mean = np.mean(mfcc, axis=1)
        
        return mfcc_mean.tolist()
    
    def _extract_pitch_features(self, audio_array: np.ndarray) -> list:
        """
        Extract pitch-related features
        AI voices tend to have more consistent pitch
        
        Returns:
            5 pitch features: [mean, std, min, max, range]
        """
        # Extract pitch using librosa's pyin algorithm
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio_array,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=self.sample_rate
        )
        
        # Filter out NaN values (unvoiced segments)
        f0_valid = f0[~np.isnan(f0)]
        
        if len(f0_valid) > 0:
            pitch_mean = np.mean(f0_valid)
            pitch_std = np.std(f0_valid)
            pitch_min = np.min(f0_valid)
            pitch_max = np.max(f0_valid)
            pitch_range = pitch_max - pitch_min
        else:
            # If no valid pitch detected, use neutral values
            pitch_mean = pitch_std = pitch_min = pitch_max = pitch_range = 0.0
        
        return [pitch_mean, pitch_std, pitch_min, pitch_max, pitch_range]
    
    def _extract_energy_features(self, audio_array: np.ndarray) -> list:
        """
        Extract energy-related features
        AI voices may have different energy distributions
        
        Returns:
            4 energy features
        """
        # RMS Energy
        rms = librosa.feature.rms(y=audio_array, hop_length=self.hop_length)[0]
        rms_mean = np.mean(rms)
        rms_std = np.std(rms)
        
        # Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(audio_array, hop_length=self.hop_length)[0]
        zcr_mean = np.mean(zcr)
        zcr_std = np.std(zcr)
        
        return [rms_mean, rms_std, zcr_mean, zcr_std]
    
    def _extract_spectral_features(self, audio_array: np.ndarray) -> list:
        """
        Extract spectral features
        AI voices often lack subtle spectral variations
        
        Returns:
            10 spectral features
        """
        # Spectral Centroid
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        centroid_mean = np.mean(spectral_centroid)
        centroid_std = np.std(spectral_centroid)
        
        # Spectral Rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        rolloff_mean = np.mean(spectral_rolloff)
        rolloff_std = np.std(spectral_rolloff)
        
        # Spectral Flatness
        spectral_flatness = librosa.feature.spectral_flatness(
            y=audio_array,
            hop_length=self.hop_length
        )[0]
        flatness_mean = np.mean(spectral_flatness)
        flatness_std = np.std(spectral_flatness)
        
        # Spectral Bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        bandwidth_mean = np.mean(spectral_bandwidth)
        bandwidth_std = np.std(spectral_bandwidth)
        
        # Spectral Contrast
        spectral_contrast = librosa.feature.spectral_contrast(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        contrast_mean = np.mean(spectral_contrast)
        contrast_std = np.std(spectral_contrast)
        
        return [
            centroid_mean, centroid_std,
            rolloff_mean, rolloff_std,
            flatness_mean, flatness_std,
            bandwidth_mean, bandwidth_std,
            contrast_mean, contrast_std
        ]
    
    def _extract_prosody_features(self, audio_array: np.ndarray) -> list:
        """
        Extract prosody-related features
        AI voices may have unnatural prosodic patterns
        
        Returns:
            7 prosody features
        """
        # Compute onset strength (rhythmic features)
        onset_env = librosa.onset.onset_strength(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        onset_mean = np.mean(onset_env)
        onset_std = np.std(onset_env)
        
        # Tempo estimation
        tempo, _ = librosa.beat.beat_track(
            y=audio_array,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )
        
        # Compute autocorrelation for periodicity
        autocorr = librosa.autocorrelate(audio_array)
        autocorr_mean = np.mean(autocorr[:100])  # First 100 lags
        autocorr_std = np.std(autocorr[:100])
        
        # Harmonic-percussive separation
        harmonic, percussive = librosa.effects.hpss(audio_array)
        harmonic_ratio = np.mean(np.abs(harmonic)) / (np.mean(np.abs(audio_array)) + 1e-6)
        percussive_ratio = np.mean(np.abs(percussive)) / (np.mean(np.abs(audio_array)) + 1e-6)
        
        return [
            onset_mean, onset_std,
            tempo,
            autocorr_mean, autocorr_std,
            harmonic_ratio, percussive_ratio
        ]
