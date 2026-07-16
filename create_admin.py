"""
Script to create the initial admin user for DecisionMind.

Usage:
    uv run python create_admin.py
"""

import asyncio
import sys
from uuid import UUID

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.hashing import hash_password
from app.models.user import User
from app.models.enums import UserRole


async def create_admin():
    """Create an initial admin user if one doesn't exist."""
    admin_email = "admin@decisionmind.com"
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if admin already exists
            result = await session.execute(
                select(User).where(User.email == admin_email)
            )
            existing_admin = result.scalar_one_or_none()
            
            if existing_admin:
                print(f"✓ Admin user already exists: {admin_email}")
                print(f"  ID: {existing_admin.id}")
                print(f"  Name: {existing_admin.name}")
                print(f"  Role: {existing_admin.role}")
                return
            
            # Create new admin user
            admin_user = User(
                name="Super Admin",
                email=admin_email,
                password_hash=hash_password("ChangeMe123!"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            
            session.add(admin_user)
            await session.commit()
            
            print("✓ Admin user created successfully!")
            print(f"  Email: {admin_email}")
            print(f"  Password: ChangeMe123!")
            print(f"  ID: {admin_user.id}")
            print(f"  Role: {admin_user.role}")
            print("\n⚠️  IMPORTANT: Change the password immediately in production!")
            
        except Exception as e:
            await session.rollback()
            print(f"✗ Error creating admin user: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_admin())
