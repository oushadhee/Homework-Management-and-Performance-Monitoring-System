"""Lesson models for storing lesson content and extracted keywords"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base


class Lesson(Base):
    """Lesson model for storing lesson content"""
    
    __tablename__ = "lessons"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Lesson Information
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)  # Main lesson content
    
    # Extracted Information (from NLP processing)
    topics = Column(JSON, nullable=True)  # List of main topics
    key_concepts = Column(JSON, nullable=True)  # List of key concepts
    difficulty_level = Column(String(20), nullable=True)  # beginner, intermediate, advanced
    
    # Metadata
    grade_level = Column(String(20), nullable=True)
    chapter = Column(String(100), nullable=True)
    lesson_number = Column(Integer, nullable=True)
    
    # Processing Status
    is_processed = Column(Integer, default=0, nullable=False)  # 0: pending, 1: processing, 2: completed, 3: failed
    processing_error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # subject = relationship("Subject", back_populates="lessons")
    # teacher = relationship("User", back_populates="lessons", foreign_keys=[teacher_id])
    # keywords = relationship("LessonKeyword", back_populates="lesson", cascade="all, delete-orphan")
    # questions = relationship("Question", back_populates="lesson", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', subject_id={self.subject_id})>"


class LessonKeyword(Base):
    """Keywords extracted from lessons"""
    
    __tablename__ = "lesson_keywords"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Keyword Information
    keyword = Column(String(100), nullable=False, index=True)
    importance_score = Column(Integer, nullable=True)  # 0.0 to 1.0
    category = Column(String(50), nullable=True)  # concept, term, topic, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # lesson = relationship("Lesson", back_populates="keywords")
    
    def __repr__(self):
        return f"<LessonKeyword(id={self.id}, keyword='{self.keyword}', lesson_id={self.lesson_id})>"

