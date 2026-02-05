"""
Generate sample audio files for testing the AI Voice Detection system
Creates AI-generated voice samples using Google TTS
"""
from gtts import gTTS
import os
from pathlib import Path

# Sample texts in different languages
samples = {
    "ai_english.mp3": {
        "text": "Hello, this is an AI generated voice sample for testing the voice detection system.",
        "lang": "en"
    },
    "ai_tamil.mp3": {
        "text": "வணக்கம், இது குரல் கண்டறிதல் அமைப்பை சோதிக்க செயற்கை நுண்ணறிவு உருவாக்கிய குரல் மாதிரி.",
        "lang": "ta"
    },
    "ai_hindi.mp3": {
        "text": "नमस्ते, यह वॉयस डिटेक्शन सिस्टम का परीक्षण करने के लिए एक एआई जेनरेट की गई वॉयस सैंपल है।",
        "lang": "hi"
    },
    "ai_malayalam.mp3": {
        "text": "നമസ്കാരം, ഇത് വോയ്‌സ് ഡിറ്റക്ഷൻ സിസ്റ്റം പരീക്ഷിക്കാൻ AI സൃഷ്ടിച്ച വോയ്‌സ് സാമ്പിൾ ആണ്.",
        "lang": "ml"
    },
    "ai_telugu.mp3": {
        "text": "నమస్కారం, ఇది వాయిస్ డిటెక్షన్ సిస్టమ్‌ను పరీక్షించడానికి AI సృష్టించిన వాయిస్ శాంపిల్.",
        "lang": "te"
    }
}

def generate_samples():
    """Generate all sample audio files"""
    # Create directory
    sample_dir = Path(__file__).parent.parent / "sample_audio"
    sample_dir.mkdir(exist_ok=True)
    
    print("🎙️ Generating sample audio files...")
    print(f"📁 Output directory: {sample_dir}")
    print()
    
    for filename, data in samples.items():
        try:
            filepath = sample_dir / filename
            print(f"   Generating {filename}...")
            
            tts = gTTS(text=data["text"], lang=data["lang"], slow=False)
            tts.save(str(filepath))
            
            # Get file size
            size_kb = filepath.stat().st_size / 1024
            print(f"   ✅ Created {filename} ({size_kb:.1f} KB)")
            
        except Exception as e:
            print(f"   ❌ Failed to create {filename}: {str(e)}")
    
    print()
    print("✅ Sample generation complete!")
    print(f"📊 Total files: {len(samples)}")
    print(f"📂 Location: {sample_dir}")
    print()
    print("💡 You can now use these files to test the UI:")
    print("   1. Open test_ui.html")
    print("   2. Upload any of these MP3 files")
    print("   3. They should be detected as 'AI_GENERATED'")

if __name__ == "__main__":
    generate_samples()
