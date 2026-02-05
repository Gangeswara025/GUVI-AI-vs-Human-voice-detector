"""
Helper script for testing the API with actual audio files
"""
import base64
import requests
import sys
import json
from pathlib import Path


def convert_mp3_to_base64(file_path: str) -> str:
    """Convert MP3 file to base64 string"""
    with open(file_path, 'rb') as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode('utf-8')


def test_voice_detection(
    audio_file: str,
    language: str,
    api_url: str = "http://localhost:8000",
    api_key: str = "hackathon_demo_key_2026"
):
    """
    Test voice detection with an actual audio file
    
    Args:
        audio_file: Path to MP3 file
        language: Language (Tamil, English, Hindi, Malayalam, Telugu)
        api_url: API base URL
        api_key: API key for authentication
    """
    print(f"\n{'='*60}")
    print(f"Testing Voice Detection API")
    print(f"{'='*60}\n")
    
    # Convert audio to base64
    print(f"📁 Reading audio file: {audio_file}")
    try:
        audio_base64 = convert_mp3_to_base64(audio_file)
        print(f"✅ Audio encoded: {len(audio_base64)} characters")
    except Exception as e:
        print(f"❌ Failed to read audio: {e}")
        return
    
    # Prepare request
    url = f"{api_url}/api/v1/detect"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    payload = {
        "audio_base64": audio_base64,
        "language": language
    }
    
    # Make request
    print(f"\n🔄 Sending request to {url}")
    print(f"📝 Language: {language}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        # Parse response
        data = response.json()
        
        if response.status_code == 200:
            print(f"\n✅ SUCCESS!")
            print(f"{'='*60}")
            print(f"Classification: {data['classification']}")
            print(f"Confidence: {data['confidenceScore']:.2%}")
            print(f"Language: {data['language']}")
            print(f"Explanation: {data['explanation']}")
            print(f"{'='*60}\n")
        else:
            print(f"\n❌ ERROR!")
            print(f"{'='*60}")
            print(json.dumps(data, indent=2))
            print(f"{'='*60}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}\n")
    except json.JSONDecodeError:
        print(f"\n❌ Failed to parse response: {response.text}\n")


def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage: python test_helper.py <audio_file.mp3> <language>")
        print("\nExample:")
        print("  python test_helper.py sample.mp3 Tamil")
        print("\nSupported languages:")
        print("  - Tamil")
        print("  - English")
        print("  - Hindi")
        print("  - Malayalam")
        print("  - Telugu")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2]
    
    # Optional: API URL and key from command line
    api_url = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:8000"
    api_key = sys.argv[4] if len(sys.argv) > 4 else "hackathon_demo_key_2026"
    
    # Validate file exists
    if not Path(audio_file).exists():
        print(f"❌ Error: File not found: {audio_file}")
        sys.exit(1)
    
    # Run test
    test_voice_detection(audio_file, language, api_url, api_key)


if __name__ == "__main__":
    main()
