from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date
import enum
from ..database import Base


class Gender(str, enum.Enum):
    """Gender options"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class BloodGroup(str, enum.Enum):
    """Blood group options"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class Student(Base):
    """
    Student model - core entity for student management.
    Contains personal info, enrollment details, and relationships.
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Student ID (unique identifier like "STU2024001")
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    blood_group = Column(Enum(BloodGroup), nullable=True)
    
    # Contact Information
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), default="Ghana")
    
    # Guardian Information
    guardian_name = Column(String(200), nullable=False)
    guardian_relationship = Column(String(50), nullable=False)  # Father, Mother, Guardian
    guardian_phone = Column(String(20), nullable=False)
    guardian_email = Column(String(255), nullable=True)
    guardian_address = Column(Text, nullable=True)
    
    # Emergency Contact (can be different from guardian)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)
    
    # Enrollment Information
    admission_date = Column(Date, nullable=False, default=date.today)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    roll_number = Column(String(20), nullable=True)  # Class roll number
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Photo
    photo_url = Column(String(500), nullable=True)
    
    # Medical Information
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    
    # Previous School
    previous_school = Column(String(200), nullable=True)
    previous_class = Column(String(50), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student_class = relationship("Class", back_populates="students", lazy="joined")
    
    def __repr__(self):
        return f"<Student {self.student_id}: {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self):
        """Get student's full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate student's age"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )