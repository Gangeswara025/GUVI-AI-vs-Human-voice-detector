# API Documentation

## AI Voice Detection API v1.0.0

Complete API reference for the AI-Generated Voice Detection system.

---

## Base URL

**Local Development:**
```
http://localhost:8000
```

**Production (Render):**
```
https://your-app-name.onrender.com
```

---

## Authentication

All protected endpoints require an API key in the header:

**Header:**
```
x-api-key: <YOUR_API_KEY>
```

**Default API Key (Development):**
```
hackathon_demo_key_2026
```

⚠️ **Production**: Change this in your `.env` file!

---

## Endpoints

### 1. Root

Get API information.

**Request:**
```http
GET /
```

**Response:**
```json
{
  "message": "AI Voice Detection API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. Health Check

Check API health and model status.

**Request:**
```http
GET /health
```

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true
}
```

---

### 3. Voice Detection

Detect if a voice is AI-generated or human.

**Request:**
```http
POST /api/v1/detect
```

**Authentication:** Required (`x-api-key` header)

**Headers:**
```
Content-Type: application/json
x-api-key: <YOUR_API_KEY>
```

**Request Body:**
```json
{
  "audio_base64": "string (Base64-encoded MP3)",
  "language": "Tamil" | "English" | "Hindi" | "Malayalam" | "Telugu"
}
```

**Field Descriptions:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audio_base64` | string | Yes | Base64-encoded MP3 audio file (max 10MB) |
| `language` | string | Yes | Must be one of: Tamil, English, Hindi, Malayalam, Telugu |

**Success Response (200):**
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.9134,
  "explanation": "Strong indicators of AI generation: unnatural pitch consistency, minimal spectral variations, uniform energy distribution"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always "success" for successful requests |
| `language` | string | Echo of input language |
| `classification` | string | Either "AI_GENERATED" or "HUMAN" |
| `confidenceScore` | float | Confidence between 0.0 and 1.0 |
| `explanation` | string | Human-readable explanation |

**Error Responses:**

#### 400 Bad Request
```json
{
  "status": "error",
  "error": "Invalid base64 encoding",
  "detail": "Failed to decode base64 audio"
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "error": "API key is missing. Please provide x-api-key header."
}
```

#### 403 Forbidden
```json
{
  "status": "error",
  "error": "Invalid API key. Access denied."
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "unexpected value; permitted: 'Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu'",
      "type": "value_error.const"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "error": "Internal server error",
  "detail": "Audio processing error: ..."
}
```

---

## Examples

### Example 1: Successful Detection

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "x-api-key: hackathon_demo_key_2026" \
  -d '{
    "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA...",
    "language": "English"
  }'
```

**Python:**
```python
import requests
import base64

# Read and encode audio
with open("audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Make request
response = requests.post(
    "http://localhost:8000/api/v1/detect",
    headers={"x-api-key": "hackathon_demo_key_2026"},
    json={
        "audio_base64": audio_base64,
        "language": "English"
    }
)

print(response.json())
```

**JavaScript (Node.js):**
```javascript
const fs = require('fs');
const axios = require('axios');

// Read and encode audio
const audioBuffer = fs.readFileSync('audio.mp3');
const audioBase64 = audioBuffer.toString('base64');

// Make request
axios.post('http://localhost:8000/api/v1/detect', {
  audio_base64: audioBase64,
  language: 'English'
}, {
  headers: {
    'x-api-key': 'hackathon_demo_key_2026'
  }
})
.then(response => console.log(response.data))
.catch(error => console.error(error.response.data));
```

### Example 2: Multiple Languages

**Tamil:**
```json
{
  "audio_base64": "...",
  "language": "Tamil"
}
```

**Hindi:**
```json
{
  "audio_base64": "...",
  "language": "Hindi"
}
```

**Malayalam:**
```json
{
  "audio_base64": "...",
  "language": "Malayalam"
}
```

**Telugu:**
```json
{
  "audio_base64": "...",
  "language": "Telugu"
}
```

---

## Rate Limits

Currently no rate limits are enforced. In production, consider:
- Rate limiting per API key
- Request size limits (10MB audio max)
- Concurrent request limits

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing API key) |
| 403 | Forbidden (invalid API key) |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

---

## OpenAPI Specification

Interactive documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Postman Collection

### Import Steps:

1. Open Postman
2. Click "Import"
3. Paste OpenAPI URL: `http://localhost:8000/openapi.json`
4. Set environment variable:
   - Key: `api_key`
   - Value: `hackathon_demo_key_2026`

### Pre-request Script (for Base64 encoding):

```javascript
// Add to Postman pre-request script
// This is a placeholder - you'll need to encode real audio
pm.environment.set("audio_base64", "SUQzBAAAAAAAI1RTU0U...");
```

---

## Testing Checklist

- [ ] Health check responds with 200
- [ ] Valid request with API key succeeds
- [ ] Request without API key returns 401
- [ ] Request with invalid API key returns 403
- [ ] Invalid language returns 422
- [ ] Large audio (>10MB) is rejected
- [ ] Invalid base64 returns 400
- [ ] All 5 languages work correctly
- [ ] Confidence scores are between 0-1
- [ ] Explanations are generated

---

## Support

For issues or questions:
- Check the [README](README.md)
- Review error messages carefully
- Ensure audio is valid MP3 format
- Verify API key is correct

---

**Last Updated:** 2026-01-27  
**Version:** 1.0.0
