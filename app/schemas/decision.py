from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import DecisionStatus


class DecisionCreate(BaseModel):
    """Schema for creating a new decision."""
    
    title: str = Field(min_length=5, max_length=255)
    
    topic: str = Field(min_length=2, max_length=100)
    
    department: str | None = Field(None, max_length=100)
    
    problem_statement: str = Field(min_length=10)
    
    decision: str = Field(min_length=10)
    
    reason: str | None = None
    
    status: DecisionStatus = DecisionStatus.DRAFT


class DecisionUpdate(BaseModel):
    """Schema for updating an existing decision."""
    
    title: str | None = Field(None, min_length=5, max_length=255)
    
    topic: str | None = Field(None, min_length=2, max_length=100)
    
    department: str | None = Field(None, max_length=100)
    
    problem_statement: str | None = Field(None, min_length=10)
    
    decision: str | None = Field(None, min_length=10)
    
    reason: str | None = None
    
    status: DecisionStatus | None = None


class DecisionResponse(BaseModel):
    """Schema for returning a single decision."""
    
    id: UUID
    
    created_by: UUID
    
    title: str
    
    topic: str
    
    department: str | None
    
    problem_statement: str
    
    decision: str
    
    reason: str | None
    
    status: DecisionStatus
    
    created_at: datetime
    
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class DecisionListResponse(BaseModel):
    """Schema for returning a paginated list of decisions."""
    
    items: list[DecisionResponse]
    
    total: int
    
    page: int
    
    page_size: int
    
    total_pages: int
