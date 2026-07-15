from fastapi import HTTPException, status

from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.hashing import verify_password
from app.repositories.user_repository import UserRepository
from app.models.user import User


class AuthService:
    """Service for authentication operations."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(self, email: str, password: str) -> dict:
        """
        Authenticate user and return tokens.
        
        Steps:
        1. Find user by email
        2. Verify password
        3. Verify account is active
        4. Generate and return access & refresh tokens
        """
        user = await self.repository.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        refresh_token = create_refresh_token(
            user_id=str(user.id),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    
    async def refresh(self, refresh_token: str) -> dict:
        """
        Refresh access token using refresh token.
        
        Steps:
        1. Verify refresh token
        2. Load user from database
        3. Generate new access token
        4. Return token response
        """
        payload = decode_token(
            refresh_token,
            expected_type="refresh",
        )

        user = await self.repository.get_by_id(payload["sub"])

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

