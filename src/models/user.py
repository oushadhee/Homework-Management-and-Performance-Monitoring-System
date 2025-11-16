"""User model for authentication and authorization"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from ..config.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class User(Base):
    """User model for all system users"""
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    
    # Role & Status
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Additional Information
    phone_number = Column(String(20), nullable=True)
    grade_level = Column(String(20), nullable=True)  # For students
    employee_id = Column(String(50), nullable=True)  # For teachers/admin
    
    # Relationships
    parent_id = Column(Integer, nullable=True)  # For linking parent to student
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # lessons = relationship("Lesson", back_populates="teacher", foreign_keys="Lesson.teacher_id")
    # submissions = relationship("Submission", back_populates="student", foreign_keys="Submission.student_id")
    # performance_metrics = relationship("PerformanceMetric", back_populates="student")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def is_teacher(self) -> bool:
        """Check if user is a teacher"""
        return self.role == UserRole.TEACHER
    
    @property
    def is_student(self) -> bool:
        """Check if user is a student"""
        return self.role == UserRole.STUDENT
    
    @property
    def is_parent(self) -> bool:
        """Check if user is a parent"""
        return self.role == UserRole.PARENT
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN

