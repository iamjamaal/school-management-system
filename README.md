# School Management System

A comprehensive school management system built with FastAPI, PostgreSQL, and SQLAlchemy. This system helps manage students, classes, teachers, and administrative tasks efficiently.

## Features

### Current Features ✅
- **User Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin, Teacher, Parent, Student)
  - Secure password hashing with bcrypt
  
- **Student Management**
  - Complete student profiles with personal and contact information
  - Guardian and emergency contact management
  - Medical information tracking
  - Photo upload support
  - Automatic student ID generation
  - Search and filtering capabilities
  - Pagination for large datasets
  
- **Class Management**
  - Create and manage classes/grades
  - Track class capacity and enrollment
  - Academic year management
  - Room assignment

### Planned Features 🚧
- Attendance tracking system
- Grading and assessment module
- Course/Subject management
- Teacher-class assignments
- Reporting and analytics
- Email notifications
- Data export (PDF/Excel)

## Tech Stack

- **Backend Framework:** FastAPI 0.115.0
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT (python-jose)
- **Validation:** Pydantic v2
- **Migrations:** Alembic
- **Testing:** Pytest

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd school-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a PostgreSQL database:
```sql
CREATE DATABASE school_db;
```

### 5. Environment Configuration

Create a `.env` file in the root directory (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/school_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**Generate a secure SECRET_KEY:**
```bash
python generate_key.py
```

### 6. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:
```bash
python -m app.main
```

The API will be available at:
- API: http://localhost:8000
- Interactive API Docs (Swagger): http://localhost:8000/docs
- Alternative API Docs (ReDoc): http://localhost:8000/redoc

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "teacher",
  "phone": "1234567890"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer {access_token}
```

### Student Endpoints

#### Create Student
```http
POST /api/v1/students/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "date_of_birth": "2010-05-15",
  "gender": "female",
  "guardian_name": "John Smith",
  "guardian_relationship": "Father",
  "guardian_phone": "9876543210",
  "class_id": 1
}
```

#### List Students
```http
GET /api/v1/students/?page=1&page_size=20&search=jane
Authorization: Bearer {access_token}
```

#### Get Student Details
```http
GET /api/v1/students/{student_id}
Authorization: Bearer {access_token}
```

#### Update Student
```http
PUT /api/v1/students/{student_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "phone": "1234567890",
  "email": "jane.smith@example.com"
}
```

### Class Endpoints

#### Create Class (Admin Only)
```http
POST /api/v1/classes/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Grade 1A",
  "grade_level": 1,
  "section": "A",
  "academic_year": "2024-2025",
  "max_students": 35,
  "room_number": "101"
}
```

#### List Classes
```http
GET /api/v1/classes/?academic_year=2024-2025
Authorization: Bearer {access_token}
```

## Database Migrations

### Create a New Migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Project Structure

```
school-management-system/
├── backend/
│   ├── alembic/              # Database migrations
│   │   ├── versions/         # Migration files
│   │   └── env.py            # Alembic environment
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   ├── deps.py       # Dependencies
│   │   │   └── v1/           # API version 1
│   │   │       ├── auth.py   # Authentication endpoints
│   │   │       ├── students.py
│   │   │       └── classes.py
│   │   ├── core/             # Core functionality
│   │   │   └── security.py   # Security utilities
│   │   ├── models/           # Database models
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   └── class_model.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── user.py
│   │   │   └── student.py
│   │   ├── utils/            # Utilities
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database setup
│   │   └── main.py           # Application entry
│   ├── tests/                # Tests
│   ├── uploads/              # Uploaded files
│   └── alembic.ini           # Alembic config
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Security Considerations

⚠️ **IMPORTANT:**
- Never commit `.env` file to version control
- Change the default SECRET_KEY in production
- Use strong passwords for database
- Keep dependencies updated
- Use HTTPS in production
- Implement rate limiting for production

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused

### Git Workflow
1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists
- Verify username/password

### Migration Issues
```bash
# Reset migrations (development only)
alembic downgrade base
alembic upgrade head
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Support

For issues and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]

## Changelog

### Version 1.0.0 (In Development)
- Initial project setup
- User authentication system
- Student management module
- Class management module
- Database migrations with Alembic
- API documentation
