from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Class(Base):
    """
    Class/Grade model - represents different classes in the school.
    Examples: "Grade 1A", "Grade 2B", "Form 3", etc.
    """
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    grade_level = Column(Integer, nullable=False)  # 1-12 for primary/secondary
    section = Column(String(10), nullable=True)  # A, B, C, etc.
    
    # Academic year
    academic_year = Column(String(20), nullable=False)  # e.g., "2024-2025"
    
    # Capacity
    max_students = Column(Integer, default=40)
    
    # Additional info
    description = Column(Text, nullable=True)
    room_number = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="student_class")
    
    def __repr__(self):
        return f"<Class {self.name} - {self.academic_year}>"
    
    @property
    def current_enrollment(self):
        """Get current number of enrolled students"""
        return len(self.students) if self.students else 0
    
    @property
    def is_full(self):
        """Check if class is at capacity"""
        return self.current_enrollment >= self.max_students