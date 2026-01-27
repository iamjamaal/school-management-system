from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from ..models.student import Gender, BloodGroup


# Class schemas
class ClassBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    grade_level: int = Field(..., ge=1, le=12)
    section: Optional[str] = None
    academic_year: str
    max_students: int = Field(default=40, ge=1)
    description: Optional[str] = None
    room_number: Optional[str] = None


class ClassCreate(ClassBase):
    pass


class ClassResponse(ClassBase):
    id: int
    current_enrollment: int
    is_full: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Student schemas
class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = None
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    
    # Contact
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Ghana"
    
    # Guardian
    guardian_name: str = Field(..., min_length=1)
    guardian_relationship: str
    guardian_phone: str
    guardian_email: Optional[EmailStr] = None
    guardian_address: Optional[str] = None
    
    # Emergency
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    
    # Medical
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    
    # Previous school
    previous_school: Optional[str] = None
    previous_class: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None


class StudentCreate(StudentBase):
    class_id: Optional[int] = None
    admission_date: Optional[date] = None


class StudentUpdate(BaseModel):
    """All fields optional for partial updates"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    class_id: Optional[int] = None
    roll_number: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    student_id: str
    admission_date: date
    class_id: Optional[int] = None
    roll_number: Optional[str] = None
    is_active: bool
    photo_url: Optional[str] = None
    full_name: str
    age: int
    created_at: datetime
    student_class: Optional[ClassResponse] = None
    
    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """Response for paginated student list"""
    total: int
    page: int
    page_size: int
    students: list[StudentResponse]