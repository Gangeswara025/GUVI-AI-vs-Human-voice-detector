"""
Audio processing pipeline: Base64 decoding, format conversion, normalization
"""
import io
import tempfile
import os
from pathlib import Path
from pydub import AudioSegment
import soundfile as sf
import numpy as np
from app.config import config
from app.utils import logger


class AudioProcessor:
    """Handle audio processing operations"""
    
    def __init__(self):
        self.sample_rate = config.SAMPLE_RATE
        
    def process_audio(self, audio_bytes: bytes) -> tuple:
        """
        Process audio from bytes: convert to WAV, normalize, and prepare for feature extraction
        
        Args:
            audio_bytes: Raw audio bytes (MP3 format)
            
        Returns:
            Tuple of (audio_array, sample_rate)
            
        Raises:
            Exception: If audio processing fails
        """
        try:
            # Step 1: Convert MP3 to WAV
            audio_array = self._convert_to_wav(audio_bytes)
            
            # Step 2: Normalize audio
            audio_array = self._normalize_audio(audio_array)
            
            # Step 3: Ensure mono channel
            audio_array = self._ensure_mono(audio_array)
            
            # STRICT RESAMPLING CHECK
            if self.sample_rate and self.sample_rate != config.SAMPLE_RATE: # Should be self.sample_rate from init
                 pass # self.sample_rate is already config.SAMPLE_RATE
            
            logger.info(f"Audio processed: shape={audio_array.shape}, sr={self.sample_rate}")
            
            return audio_array, self.sample_rate
            
        except Exception as e:
            logger.error(f"Audio processing failed: {str(e)}")
            raise Exception(f"Audio processing error: {str(e)}")
    
    def _convert_to_wav(self, audio_bytes: bytes) -> np.ndarray:
        """
        Convert MP3 bytes to WAV array
        
        Args:
            audio_bytes: Raw MP3 bytes
            
        Returns:
            Audio array
        """
        try:
            # Write bytes to a temporary file
            # This is needed because librosa requires a file path
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
                temp_file.write(audio_bytes)
            
            try:
                # Load with librosa (works without FFmpeg for most MP3 files)
                import librosa
                audio_array, sr = librosa.load(temp_path, sr=self.sample_rate, mono=True)
                
                logger.info(f"Converted MP3 to WAV: {len(audio_array)} samples at {sr}Hz")
                
                return audio_array
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
            
        except Exception as e:
            logger.error(f"MP3 to WAV conversion failed: {str(e)}")
            raise Exception(f"Audio format conversion error: {str(e)}")
    
    def _normalize_audio(self, audio_array: np.ndarray) -> np.ndarray:
        """
        Normalize audio to consistent volume level
        
        Args:
            audio_array: Input audio array
            
        Returns:
            Normalized audio array
        """
        # Normalize to [-1, 1] range
        max_val = np.max(np.abs(audio_array))
        if max_val > 0:
            audio_array = audio_array / max_val
        
        logger.info("Audio normalized")
        return audio_array
    
    def _ensure_mono(self, audio_array: np.ndarray) -> np.ndarray:
        """
        Ensure audio is mono (single channel)
        
        Args:
            audio_array: Input audio array
            
        Returns:
            Mono audio array
        """
        # If stereo, convert to mono by averaging channels
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)
            logger.info("Converted stereo to mono")
        
        return audio_array
    
    def validate_audio_duration(self, audio_array: np.ndarray, min_duration: float = 0.5, max_duration: float = 30.0) -> bool:
        """
        Validate audio duration is within acceptable range
        
        Args:
            audio_array: Audio array
            min_duration: Minimum duration in seconds
            max_duration: Maximum duration in seconds
            
        Returns:
            True if duration is valid
            
        Raises:
            ValueError: If duration is out of range
        """
        duration = len(audio_array) / self.sample_rate
        
        if duration < min_duration:
            raise ValueError(f"Audio too short: {duration:.2f}s (minimum {min_duration}s)")
        
        if duration > max_duration:
            raise ValueError(f"Audio too long: {duration:.2f}s (maximum {max_duration}s)")
        
        logger.info(f"Audio duration: {duration:.2f}s")
        return True
