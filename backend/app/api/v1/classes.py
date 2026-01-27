from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.class_model import Class
from ...models.user import User, UserRole
from ...schemas.student import ClassCreate, ClassResponse
from ...api.deps import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Create a new class/grade.
    Only admins can create classes.
    
    Example:
    {
        "name": "Grade 1A",
        "grade_level": 1,
        "section": "A",
        "academic_year": "2024-2025",
        "max_students": 35,
        "room_number": "101"
    }
    """
    # Check if class name already exists for this academic year
    existing_class = db.query(Class).filter(
        Class.name == class_data.name,
        Class.academic_year == class_data.academic_year
    ).first()
    
    if existing_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Class '{class_data.name}' already exists for {class_data.academic_year}"
        )
    
    new_class = Class(**class_data.model_dump())
    
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    return new_class


@router.get("/", response_model=list[ClassResponse])
def get_classes(
    academic_year: str = None,
    grade_level: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all classes with optional filters.
    
    Filters:
    - academic_year: Filter by academic year (e.g., "2024-2025")
    - grade_level: Filter by grade level (1-12)
    """
    query = db.query(Class)
    
    if academic_year:
        query = query.filter(Class.academic_year == academic_year)
    
    if grade_level:
        query = query.filter(Class.grade_level == grade_level)
    
    classes = query.all()
    return classes


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific class by ID.
    """
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found"
        )
    
    return class_obj


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int,
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Update class information.
    Only admins can update classes.
    """
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found"
        )
    
    # Check if new name conflicts with existing class
    if class_data.name != class_obj.name:
        existing_class = db.query(Class).filter(
            Class.name == class_data.name,
            Class.academic_year == class_data.academic_year,
            Class.id != class_id
        ).first()
        
        if existing_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Class '{class_data.name}' already exists for {class_data.academic_year}"
            )
    
    # Update fields
    for field, value in class_data.model_dump().items():
        setattr(class_obj, field, value)
    
    db.commit()
    db.refresh(class_obj)
    
    return class_obj


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Delete a class.
    Only admins can delete classes.
    Note: Cannot delete class with enrolled students.
    """
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found"
        )
    
    # Check if class has students
    if class_obj.current_enrollment > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete class with {class_obj.current_enrollment} enrolled students"
        )
    
    db.delete(class_obj)
    db.commit()
    
    return {"message": f"Class {class_obj.name} deleted successfully"}