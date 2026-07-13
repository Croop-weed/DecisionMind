from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    STAFF = "STAFF"


class DecisionStatus(str, Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    ARCHIVED = "ARCHIVED"


class DocumentType(str, Enum):
    MEETING = "MEETING"
    RFC = "RFC"
    EMAIL = "EMAIL"
    PDF = "PDF"
    DOCX = "DOCX"
    MARKDOWN = "MARKDOWN"