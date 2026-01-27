import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Register a user
def test_register():
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "teacher@school.com",
        "username": "teacher1",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "9876543210",
        "role": "teacher",
        "password": "TeacherPass123"
    })
    print("Register:", response.status_code)
    print(response.json())
    return response.json()

# 2. Login
def test_login(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={
        "username": username,
        "password": password
    })
    print("\nLogin:", response.status_code)
    data = response.json()
    print(f"Token: {data['access_token'][:50]}...")
    return data["access_token"]

# 3. Get current user
def test_me(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print("\nGet Me:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    # Register
    test_register()
    
    # Login
    token = test_login("teacher1", "TeacherPass123")
    
    # Get current user info
    test_me(token)