from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    payload = decode_token(
        token,
        expected_type="access",
    )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # TODO:
    # Query the database using user_id
    # Verify user exists
    # Verify user.is_active

    return payload