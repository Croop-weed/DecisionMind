from datetime import datetime
from uuid import UUID

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.decision import Decision
from app.models.enums import DecisionStatus


class DecisionRepository:
    """Repository for Decision model database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, decision: Decision) -> Decision:
        """
        Create a new decision in the database.
        
        Args:
            decision: Decision model instance
            
        Returns:
            The created Decision instance
        """
        self.db.add(decision)
        await self.db.commit()
        await self.db.refresh(decision)
        return decision

    async def get_by_id(self, decision_id: UUID) -> Decision | None:
        """
        Retrieve a decision by its ID.
        
        Args:
            decision_id: UUID of the decision
            
        Returns:
            Decision instance or None if not found
        """
        result = await self.db.execute(
            select(Decision).where(Decision.id == decision_id)
        )
        return result.scalar_one_or_none()

    async def update(self, decision: Decision) -> Decision:
        """
        Update an existing decision.
        
        Args:
            decision: Decision model instance with updated fields
            
        Returns:
            The updated Decision instance
        """
        await self.db.merge(decision)
        await self.db.commit()
        await self.db.refresh(decision)
        return decision

    async def delete(self, decision_id: UUID) -> None:
        """
        Delete a decision by its ID.
        
        Args:
            decision_id: UUID of the decision to delete
        """
        decision = await self.get_by_id(decision_id)
        if decision:
            await self.db.delete(decision)
            await self.db.commit()

    async def list(
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
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            topic: Filter by topic (exact match)
            department: Filter by department (exact match)
            status: Filter by status
            created_by: Filter by creator user ID
            created_after: Filter for decisions created after this date
            created_before: Filter for decisions created before this date
            sort_by: Sort order - "newest" or "oldest"
            
        Returns:
            Tuple of (list of Decision instances, total count)
        """
        # Build filters
        filters = []

        if topic:
            filters.append(Decision.topic == topic)

        if department:
            filters.append(Decision.department == department)

        if status:
            filters.append(Decision.status == status)

        if created_by:
            filters.append(Decision.created_by == created_by)

        if created_after:
            filters.append(Decision.created_at >= created_after)

        if created_before:
            filters.append(Decision.created_at <= created_before)

        # Build query
        query = select(Decision)

        if filters:
            query = query.where(and_(*filters))

        # Sorting
        if sort_by == "oldest":
            query = query.order_by(Decision.created_at.asc())
        else:  # Default: newest
            query = query.order_by(Decision.created_at.desc())

        # Get total count
        count_result = await self.db.execute(
            select(Decision).where(and_(*filters) if filters else True)
        )
        total_count = len(count_result.scalars().all())

        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # Execute query
        result = await self.db.execute(query)
        decisions = result.scalars().all()

        return decisions, total_count

    async def search(self, query: str) -> list[Decision]:
        """
        Search decisions by title or topic.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Decision instances
        """
        search_term = f"%{query.lower()}%"
        
        result = await self.db.execute(
            select(Decision).where(
                or_(
                    Decision.title.ilike(search_term),
                    Decision.topic.ilike(search_term),
                )
            )
        )
        
        return result.scalars().all()

    async def get_by_creator(self, user_id: UUID) -> list[Decision]:
        """
        Get all decisions created by a specific user.
        
        Args:
            user_id: UUID of the creator
            
        Returns:
            List of Decision instances
        """
        result = await self.db.execute(
            select(Decision)
            .where(Decision.created_by == user_id)
            .order_by(Decision.created_at.desc())
        )
        return result.scalars().all()
