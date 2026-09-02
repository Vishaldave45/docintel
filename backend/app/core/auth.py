"""API Key Authentication Dependency and Verification."""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    header_key: str | None = Security(api_key_header),
) -> str | None:
    """Verify API key for protected write endpoints.

    In development/default mode where DOCINTEL_API_KEY is not set,
    requests pass through without error. When DOCINTEL_API_KEY is configured,
    a matching X-API-Key header is strictly required.
    """
    configured_key = settings.api_key
    if not configured_key:
        return None

    if not header_key or header_key != configured_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key in 'X-API-Key' header",
        )

    return header_key
