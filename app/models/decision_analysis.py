from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class DecisionAnalysis(Base):
    __tablename__ = "decision_analyses"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    decision_id: Mapped[UUID] = mapped_column(
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    pros: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    cons: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    risks: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    alternatives: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    assumptions: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
    )

    prompt_version: Mapped[str] = mapped_column(
        String(30),
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    decision: Mapped["Decision"] = relationship(
        "Decision",
        back_populates="analyses",
    )