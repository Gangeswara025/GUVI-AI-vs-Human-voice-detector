# PowerShell script for testing on Windows

# Replace with your actual API URL and API key
$API_URL = "http://localhost:8000"
$API_KEY = "hackathon_demo_key_2026"

Write-Host "=========================================" -ForegroundColor Green
Write-Host "AI Voice Detection API - Test Requests" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
Write-Host "-------------------"
Invoke-RestMethod -Uri "$API_URL/health" -Method Get
Write-Host "`n"

# Test 2: Convert MP3 to Base64 and send request
Write-Host "Test 2: Voice Detection" -ForegroundColor Yellow
Write-Host "-----------------------"

# If you have an MP3 file, convert it to base64:
# $audioPath = "path\to\your\audio.mp3"
# $audioBytes = [IO.File]::ReadAllBytes($audioPath)
# $audioBase64 = [Convert]::ToBase64String($audioBytes)

# Sample tiny base64 audio (replace with real audio)
$audioBase64 = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAACAAABhADY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY////////////////////////////////////////////////////////////"

$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = $API_KEY
}

$body = @{
    audio_base64 = $audioBase64
    language = "Tamil"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$API_URL/api/v1/detect" -Method Post -Headers $headers -Body $body
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n"
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Test completed!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Helper: Convert MP3 file to Base64
# function Convert-Mp3ToBase64 {
#     param([string]$FilePath)
#     $bytes = [IO.File]::ReadAllBytes($FilePath)
#     return [Convert]::ToBase64String($bytes)
# }
#
# Usage:
# $base64Audio = Convert-Mp3ToBase64 -FilePath "your_audio.mp3"
