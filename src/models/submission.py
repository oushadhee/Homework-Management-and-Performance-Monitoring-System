"""Submission models for student homework submissions"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..config.database import Base


class SubmissionStatus(str, enum.Enum):
    """Submission status enumeration"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    RETURNED = "returned"


class Submission(Base):
    """Student homework submission model"""
    
    __tablename__ = "submissions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    homework_id = Column(Integer, ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Submission Information
    status = Column(SQLEnum(SubmissionStatus), default=SubmissionStatus.DRAFT, nullable=False, index=True)
    
    # Scoring
    total_score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=True)
    
    # Grading Information
    auto_graded_score = Column(Float, nullable=True)
    manual_graded_score = Column(Float, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Feedback
    teacher_feedback = Column(Text, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    
    # Timing
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    is_late = Column(Integer, default=0, nullable=False)  # Boolean: 0 or 1
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # homework = relationship("Homework", back_populates="submissions")
    # student = relationship("User", back_populates="submissions", foreign_keys=[student_id])
    # grader = relationship("User", foreign_keys=[graded_by])
    # answers = relationship("SubmissionAnswer", back_populates="submission", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Submission(id={self.id}, homework_id={self.homework_id}, student_id={self.student_id})>"


class SubmissionAnswer(Base):
    """Individual answers in a submission"""
    
    __tablename__ = "submission_answers"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Answer Information
    answer_text = Column(Text, nullable=True)
    selected_option = Column(String(1), nullable=True)  # For MCQ: A, B, C, D
    
    # Grading
    is_correct = Column(Integer, nullable=True)  # Boolean: 0 or 1, null if not graded
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=False)
    
    # AI Evaluation
    similarity_score = Column(Float, nullable=True)  # For subjective answers
    ai_evaluation = Column(Text, nullable=True)
    
    # Manual Review
    manual_score = Column(Float, nullable=True)
    manual_feedback = Column(Text, nullable=True)
    requires_manual_review = Column(Integer, default=0, nullable=False)  # Boolean
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # submission = relationship("Submission", back_populates="answers")
    # question = relationship("Question")
    
    def __repr__(self):
        return f"<SubmissionAnswer(id={self.id}, submission_id={self.submission_id}, question_id={self.question_id})>"

