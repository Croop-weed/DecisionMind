from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status

from app.models.decision import Decision
from app.models.enums import DecisionStatus, UserRole
from app.models.user import User
from app.repositories.decision_repository import DecisionRepository
from app.schemas.decision import DecisionCreate, DecisionUpdate


class DecisionService:
    """Service for decision management business logic."""

    def __init__(self, repository: DecisionRepository):
        self.repository = repository

    async def create_decision(
        self,
        data: DecisionCreate,
        current_user: User,
    ) -> Decision:
        """
        Create a new decision.
        
        Authorization: Admin, Manager
        
        Args:
            data: DecisionCreate schema
            current_user: Current authenticated user
            
        Returns:
            Created Decision instance
            
        Raises:
            HTTPException: 403 if user lacks permission
        """
        # Permission check: Only Admin and Manager can create
        if current_user.role not in (UserRole.ADMIN, UserRole.MANAGER):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Admin and Manager can create decisions.",
            )

        decision = Decision(
            created_by=current_user.id,
            title=data.title,
            topic=data.topic,
            department=data.department,
            problem_statement=data.problem_statement,
            decision=data.decision,
            reason=data.reason,
            status=data.status,
        )

        return await self.repository.create(decision)

    async def get_decision(self, decision_id: UUID) -> Decision:
        """
        Get a decision by ID.
        
        Authorization: Any authenticated user
        
        Args:
            decision_id: UUID of the decision
            
        Returns:
            Decision instance
            
        Raises:
            HTTPException: 404 if decision not found
        """
        decision = await self.repository.get_by_id(decision_id)

        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found.",
            )

        return decision

    async def update_decision(
        self,
        decision_id: UUID,
        data: DecisionUpdate,
        current_user: User,
    ) -> Decision:
        """
        Update an existing decision.
        
        Authorization: Admin (any decision), Manager (own decision only)
        
        Args:
            decision_id: UUID of the decision to update
            data: DecisionUpdate schema with updated fields
            current_user: Current authenticated user
            
        Returns:
            Updated Decision instance
            
        Raises:
            HTTPException: 404 if decision not found, 403 if permission denied
        """
        decision = await self.repository.get_by_id(decision_id)

        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found.",
            )

        # Permission check: Only Admin or the Manager who created it
        is_admin = current_user.role == UserRole.ADMIN
        is_creator = decision.created_by == current_user.id

        if not is_admin and not (current_user.role == UserRole.MANAGER and is_creator):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own decisions.",
            )

        # Update only provided fields
        if data.title is not None:
            decision.title = data.title

        if data.topic is not None:
            decision.topic = data.topic

        if data.department is not None:
            decision.department = data.department

        if data.problem_statement is not None:
            decision.problem_statement = data.problem_statement

        if data.decision is not None:
            decision.decision = data.decision

        if data.reason is not None:
            decision.reason = data.reason

        if data.status is not None:
            decision.status = data.status

        return await self.repository.update(decision)

    async def delete_decision(
        self,
        decision_id: UUID,
        current_user: User,
    ) -> None:
        """
        Delete a decision.
        
        Authorization: Admin only
        
        Args:
            decision_id: UUID of the decision to delete
            current_user: Current authenticated user
            
        Raises:
            HTTPException: 404 if decision not found, 403 if not admin
        """
        decision = await self.repository.get_by_id(decision_id)

        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found.",
            )

        # Permission check: Only Admin can delete
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Admin can delete decisions.",
            )

        await self.repository.delete(decision_id)

    async def list_decisions(
        self,
        page: int = 1,
        page_size: int = 10,
        topic: str | None = None,
        department: str | None = None,
        status: DecisionStatus | None = None,
        created_by: UUID | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
        sort_by: str = "newest",
    ) -> tuple[list[Decision], int]:
        """
        List decisions with filtering and pagination.
        
        Authorization: Any authenticated user
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            topic: Filter by topic
            department: Filter by department
            status: Filter by status
            created_by: Filter by creator
            created_after: Filter for decisions created after this date
            created_before: Filter for decisions created before this date
            sort_by: Sort order - "newest" or "oldest"
            
        Returns:
            Tuple of (list of decisions, total count)
        """
        return await self.repository.list(
            page=page,
            page_size=page_size,
            topic=topic,
            department=department,
            status=status,
            created_by=created_by,
            created_after=created_after,
            created_before=created_before,
            sort_by=sort_by,
        )

    async def search_decisions(self, query: str) -> list[Decision]:
        """
        Search decisions by title or topic.
        
        Authorization: Any authenticated user
        
        Args:
            query: Search query string
            
        Returns:
            List of matching decisions
        """
        return await self.repository.search(query)
