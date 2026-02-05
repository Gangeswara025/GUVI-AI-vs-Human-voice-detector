# Sample Audio Files for Testing

This directory contains sample audio files for testing the AI Voice Detection system.

## Files

### AI-Generated Voices (using Google TTS)
These files are generated using text-to-speech engines and should be detected as **AI_GENERATED**:

- `ai_english.mp3` - English AI voice sample
- `ai_tamil.mp3` - Tamil AI voice sample  
- `ai_hindi.mp3` - Hindi AI voice sample

### Human-Like Samples
These are for comparison testing:

- `test_sample.mp3` - Test audio file

## How to Use

1. **Upload to UI**: Use the test_ui.html interface to upload these files
2. **API Testing**: Convert to Base64 and send via API
3. **Expected Results**: AI-generated files should show high confidence for "AI_GENERATED" classification

## Generate More Samples

You can generate additional AI voice samples using the training script:

```bash
cd d:\Guvi-Hackathon
venv\Scripts\activate
python -c "from gtts import gTTS; tts = gTTS('Hello, this is a test', lang='en'); tts.save('sample_audio/my_sample.mp3')"
```

## Base64 Conversion

To convert an MP3 to Base64 for API testing:

**PowerShell:**
```powershell
$bytes = [IO.File]::ReadAllBytes("sample_audio\ai_english.mp3")
$base64 = [Convert]::ToBase64String($bytes)
$base64 | Out-File -FilePath "audio_base64.txt"
```

**Python:**
```python
import base64
with open("sample_audio/ai_english.mp3", "rb") as f:
    base64_audio = base64.b64encode(f.read()).decode()
print(base64_audio)
```
