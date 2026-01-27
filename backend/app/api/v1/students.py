from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import date
import os
import shutil
from ...database import get_db
from ...models.student import Student
from ...models.class_model import Class
from ...models.user import User
from ...schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
)
from ...api.deps import get_current_user
from ...config import settings

router = APIRouter()


def generate_student_id(db: Session, admission_year: int) -> str:
    """
    Generate unique student ID in format: STU{YEAR}{NUMBER}
    Example: STU2024001, STU2024002, etc.
    """
    prefix = f"STU{admission_year}"
    
    # Get the last student ID for this year
    last_student = db.query(Student).filter(
        Student.student_id.like(f"{prefix}%")
    ).order_by(Student.student_id.desc()).first()
    
    if last_student:
        # Extract number and increment
        last_number = int(last_student.student_id.replace(prefix, ""))
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:03d}"


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new student.
    
    Required fields:
    - first_name, last_name, date_of_birth, gender
    - guardian_name, guardian_relationship, guardian_phone
    
    Optional:
    - class_id (assign to a class)
    - All other personal and contact details
    """
    # Check if class exists (if provided)
    if student_data.class_id:
        class_obj = db.query(Class).filter(Class.id == student_data.class_id).first()
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with id {student_data.class_id} not found"
            )
        
        # Check if class is full
        if class_obj.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Class {class_obj.name} is full (max: {class_obj.max_students})"
            )
    
    # Check if email already exists (if provided)
    if student_data.email:
        existing_student = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Generate student ID
    admission_year = student_data.admission_date.year if student_data.admission_date else date.today().year
    student_id = generate_student_id(db, admission_year)
    
    # Create student
    new_student = Student(
        student_id=student_id,
        **student_data.model_dump()
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


@router.get("/", response_model=StudentListResponse)
def get_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    class_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get paginated list of students with optional filters.
    
    Filters:
    - search: Search by name, student_id, or email
    - class_id: Filter by class
    - is_active: Filter by active status
    - gender: Filter by gender
    
    Pagination:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    """
    query = db.query(Student)
    
    # Apply filters
    if search:
        search_filter = or_(
            Student.first_name.ilike(f"%{search}%"),
            Student.last_name.ilike(f"%{search}%"),
            Student.student_id.ilike(f"%{search}%"),
            Student.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if class_id:
        query = query.filter(Student.class_id == class_id)
    
    if is_active is not None:
        query = query.filter(Student.is_active == is_active)
    
    if gender:
        query = query.filter(Student.gender == gender)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    skip = (page - 1) * page_size
    students = query.offset(skip).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "students": students
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific student by ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update student information.
    All fields are optional - only provided fields will be updated.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Check if new class exists (if changing class)
    if student_data.class_id and student_data.class_id != student.class_id:
        new_class = db.query(Class).filter(Class.id == student_data.class_id).first()
        if not new_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with id {student_data.class_id} not found"
            )
        if new_class.is_full:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Class {new_class.name} is full"
            )
    
    # Update fields
    update_data = student_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a student (soft delete - sets is_active to False).
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Soft delete
    student.is_active = False
    db.commit()
    
    return {"message": f"Student {student.student_id} deactivated successfully"}


@router.post("/{student_id}/upload-photo")
def upload_student_photo(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload student photo.
    Allowed formats: jpg, jpeg, png
    Max size: 5MB
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG and PNG images are allowed"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, "student_photos")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate filename
    file_extension = file.filename.split(".")[-1]
    filename = f"{student.student_id}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update student photo_url
    student.photo_url = f"/uploads/student_photos/{filename}"
    db.commit()
    
    return {
        "message": "Photo uploaded successfully",
        "photo_url": student.photo_url
    }