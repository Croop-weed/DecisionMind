"""User management router for administrative operations."""

from fastapi import APIRouter, Depends, status

from app.dependencies import get_user_service
from app.core.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Create a new user account. Only administrators can create users."
)
async def create_user(
    request: UserCreate,
    service: UserService = Depends(get_user_service),
    current_admin: User = Depends(get_current_admin),
) -> UserResponse:
    """
    Create user endpoint (admin only).
    
    Create a new user account with the provided details.
    Requires admin privileges.
    """
    return await service.create_user(request)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get the profile of the currently authenticated user."
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Get current user endpoint.
    
    Returns the authenticated user's profile information.
    Note: This is a convenience endpoint. The auth router also provides /auth/me
    """
    return current_user
