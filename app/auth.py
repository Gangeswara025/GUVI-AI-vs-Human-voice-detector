"""
API Key authentication middleware
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import config

# Define API Key header
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify the API key from request headers
    
    Args:
        api_key: API key from x-api-key header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please provide x-api-key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Access denied.",
        )
    
    return api_key
