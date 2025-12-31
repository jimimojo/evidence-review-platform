from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVISION = "revision"

class ReviewType(str, enum.Enum):
    SYSTEMATIC = "systematic"  # Full systematic review
    RAPID = "rapid"  # Rapid evidence synthesis
    SCOPING = "scoping"  # Scoping review
    EVIDENCE_BRIEF = "evidence_brief"  # Quick evidence brief
    CUSTOM = "custom"  # Custom review

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    review_type = Column(Enum(ReviewType), nullable=False)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    
    # Research question and methodology
    research_question = Column(Text)
    methodology = Column(Text)  # PRISMA, GRADE, CFIR, etc.
    
    # Client and reviewer relationships
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Pricing and payment
    price = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String, default="pending")
    stripe_payment_intent_id = Column(String, nullable=True)
    
    # Timeline
    deadline = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])
