from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import DecisionStatus


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    topic: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
    )

    problem_statement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
    )

    status: Mapped[DecisionStatus] = mapped_column(
        Enum(DecisionStatus),
        default=DecisionStatus.DRAFT,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    creator = relationship(
        "User",
        back_populates="decisions",
    )

    documents = relationship(
        "Document",
        back_populates="decision",
        cascade="all, delete-orphan",
    )

    analyses = relationship(
        "DecisionAnalysis",
        back_populates="decision",
        cascade="all, delete-orphan",
    )

    outcomes = relationship(
        "DecisionOutcome",
        back_populates="decision",
        cascade="all, delete-orphan",
    )

    versions = relationship(
        "DecisionVersion",
        back_populates="decision",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "Comment",
        back_populates="decision",
        cascade="all, delete-orphan",
    )

    embeddings = relationship(
        "Embedding",
        back_populates="decision",
        cascade="all, delete-orphan",
    )