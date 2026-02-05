"""
Unit tests for AI Voice Detection API
"""
import pytest
import base64
import json
from fastapi.testclient import TestClient
from main import app
from app.config import config

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "model_loaded" in data


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestAuthentication:
    """Test API key authentication"""
    
    def test_missing_api_key(self):
        """Test request without API key"""
        response = client.post(
            "/api/v1/detect",
            json={
                "audio_base64": "dGVzdA==",
                "language": "English"
            }
        )
        assert response.status_code == 401
    
    def test_invalid_api_key(self):
        """Test request with invalid API key"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": "invalid_key"},
            json={
                "audio_base64": "dGVzdA==",
                "language": "English"
            }
        )
        assert response.status_code == 403
    
    def test_valid_api_key(self):
        """Test request with valid API key (may fail on invalid audio)"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": config.API_KEY},
            json={
                "audio_base64": "dGVzdA==",
                "language": "English"
            }
        )
        # Will return 400 or 500 due to invalid audio, but not 401/403
        assert response.status_code not in [401, 403]


class TestValidation:
    """Test request validation"""
    
    def test_invalid_language(self):
        """Test request with unsupported language"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": config.API_KEY},
            json={
                "audio_base64": "dGVzdA==",
                "language": "French"
            }
        )
        assert response.status_code == 422
    
    def test_missing_audio(self):
        """Test request without audio"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": config.API_KEY},
            json={
                "language": "English"
            }
        )
        assert response.status_code == 422
    
    def test_missing_language(self):
        """Test request without language"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": config.API_KEY},
            json={
                "audio_base64": "dGVzdA=="
            }
        )
        assert response.status_code == 422


class TestAudioProcessing:
    """Test audio processing"""
    
    def test_invalid_base64(self):
        """Test request with invalid base64"""
        response = client.post(
            "/api/v1/detect",
            headers={"x-api-key": config.API_KEY},
            json={
                "audio_base64": "not-valid-base64!!!",
                "language": "English"
            }
        )
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
