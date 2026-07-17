"""Decision management router for CRUD operations."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user
from app.dependencies import get_decision_service
from app.models.user import User
from app.models.enums import DecisionStatus
from app.schemas.decision import (
    DecisionCreate,
    DecisionUpdate,
    DecisionResponse,
    DecisionListResponse,
)
from app.services.decision_service import DecisionService

router = APIRouter(
    prefix="/api/v1/decisions",
    tags=["Decisions"],
)


@router.post(
    "",
    response_model=DecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new decision",
    description="Create a new decision. Only Admin and Manager can create decisions.",
)
async def create_decision(
    request: DecisionCreate,
    service: DecisionService = Depends(get_decision_service),
    current_user: User = Depends(get_current_user),
) -> DecisionResponse:
    """
    Create a new decision.
    
    Requires authentication. Only Admin and Manager roles can create decisions.
    Staff users will receive a 403 Forbidden response.
    """
    decision = await service.create_decision(request, current_user)
    return decision


@router.get(
    "",
    response_model=DecisionListResponse,
    status_code=status.HTTP_200_OK,
    summary="List decisions",
    description="Get a paginated list of decisions with optional filtering.",
)
async def list_decisions(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    topic: str | None = Query(None, description="Filter by topic"),
    department: str | None = Query(None, description="Filter by department"),
    status: DecisionStatus | None = Query(None, description="Filter by status"),
    created_by: UUID | None = Query(None, description="Filter by creator user ID"),
    sort_by: str = Query("newest", pattern="^(newest|oldest)$", description="Sort order"),
    service: DecisionService = Depends(get_decision_service),
    current_user: User = Depends(get_current_user),
) -> DecisionListResponse:
    """
    List all decisions with optional filtering and pagination.
    
    Supports filters:
    - topic: exact match on topic
    - department: exact match on department
    - status: filter by decision status
    - created_by: filter by creator user ID
    - sort_by: "newest" (default) or "oldest"
    
    Pagination:
    - page: page number (default 1)
    - page_size: items per page (default 10, max 100)
    """
    decisions, total_count = await service.list_decisions(
        page=page,
        page_size=page_size,
        topic=topic,
        department=department,
        status=status,
        created_by=created_by,
        sort_by=sort_by,
    )

    total_pages = (total_count + page_size - 1) // page_size

    return DecisionListResponse(
        items=decisions,
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{decision_id}",
    response_model=DecisionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get decision by ID",
    description="Retrieve a specific decision by its ID.",
)
async def get_decision(
    decision_id: UUID,
    service: DecisionService = Depends(get_decision_service),
    current_user: User = Depends(get_current_user),
) -> DecisionResponse:
    """
    Get a specific decision by ID.
    
    Any authenticated user can retrieve decisions.
    Returns 404 if decision not found.
    """
    decision = await service.get_decision(decision_id)
    return decision


@router.patch(
    "/{decision_id}",
    response_model=DecisionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update decision",
    description="Update an existing decision. Admin can update any decision. Manager can only update their own.",
)
async def update_decision(
    decision_id: UUID,
    request: DecisionUpdate,
    service: DecisionService = Depends(get_decision_service),
    current_user: User = Depends(get_current_user),
) -> DecisionResponse:
    """
    Update a decision.
    
    Authorization:
    - Admin: can update any decision
    - Manager: can only update decisions they created
    - Staff: cannot update (403 Forbidden)
    
    Only provided fields are updated. Fields omitted from request are not changed.
    Returns 404 if decision not found.
    Returns 403 if insufficient permissions.
    """
    decision = await service.update_decision(decision_id, request, current_user)
    return decision


@router.delete(
    "/{decision_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete decision",
    description="Delete a decision. Only Admin can delete decisions.",
)
async def delete_decision(
    decision_id: UUID,
    service: DecisionService = Depends(get_decision_service),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a decision.
    
    Authorization: Admin only
    
    Returns 404 if decision not found.
    Returns 403 if not admin.
    Returns 204 No Content on success.
    """
    await service.delete_decision(decision_id, current_user)
