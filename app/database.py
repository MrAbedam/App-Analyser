# project/app/database.py

from typing import List
from .models import Application

# In-memory database
db: List[Application] = []

def init_db():
    """Initialize the in-memory database with sample data."""
    global db
    db = []
    db.append(Application(id=1, name="App1", description="Description for App1"))
    db.append(Application(id=2, name="App2", description="Description for App2"))
    db.append(Application(id=3, name="App3", description="Description for App3"))

def reset_db():
    """Reset the in-memory database."""
    global db
    db = []