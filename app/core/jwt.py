from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import setting

def create_access_token(user_id: str, role: str) -> str:
    return _create_token(
        data={
            "sub": user_id,
            "role": role,
        },
        expires_delta=timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        token_type="access",
    )

def create_refresh_token(user_id: str) -> str:

    return _create_token(
        data={
            "sub": user_id,
        },
        expires_delta=timedelta(
            days=setting.REFRESH_TOKEN_EXPIRE_DAYS
        ),
        token_type="refresh",
    )

def decode_token(token: str,expected_type: str | None = None) -> dict:

    try:
        payload = jwt.decode(
            token,
            setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM],
        )

        if expected_type and payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )