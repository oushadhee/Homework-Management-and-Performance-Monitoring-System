"""Subject model for managing different academic subjects"""

from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base


class Subject(Base):
    """Subject model for academic subjects"""
    
    __tablename__ = "subjects"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Subject Information
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Configuration
    grade_level = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    icon = Column(String(50), nullable=True)  # Icon identifier for UI
    color = Column(String(20), nullable=True)  # Color code for UI
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # lessons = relationship("Lesson", back_populates="subject", cascade="all, delete-orphan")
    # homeworks = relationship("Homework", back_populates="subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', code='{self.code}')>"

