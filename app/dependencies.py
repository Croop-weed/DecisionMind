"""
Dependency providers for repositories and services.

These functions provide instances of repositories and services
without manual instantiation in route handlers.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.decision_repository import DecisionRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.decision_service import DecisionService


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


async def get_decision_repository(
    db: AsyncSession = Depends(get_db),
) -> DecisionRepository:
    """Provide DecisionRepository instance."""
    return DecisionRepository(db)


async def get_decision_service(
    repository: DecisionRepository = Depends(get_decision_repository),
) -> DecisionService:
    """Provide DecisionService instance."""
    return DecisionService(repository)
