"""
Utility functions for the API
"""
import logging
import base64
from typing import Dict, Any


def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def validate_language(language: str, supported_languages: list) -> bool:
    """
    Validate if the language is supported
    
    Args:
        language: Language to validate
        supported_languages: List of supported languages
        
    Returns:
        True if language is supported
    """
    return language in supported_languages


def validate_base64_size(base64_string: str, max_size_bytes: int) -> bool:
    """
    Validate the size of base64 encoded data
    
    Args:
        base64_string: Base64 encoded string
        max_size_bytes: Maximum allowed size in bytes
        
    Returns:
        True if size is within limits
    """
    # Calculate approximate decoded size
    # Base64 encoding increases size by ~33%
    decoded_size = (len(base64_string) * 3) / 4
    return decoded_size <= max_size_bytes


def create_error_response(error: str, detail: str = None) -> Dict[str, Any]:
    """
    Create a standardized error response
    
    Args:
        error: Error message
        detail: Detailed error information
        
    Returns:
        Error response dictionary
    """
    response = {
        "status": "error",
        "error": error
    }
    if detail:
        response["detail"] = detail
    return response


def decode_base64_audio(base64_string: str) -> bytes:
    """
    Decode base64 audio data
    
    Args:
        base64_string: Base64 encoded audio
        
    Returns:
        Decoded audio bytes
        
    Raises:
        ValueError: If decoding fails
    """
    try:
        # Remove any whitespace or newlines
        base64_string = base64_string.strip().replace('\n', '').replace('\r', '')
        
        # Decode base64
        audio_bytes = base64.b64decode(base64_string, validate=True)
        
        logger.info(f"Decoded audio: {len(audio_bytes)} bytes")
        return audio_bytes
        
    except Exception as e:
        logger.error(f"Base64 decoding failed: {str(e)}")
        raise ValueError(f"Failed to decode base64 audio: {str(e)}")
