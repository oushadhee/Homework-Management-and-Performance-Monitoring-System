"""Question models for storing generated questions"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..config.database import Base


class QuestionType(str, enum.Enum):
    """Question type enumeration"""
    MCQ = "mcq"  # Multiple Choice Question
    SHORT_ANSWER = "short_answer"
    DESCRIPTIVE = "descriptive"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"


class Question(Base):
    """Question model for storing generated questions"""
    
    __tablename__ = "questions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Question Information
    question_type = Column(SQLEnum(QuestionType), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    
    # Answer Information
    correct_answer = Column(Text, nullable=False)  # For MCQ: option letter; For others: text answer
    explanation = Column(Text, nullable=True)  # Explanation of the correct answer
    
    # Metadata
    difficulty_level = Column(String(20), nullable=True)  # easy, medium, hard
    bloom_taxonomy_level = Column(String(50), nullable=True)  # remember, understand, apply, analyze, evaluate, create
    keywords = Column(JSON, nullable=True)  # Related keywords from lesson
    
    # Scoring
    max_points = Column(Float, default=1.0, nullable=False)
    
    # Usage Statistics
    times_used = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # lesson = relationship("Lesson", back_populates="questions")
    # subject = relationship("Subject")
    # mcq_options = relationship("MCQOption", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question(id={self.id}, type='{self.question_type}', lesson_id={self.lesson_id})>"


class MCQOption(Base):
    """MCQ options for multiple choice questions"""
    
    __tablename__ = "mcq_options"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Option Information
    option_letter = Column(String(1), nullable=False)  # A, B, C, D
    option_text = Column(Text, nullable=False)
    is_correct = Column(Integer, default=0, nullable=False)  # Boolean: 0 or 1
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # question = relationship("Question", back_populates="mcq_options")
    
    def __repr__(self):
        return f"<MCQOption(id={self.id}, option='{self.option_letter}', question_id={self.question_id})>"

