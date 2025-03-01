# this file is for initializing the database

from flasktracker import create_app, db

app = create_app()

app.app_context().push()
from backend.flasktracker.models import User

db.create_all()

# creating users with secure passwords
user1 = User(name="LeBron James", email="lebron@gmail.com")
user1.set_password("lebron")

user2 = User(name="Joe Biden", email="joebiden@gmail.com")
user2.set_password("joebiden")

# adding to database
try:
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("users added successfully")
except Exception as e:
    db.session.rollback()
    print(f"Error: {e}")

# verify users
users = User.query.all()
for user in users:
    print(user.name, user.email)
