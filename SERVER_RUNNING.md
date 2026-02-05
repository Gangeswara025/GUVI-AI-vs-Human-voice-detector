# ✅ Your API is Now Running!

## 🎉 Success!

Your **AI Voice Detection API** is successfully running at:

**Local URL**: http://127.0.0.1:8000  
**Docs URL**: http://127.0.0.1:8000/docs

The server is in **reload mode** - it will automatically restart when you make code changes.

---

## 🚀 Quick Testing

### Option 1: Interactive Swagger UI (Easiest)

1. Open your browser and go to: **http://127.0.0.1:8000/docs**
2. You'll see a beautiful interactive API documentation
3. Click on **POST /api/v1/detect** endpoint
4. Click **"Try it out"** button
5. Fill in:
   - **x-api-key**: `hackathon_demo_key_2026`
   - **audio_base64**: (paste base64-encoded MP3)
   - **language**: `Tamil` (or any of: English, Hindi, Malayalam, Telugu)
6. Click **"Execute"**
7. See your result!

### Option 2: PowerShell Test Script

```powershell
.\examples\sample_requests.ps1
```

### Option 3: Test with Your Own Audio File

```powershell
# If you have an MP3 file
python test_helper.py your_audio.mp3 Tamil
```

---

## 📝 Converting MP3 to Base64 (for Testing)

If you want to test with your own audio:

```powershell
# PowerShell command
$bytes = [IO.File]::ReadAllBytes("path\to\your\audio.mp3")
$base64 = [Convert]::ToBase64String($bytes)
$base64 | Out-File -FilePath "audio_base64.txt"
```

Then copy the content from `audio_base64.txt` and use it in your API request.

---

## 🔑 API Key

**Current API Key**: `hackathon_demo_key_2026`

This is set in your `.env` file. For production deployment, change this to a secure random key!

---

## 📡 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | API info |
| `/health` | GET | No | Health check |
| `/api/v1/detect` | POST | Yes | Voice detection |
| `/docs` | GET | No | Interactive API docs |

---

## 🎯 Example Request

```json
{
  "audio_base64": "<your-base64-encoded-mp3>",
  "language": "Tamil"
}
```

**Headers:**
```
x-api-key: hackathon_demo_key_2026
Content-Type: application/json
```

**Expected Response:**
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED" or "HUMAN",
  "confidenceScore": 0.91,
  "explanation": "Strong indicators of AI generation: unnatural pitch consistency..."
}
```

---

## ⚠️ Note About FFmpeg

You may have seen a warning about FFmpeg. This is normal! The API will still work, but for better audio processing, install FFmpeg:

1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your Windows PATH
4. Restart PowerShell

This is optional for testing but recommended for production use.

---

## 🛑 Stopping the Server

Press **Ctrl+C** in the PowerShell terminal to stop the server.

---

## 🌐 Next: Deploy to Cloud

When you're ready to deploy:

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable**: `API_KEY=<your-secret-key>`

See [README.md](README.md) for detailed deployment instructions.

---

## 📚 Documentation

- **README.md** - Complete setup guide
- **API_DOCUMENTATION.md** - Detailed API reference
- **QUICKSTART.md** - 5-minute quick start
- **Walkthrough artifact** - Full project overview

---

**Your hackathon project is ready to go! 🏆**

The server will keep running in this terminal. Open a new PowerShell window for testing.
