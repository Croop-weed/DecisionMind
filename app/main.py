from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

app = FastAPI(
    title="DecisionAI Backend",
    description="Authentication & Authorization for DecisionMind",
    version="1.0.0",
)

from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router
from app.api.v1.decision import router as decision_router

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(decision_router)

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Ping the database
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(e)}"
        )

