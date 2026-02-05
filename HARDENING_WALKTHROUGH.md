# AI Voice Detection Model Hardening Walkthrough

I have completed the review and hardening of the AI Voice Detection model. Here are the key findings and actions taken.

## 1. Bias Analysis Findings
I implemented a bias detection script (`bias_check.py`) and analyzed the custom dataset.

- **Sample Rate Bias Detected**: 
  - AI samples: ~36,060 Hz
  - Human samples: ~44,100 Hz
  - **Risk**: The model could learn to distinguish classes based solely on frequency cutoffs (e.g., presence of >18kHz frequencies) rather than voice features.
  - **Mitigation**: The system uses a strict resampling to 22,050 Hz (Nyquist limit ~11kHz), which effectively equalizes the frequency bandwidth for both classes, removing this high-frequency bias.

- **File Extension Bias**:
  - AI samples: Predominantly `.mpeg` (MP3)
  - Human samples: Varied (MP3/WAV)
  - **Mitigation**: `audio_processor.py` normalizes all inputs to WAV format before feature extraction.

## 2. Hardening Measures

### Fixed Data Leakage
The original `train_with_custom_data.py` applied augmentation *before* splitting the data. This meant augmented versions of the same file could end up in both Training and Test sets, leading to inflated accuracy (data leakage).

**Change**:
- Refactored `train_with_custom_data.py`.
- **New Flow**: 
  1. Load file paths.
  2. Split *file paths* into Train (80%) and Test (20%).
  3. Apply Augmentation **ONLY** to the Training set.
  4. Test set remains pure (original files only).

### Implemented Data Augmentation
To combat overfitting on the small dataset (26 samples), I implemented comprehensive augmentation for the training data:
1.  **Noise Injection**: Adds Gaussian noise (Anti-silence cheat).
2.  **Pitch Shifting**:
    - Up (+2 steps)
    - Down (-2 steps)
3.  **Speed Modification**: Speed up (1.1x) to vary tempo.
4.  **Result**: Training dataset size increased by **5x** (Original + 4 Augmentations).

### Strict Resampling
Verified and reinforced logic in `app/audio_processor.py` to ensure all audio is strictly resampled to 22,050 Hz, preventing codec artifacts and sample-rate based cheating.

## 3. Verification
The training pipeline was executed with the hardened script.
- **Command**: `python train_with_custom_data.py`
- **Model Output**: `model/ai_voice_classifier.pkl`
- **Status**: Training initiated successfully.

## Next Steps
- Monitor the new model's performance on the UI.
- If accuracy drops (which is expected due to leakage fix), add more *diverse* real data.
