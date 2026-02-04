# Run this once to create the admin user
import requests

BASE_URL = "http://localhost:8000/api/v1"
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "admin@school.com",
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "phone": "1234567890",
    "role": "admin",
    "password": "Admin123456"
})
print(response.status_code)
print(response.json())