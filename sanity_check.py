import base64
import requests
import sys
import os

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/detect"
# Default API key from config.py or .env.example (usually 'test_secret_key' or similar for dev)
# You may need to change this if you set a custom API Key
API_KEY = "test_key_12345" 

def test_audio(path, expected_label=None):
    print(f"\n🎧 Testing: {path}")
    
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    try:
        with open(path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()

        response = requests.post(
            API_URL,
            headers={"x-api-key": API_KEY},
            json={"audio_base64": audio_b64, "language": "en"}
        )
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get('classification')
            confidence = result.get('confidenceScore')
            explanation = result.get('explanation', {}).get('summary', '')
            
            print(f"✅ Prediction: {prediction}")
            print(f"📊 Confidence: {confidence}")
            print(f"📝 Reason: {explanation}")
            
            if expected_label:
                if prediction == expected_label:
                    print("🎉 PASS: Clean match!")
                else:
                    print(f"⚠️ FAIL: Expected {expected_label}, got {prediction}")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Script Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Sanity Check...")
    print(f"Target: {API_URL}")
    
    # You can pass files as arguments or use defaults
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            test_audio(f)
    else:
        # Default test files - CHANGE THESE PATHS to actual files you have
        print("\nUsing default test paths (Update these in sanity_check.py if needed)")
        
        # Example paths - User should update these to point to real files they kept aside
        test_audio("sample_audio/human_sample.mp3", expected_label="HUMAN")
        test_audio("sample_audio/ai_sample.mp3", expected_label="AI_GENERATED")
