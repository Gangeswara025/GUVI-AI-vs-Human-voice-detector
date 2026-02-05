"""
Explainability engine for voice detection results
"""
import numpy as np
from app.utils import logger


class VoiceExplainer:
    """Generate human-readable explanations for voice detection results"""
    
    # Feature name mapping (39 features)
    FEATURE_NAMES = [
        # MFCC (0-12)
        "MFCC-1", "MFCC-2", "MFCC-3", "MFCC-4", "MFCC-5", "MFCC-6", "MFCC-7",
        "MFCC-8", "MFCC-9", "MFCC-10", "MFCC-11", "MFCC-12", "MFCC-13",
        # Pitch (13-17)
        "Pitch Mean", "Pitch Std", "Pitch Min", "Pitch Max", "Pitch Range",
        # Energy (18-21)
        "RMS Mean", "RMS Std", "ZCR Mean", "ZCR Std",
        # Spectral (22-31)
        "Spectral Centroid Mean", "Spectral Centroid Std",
        "Spectral Rolloff Mean", "Spectral Rolloff Std",
        "Spectral Flatness Mean", "Spectral Flatness Std",
        "Spectral Bandwidth Mean", "Spectral Bandwidth Std",
        "Spectral Contrast Mean", "Spectral Contrast Std",
        # Prosody (32-38)
        "Onset Mean", "Onset Std", "Tempo",
        "Autocorr Mean", "Autocorr Std",
        "Harmonic Ratio", "Percussive Ratio"
    ]
    
    def __init__(self):
        pass
    
    def generate_explanation(
        self,
        classification: str,
        confidence: float,
        features: np.ndarray,
        top_features: list = None
    ) -> str:
        """
        Generate human-readable explanation
        
        Args:
            classification: "AI_GENERATED" or "HUMAN"
            confidence: Confidence score
            features: Feature vector
            top_features: List of (index, value, importance) tuples
            
        Returns:
            Explanation string
        """
        try:
            if classification == "AI_GENERATED":
                explanation = self._explain_ai_voice(confidence, features, top_features)
            else:
                explanation = self._explain_human_voice(confidence, features, top_features)
            
            logger.info(f"Generated explanation: {explanation}")
            return explanation
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {str(e)}")
            return f"Voice classified as {classification} with {confidence:.2%} confidence"
    
    def _explain_ai_voice(self, confidence: float, features: np.ndarray, top_features: list) -> str:
        """Generate explanation for AI-generated voice"""
        explanations = []
        
        # Analyze pitch consistency (features 13-17)
        pitch_std = features[14]  # Pitch Std
        if pitch_std < 20:  # Low variation
            explanations.append("unnatural pitch consistency")
        
        # Analyze spectral flatness (features 26-27)
        spectral_flatness_mean = features[26]
        if spectral_flatness_mean < 0.1:  # Low flatness = tonal
            explanations.append("minimal spectral variations")
        
        # Analyze energy consistency (features 18-21)
        rms_std = features[19]  # RMS Std
        if rms_std < 0.05:  # Low variation
            explanations.append("uniform energy distribution")
        
        # Analyze prosody (features 32-38)
        tempo = features[34]
        if 100 < tempo < 140:  # Very consistent tempo
            explanations.append("mechanical speech rhythm")
        
        # Analyze harmonic content
        harmonic_ratio = features[37]
        if harmonic_ratio > 0.7:  # High harmonic content
            explanations.append("overly smooth harmonic structure")
        
        # Build explanation text
        if not explanations:
            explanations.append("synthetic voice characteristics detected")
        
        # Create final explanation
        if confidence > 0.9:
            strength = "Strong"
        elif confidence > 0.7:
            strength = "Clear"
        else:
            strength = "Moderate"
        
        explanation = f"{strength} indicators of AI generation: {', '.join(explanations[:3])}"
        
        return explanation
    
    def _explain_human_voice(self, confidence: float, features: np.ndarray, top_features: list) -> str:
        """Generate explanation for human voice"""
        explanations = []
        
        # Analyze pitch variation (features 13-17)
        pitch_std = features[14]  # Pitch Std
        if pitch_std > 30:  # High variation
            explanations.append("natural pitch variations")
        
        # Analyze spectral complexity (features 22-31)
        spectral_flatness_mean = features[26]
        if spectral_flatness_mean > 0.15:  # Higher flatness = noisy/complex
            explanations.append("rich spectral complexity")
        
        # Analyze energy dynamics (features 18-21)
        rms_std = features[19]  # RMS Std
        if rms_std > 0.08:  # High variation
            explanations.append("natural energy fluctuations")
        
        # Analyze prosody variation
        onset_std = features[33]  # Onset Std
        if onset_std > 0.5:  # High variation in rhythm
            explanations.append("organic speech rhythm")
        
        # Analyze micro-variations
        autocorr_std = features[36]  # Autocorr Std
        if autocorr_std > 100:  # High variation
            explanations.append("natural micro-variations")
        
        # Build explanation text
        if not explanations:
            explanations.append("human voice characteristics detected")
        
        # Create final explanation
        if confidence > 0.9:
            strength = "Strong"
        elif confidence > 0.7:
            strength = "Clear"
        else:
            strength = "Moderate"
        
        explanation = f"{strength} indicators of human voice: {', '.join(explanations[:3])}"
        
        return explanation
    
    def get_detailed_analysis(self, features: np.ndarray, top_features: list) -> dict:
        """
        Get detailed feature analysis
        
        Args:
            features: Feature vector
            top_features: List of (index, value, importance) tuples
            
        Returns:
            Dictionary with detailed analysis
        """
        analysis = {
            "pitch_analysis": {
                "mean": float(features[13]),
                "std": float(features[14]),
                "range": float(features[17])
            },
            "energy_analysis": {
                "rms_mean": float(features[18]),
                "rms_std": float(features[19]),
                "zcr_mean": float(features[20])
            },
            "spectral_analysis": {
                "centroid_mean": float(features[22]),
                "flatness_mean": float(features[26]),
                "contrast_mean": float(features[30])
            },
            "prosody_analysis": {
                "tempo": float(features[34]),
                "harmonic_ratio": float(features[37])
            }
        }
        
        if top_features:
            analysis["top_contributing_features"] = [
                {
                    "name": self.FEATURE_NAMES[idx],
                    "value": float(val),
                    "importance": float(imp)
                }
                for idx, val, imp in top_features
            ]
        
        return analysis


# Create global explainer instance
explainer = VoiceExplainer()
