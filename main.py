"""
Main FastAPI application for AI Voice Detection API
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from contextlib import asynccontextmanager

from app.config import config
from app.schemas import (
    VoiceDetectionRequest,
    VoiceDetectionResponse,
    ErrorResponse,
    HealthResponse
)
from app.auth import verify_api_key
from app.utils import logger, decode_base64_audio, create_error_response
from app.audio_processor import AudioProcessor
from app.feature_extractor import FeatureExtractor
from model.model import voice_model
from app.explainer import explainer


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    logger.info("Starting AI Voice Detection API...")
    logger.info(f"Loading model from {config.MODEL_PATH}")
    voice_model.load_model()
    logger.info("Model loaded successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API...")


# Create FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="Detect whether a voice sample is AI-generated or human across multiple Indian languages",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
audio_processor = AudioProcessor()
feature_extractor = FeatureExtractor()


@app.get("/", tags=["UI"])
async def serve_ui():
    """Serve the Voice Detection UI"""
    return FileResponse("test_ui.html")


@app.get("/api-info", tags=["Root"])
async def api_info():
    """API Information endpoint"""
    return {
        "message": "AI Voice Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=voice_model.is_loaded
    )


@app.post(
    "/api/v1/detect",
    response_model=VoiceDetectionResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    tags=["Voice Detection"]
)
async def detect_voice(
    request: VoiceDetectionRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Detect if a voice sample is AI-generated or human
    
    **Authentication**: Requires `x-api-key` header
    
    **Supported Languages**: Tamil, English, Hindi, Malayalam, Telugu
    
    **Input**: Base64-encoded MP3 audio file
    
    **Output**: Classification result with confidence score and explanation
    """
    try:
        logger.info(f"Processing voice detection request for language: {request.language}")
        
        # Step 1: Decode base64 audio
        try:
            audio_bytes = decode_base64_audio(request.audio_base64)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Step 2: Validate audio size
        if len(audio_bytes) > config.MAX_AUDIO_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Audio file too large. Maximum size: {config.MAX_AUDIO_SIZE_MB}MB"
            )
        
        # Step 3: Process audio (MP3 -> WAV, normalize)
        try:
            audio_array, sample_rate = audio_processor.process_audio(audio_bytes)
            audio_processor.validate_audio_duration(audio_array)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Audio processing failed: {str(e)}"
            )
        
        # Step 4: Extract features
        try:
            features = feature_extractor.extract_features(audio_array)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Feature extraction failed: {str(e)}"
            )
        
        # Step 5: Make prediction
        try:
            classification, confidence, probabilities = voice_model.predict(features)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Model prediction failed: {str(e)}"
            )
        
        # Step 6: Get top features for explainability
        top_features = voice_model.get_top_features(features, n_top=5)
        
        # Step 7: Generate explanation
        explanation = explainer.generate_explanation(
            classification=classification,
            confidence=confidence,
            features=features,
            top_features=top_features
        )
        
        # Step 8: Create response
        response = VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence, 4),
            explanation=explanation
        )
        
        logger.info(f"Detection complete: {classification} ({confidence:.3f})")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            error=exc.detail,
            detail=str(exc.detail) if hasattr(exc, 'detail') else None
        )
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            error="Internal server error",
            detail=str(exc)
        )
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
