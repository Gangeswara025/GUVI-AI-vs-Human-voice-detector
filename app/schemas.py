"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Literal


class VoiceDetectionRequest(BaseModel):
    """Request model for voice detection endpoint"""
    
    audio_base64: str = Field(
        ...,
        description="Base64-encoded MP3 audio file",
        min_length=100
    )
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ...,
        description="Language of the audio sample"
    )
    
    @validator("audio_base64")
    def validate_base64(cls, v):
        """Validate base64 string"""
        import base64
        try:
            # Try to decode to verify it's valid base64
            base64.b64decode(v, validate=True)
            return v
        except Exception:
            raise ValueError("Invalid base64 encoding")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA...",
                "language": "Tamil"
            }
        }
    }


class VoiceDetectionResponse(BaseModel):
    """Response model for voice detection endpoint"""
    
    status: Literal["success", "error"] = Field(
        ...,
        description="Status of the request"
    )
    language: str = Field(
        ...,
        description="Language of the audio sample"
    )
    classification: Literal["AI_GENERATED", "HUMAN"] = Field(
        ...,
        description="Classification result"
    )
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0"
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the classification"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "language": "Tamil",
                "classification": "AI_GENERATED",
                "confidenceScore": 0.91,
                "explanation": "Unnatural pitch consistency detected with minimal spectral variations"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Error response model"""
    
    status: Literal["error"] = "error"
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Detailed error information")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "error",
                "error": "Invalid audio format",
                "detail": "Audio file must be in MP3 format"
            }
        }
    }


class HealthResponse(BaseModel):
    """Health check response model"""
    
    status: str = "healthy"
    version: str = "1.0.0"
    is_model_loaded: bool = Field(True, alias="model_loaded")
    
    model_config = {
        "protected_namespaces": ()
    }
