"""Homework models for managing homework assignments"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base


class Homework(Base):
    """Homework assignment model"""
    
    __tablename__ = "homeworks"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Homework Information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    
    # Scheduling
    assigned_date = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    
    # Configuration
    total_points = Column(Float, default=100.0, nullable=False)
    passing_score = Column(Float, default=60.0, nullable=False)
    allow_late_submission = Column(Boolean, default=False, nullable=False)
    
    # Target Audience
    grade_level = Column(String(20), nullable=True)
    class_section = Column(String(50), nullable=True)
    
    # Status
    is_published = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Statistics
    total_submissions = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # subject = relationship("Subject", back_populates="homeworks")
    # teacher = relationship("User", foreign_keys=[teacher_id])
    # lesson = relationship("Lesson")
    # homework_questions = relationship("HomeworkQuestion", back_populates="homework", cascade="all, delete-orphan")
    # submissions = relationship("Submission", back_populates="homework", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Homework(id={self.id}, title='{self.title}', subject_id={self.subject_id})>"


class HomeworkQuestion(Base):
    """Junction table linking homework to questions"""
    
    __tablename__ = "homework_questions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    homework_id = Column(Integer, ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Question Configuration
    question_order = Column(Integer, nullable=False)  # Order in homework
    points = Column(Float, nullable=False)  # Points for this question in this homework
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # homework = relationship("Homework", back_populates="homework_questions")
    # question = relationship("Question")
    
    def __repr__(self):
        return f"<HomeworkQuestion(homework_id={self.homework_id}, question_id={self.question_id})>"

