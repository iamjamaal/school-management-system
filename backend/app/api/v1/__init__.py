# This file makes it easier to import routers in main.py
from . import auth, students, classes

__all__ = ["auth", "students", "classes"]