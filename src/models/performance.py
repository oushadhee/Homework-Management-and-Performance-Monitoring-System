"""Performance tracking and reporting models"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base


class PerformanceMetric(Base):
    """Student performance metrics tracking"""
    
    __tablename__ = "performance_metrics"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Time Period
    period_start = Column(Date, nullable=False, index=True)
    period_end = Column(Date, nullable=False, index=True)
    period_type = Column(String(20), nullable=False)  # weekly, monthly, quarterly, yearly
    
    # Performance Metrics
    total_homeworks = Column(Integer, default=0, nullable=False)
    completed_homeworks = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, nullable=True)
    highest_score = Column(Float, nullable=True)
    lowest_score = Column(Float, nullable=True)
    
    # Completion Metrics
    on_time_submissions = Column(Integer, default=0, nullable=False)
    late_submissions = Column(Integer, default=0, nullable=False)
    missing_submissions = Column(Integer, default=0, nullable=False)
    
    # Performance Trends
    improvement_rate = Column(Float, nullable=True)  # Percentage improvement
    consistency_score = Column(Float, nullable=True)  # 0-100
    
    # Detailed Analytics
    topic_performance = Column(JSON, nullable=True)  # Performance by topic
    question_type_performance = Column(JSON, nullable=True)  # Performance by question type
    difficulty_performance = Column(JSON, nullable=True)  # Performance by difficulty
    
    # Weak Areas
    weak_topics = Column(JSON, nullable=True)  # List of topics needing improvement
    strong_topics = Column(JSON, nullable=True)  # List of strong topics
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    # student = relationship("User", back_populates="performance_metrics")
    # subject = relationship("Subject")
    
    def __repr__(self):
        return f"<PerformanceMetric(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id})>"


class MonthlyReport(Base):
    """Monthly performance reports"""
    
    __tablename__ = "monthly_reports"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Report Period
    report_month = Column(Integer, nullable=False)  # 1-12
    report_year = Column(Integer, nullable=False)
    
    # Overall Performance
    overall_average = Column(Float, nullable=True)
    total_homeworks_completed = Column(Integer, default=0, nullable=False)
    total_homeworks_assigned = Column(Integer, default=0, nullable=False)
    completion_rate = Column(Float, nullable=True)
    
    # Subject-wise Performance
    subject_performance = Column(JSON, nullable=True)  # Performance breakdown by subject
    
    # Trends
    performance_trend = Column(String(20), nullable=True)  # improving, declining, stable
    attendance_rate = Column(Float, nullable=True)
    
    # Insights & Recommendations
    strengths = Column(JSON, nullable=True)  # List of strengths
    areas_for_improvement = Column(JSON, nullable=True)  # List of areas needing work
    recommendations = Column(JSON, nullable=True)  # Personalized recommendations
    
    # AI-Generated Summary
    ai_summary = Column(Text, nullable=True)
    teacher_comments = Column(Text, nullable=True)
    
    # Report Status
    is_generated = Column(Integer, default=0, nullable=False)  # Boolean
    is_sent_to_parent = Column(Integer, default=0, nullable=False)  # Boolean
    is_sent_to_teacher = Column(Integer, default=0, nullable=False)  # Boolean
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # student = relationship("User")
    
    def __repr__(self):
        return f"<MonthlyReport(id={self.id}, student_id={self.student_id}, month={self.report_month}/{self.report_year})>"

