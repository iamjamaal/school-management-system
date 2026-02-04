
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.core.security import get_password_hash
from backend.app.database import SessionLocal
from backend.app.models.user import User


# Set your new password here
NEW_PASSWORD = "Admin123456"

db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()
if admin:
    admin.hashed_password = get_password_hash(NEW_PASSWORD)
    db.commit()
    print("Admin password reset successfully.")
else:
    print("Admin user not found.")
db.close()