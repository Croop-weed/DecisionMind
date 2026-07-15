from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password

class UserService:

    def __init__(self,repository: UserRepository):
        self.repository = repository

    async def create_user(self,data: UserCreate):

        existing = await self.repository.get_by_email(
            data.email
        )

        if existing:
            raise ValueError(
                "Email already registered."
            )

        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            role=data.role,
        )

        return await self.repository.create(user)