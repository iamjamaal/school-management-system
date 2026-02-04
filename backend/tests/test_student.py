import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
def login():
    response = requests.post(f"{BASE_URL}/auth/login", data={
        "username": "admin",
        "password": "Admin123456"
    })
    try:
        return response.json()["access_token"]
    except KeyError:
        print("Login failed:", response.status_code, response.text)
        raise

# 2. Create class
def create_class(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/classes/", 
        json={
            "name": "Test Class",
            "grade_level": 3,
            "section": "A",
            "academic_year": "2024-2025",
            "max_students": 30
        },
        headers=headers
    )
    print("Create Class:", response.status_code)
    try:
        return response.json()["id"]
    except KeyError:
        print("Create class failed:", response.status_code, response.text)
        raise

# 3. Create student
def create_student(token, class_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/students/",
        json={
            "first_name": "Test",
            "last_name": "Student",
            "date_of_birth": "2015-05-15",
            "gender": "male",
            "guardian_name": "Test Guardian",
            "guardian_relationship": "Father",
            "guardian_phone": "0244000000",
            "class_id": class_id
        },
        headers=headers
    )
    print("Create Student:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json()["id"]

# 4. Get all students
def get_students(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/students/", headers=headers)
    print("\nAll Students:", response.status_code)
    data = response.json()
    print(f"Total: {data['total']}, Page: {data['page']}")
    for student in data['students']:
        print(f"  - {student['student_id']}: {student['full_name']}")

# 5. Search students
def search_students(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/students/?search={query}", 
        headers=headers
    )
    print(f"\nSearch '{query}':", response.status_code)
    data = response.json()
    print(f"Found: {data['total']} students")

if __name__ == "__main__":
    token = login()
    print("✓ Logged in")
    
    class_id = create_class(token)
    print(f"✓ Created class (id: {class_id})")
    
    student_id = create_student(token, class_id)
    print(f"✓ Created student (id: {student_id})")
    
    get_students(token)
    search_students(token, "Test")