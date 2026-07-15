from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(min_length=8)

    role: UserRole = UserRole.STAFF

from uuid import UUID

class UserResponse(BaseModel):

    id: UUID

    name: str

    email: EmailStr

    role: UserRole

    is_active: bool

    model_config = {
        "from_attributes": True
    }

