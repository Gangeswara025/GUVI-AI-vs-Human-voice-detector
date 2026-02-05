#!/bin/bash

# Sample cURL requests for testing the AI Voice Detection API

# Replace with your actual API URL and API key
API_URL="http://localhost:8000"
API_KEY="hackathon_demo_key_2026"

echo "========================================="
echo "AI Voice Detection API - Test Requests"
echo "========================================="
echo ""

# Test 1: Health Check (No API key required)
echo "Test 1: Health Check"
echo "-------------------"
curl -X GET "${API_URL}/health"
echo -e "\n\n"

# Test 2: Voice Detection Request (requires sample base64 audio)
echo "Test 2: Voice Detection (Tamil)"
echo "-------------------------------"

# This is a tiny sample MP3 in base64 (you'll need to replace with actual audio)
# To create base64 from an MP3 file:
# On Linux/Mac: base64 -i your_audio.mp3
# On Windows PowerShell: [Convert]::ToBase64String([IO.File]::ReadAllBytes("your_audio.mp3"))

SAMPLE_AUDIO="SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAACAAABhADY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY////////////////////////////////////////////////////////////"

curl -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "{
    \"audio_base64\": \"${SAMPLE_AUDIO}\",
    \"language\": \"Tamil\"
  }"
echo -e "\n\n"

# Test 3: Request without API key (should fail)
echo "Test 3: Request without API key (should fail with 401)"
echo "-------------------------------------------------------"
curl -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -d "{
    \"audio_base64\": \"${SAMPLE_AUDIO}\",
    \"language\": \"English\"
  }"
echo -e "\n\n"

# Test 4: Request with invalid API key (should fail)
echo "Test 4: Request with invalid API key (should fail with 403)"
echo "------------------------------------------------------------"
curl -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "x-api-key: invalid_key_123" \
  -d "{
    \"audio_base64\": \"${SAMPLE_AUDIO}\",
    \"language\": \"Hindi\"
  }"
echo -e "\n\n"

# Test 5: Request with invalid language (should fail)
echo "Test 5: Request with invalid language (should fail with 422)"
echo "-------------------------------------------------------------"
curl -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "{
    \"audio_base64\": \"${SAMPLE_AUDIO}\",
    \"language\": \"French\"
  }"
echo -e "\n\n"

echo "========================================="
echo "Tests completed!"
echo "========================================="
