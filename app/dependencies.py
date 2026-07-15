"""
Dependency providers for repositories and services.

These functions provide instances of repositories and services
without manual instantiation in route handlers.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService


async def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Provide UserRepository instance."""
    return UserRepository(db)


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Provide UserService instance."""
    return UserService(repository)


async def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Provide AuthService instance."""
    return AuthService(repository)
