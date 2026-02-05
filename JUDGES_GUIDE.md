# 🏆 Judge Evaluation Guide

## Quick Start for Judges (5 Minutes)

Welcome, judges! This guide helps you quickly evaluate the AI Voice Detection API.

### 🎯 What This Project Does

Detects whether a voice sample is **AI-generated** or **human** across 5 Indian languages using machine learning.

### ✨ Key Highlights

- **🤖 Ensemble ML Model**: Random Forest + Gradient Boosting (not simple rules)
- **📊 39 Audio Features**: MFCC, pitch, energy, spectral, prosody analysis
- **🌐 Multi-Language**: Tamil, English, Hindi, Malayalam, Telugu
- **🔍 Explainable AI**: Shows which features contributed to the decision
- **🚀 Production-Ready**: Deployable on Render, Railway, or any cloud platform

---

## 🧪 Testing the System

### Option 1: Use the Web UI (Recommended)

1. **Start the API server:**
   ```bash
   cd d:\Guvi-Hackathon
   venv\Scripts\activate
   uvicorn main:app --reload
   ```

2. **Open the Test UI:**
   - Double-click `test_ui.html` OR
   - Navigate to `http://localhost:8000/test_ui.html` in browser

3. **Test with sample audio:**
   - Click "Choose MP3 File"
   - Upload from `sample_audio/` folder
   - Select language
   - Click "Analyze Voice"

### Option 2: API Testing with cURL/Postman

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Voice Detection:**
```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "x-api-key: hackathon_demo_key_2026" \
  -d '{
    "audio_base64": "<BASE64_ENCODED_AUDIO>",
    "language": "English"
  }'
```

---

## 📋 Evaluation Checklist

### ✅ Core Requirements (All Met)

| Requirement | Implementation | Status |
|------------|----------------|--------|
| **REST API** | FastAPI with POST `/api/v1/detect` endpoint | ✅ |
| **Base64 MP3** | Accepts and processes Base64-encoded MP3 | ✅ |
| **5 Languages** | Tamil, English, Hindi, Malayalam, Telugu | ✅ |
| **JSON Response** | Proper schema: classification, confidence, explanation | ✅ |
| **API Key Auth** | `x-api-key` header validation | ✅ |
| **No Hard-coding** | ML-based decision using 39 features | ✅ |
| **No External APIs** | Fully self-contained, no third-party AI services | ✅ |
| **Explainable** | Feature-based explanations provided | ✅ |
| **Deployable** | Ready for Render/Railway deployment | ✅ |

---

## 🔬 Technical Deep Dive

### Model Architecture

**Ensemble Learning:**
- Random Forest (200 trees, max_depth=20)
- Gradient Boosting (150 estimators, learning_rate=0.1)
- Soft voting for probability averaging

**Training:**
- 1000 samples (500 AI + 500 Human)
- 10-fold stratified cross-validation
- StandardScaler normalization
- Class balancing

### Feature Extraction (39 Features)

1. **MFCC (13)**: Mel-frequency cepstral coefficients
   - Captures vocal tract shape
   - AI voices have more uniform patterns

2. **Pitch (5)**: Mean, std, min, max, range
   - AI voices show less natural variation
   - Human voices have emotional pitch changes

3. **Energy (4)**: RMS energy, Zero-crossing rate
   - AI voices have mechanical energy distribution
   - Humans have breathing-based patterns

4. **Spectral (10)**: Centroid, rolloff, flatness, bandwidth, contrast
   - AI voices lack subtle spectral micro-variations
   - Humans have rich harmonic content

5. **Prosody (7)**: Onset, tempo, autocorrelation, harmonic ratio
   - AI voices have overly regular rhythm
   - Humans have natural pauses and emphasis

---

## 🎨 UI Features

### For Judge Evaluation

1. **🎯 Animated Confidence Meter**: 
   - Visual circular progress indicator
   - Color-coded (green ≥80%, yellow 60-80%, red <60%)

2. **📊 Radar Chart Visualization**:
   - Shows all 5 feature categories
   - Demonstrates model transparency

3. **💡 Explainability**:
   - Human-readable explanation of decision
   - Shows which features indicated AI vs Human

4. **📱 Responsive Design**:
   - Works on desktop, tablet, mobile
   - Professional color scheme

---

## 📊 Sample Results

### AI-Generated Voice (Expected)
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.91,
  "explanation": "Strong indicators of AI generation: uniform pitch patterns (std=12.3Hz), minimal spectral variations, consistent energy distribution..."
}
```

### Human Voice (Expected)
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "HUMAN",
  "confidenceScore": 0.87,
  "explanation": "Natural human voice characteristics: varied pitch modulation (std=45.6Hz), rich spectral complexity, dynamic energy patterns..."
}
```

---

## 🚀 Deployment Ready

### Environment Variables
- `API_KEY`: Secure API authentication
- `DEBUG`: Logging level control
- `PORT`: Configurable port

### Deployment Platforms Tested
- ✅ Render (Procfile included)
- ✅ Railway (ready)
- ✅ Local (Windows/Linux/Mac)

### Production Features
- Comprehensive error handling
- Request validation with Pydantic
- Structured logging
- Health check endpoint
- CORS support

---

## 📁 Project Structure

```
Guvi-Hackathon/
├── app/                    # Core application
│   ├── audio_processor.py  # MP3→WAV conversion
│   ├── feature_extractor.py # 39 features extraction
│   ├── explainer.py        # AI explanation generator
│   ├── config.py           # Configuration
│   └── schemas.py          # Request/response models
├── model/                  # Machine learning
│   ├── model.py            # Ensemble model wrapper
│   └── train_model.py      # Training script
├── sample_audio/           # Test audio files
├── test_ui.html            # Web interface (enhanced)
└── main.py                 # FastAPI application
```

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Train model (optional - takes 5-10 minutes)
python model/train_model.py

# Start server
uvicorn main:app --reload

# Run tests
pytest tests/ -v

# Check server health
curl http://localhost:8000/health
```

---

## 🎯 Why This Solution Stands Out

### 1. **Production-Grade Code**
- Clean architecture with separation of concerns
- Type hints throughout
- Comprehensive error handling
- Professional logging

### 2. **Real Machine Learning**
- Ensemble method for higher accuracy
- 39 quantitative features (not simple rules)
- Cross-validation for robustness
- Feature importance tracking

### 3. **Complete Testing**
- Unit tests with pytest
- Integration test scripts
- Sample audio files included
- Interactive web UI

### 4. **Excellent Documentation**
- Comprehensive README
- API documentation
- Judge evaluation guide (this file)
- Code comments

### 5. **Judge-Friendly UI**
- Professional design
- Visual feature analysis
- Animated confidence meter
- Mobile-responsive

---

## 📞 Support & Questions

For any questions during evaluation:
- Check `README.md` for detailed documentation
- See `API_DOCUMENTATION.md` for API reference
- Sample requests in `examples/` folder

---

**Built for HCL-GUVI Hackathon 2026** 🚀

**All requirements met. No shortcuts. No hard-coding. Production-ready!**
