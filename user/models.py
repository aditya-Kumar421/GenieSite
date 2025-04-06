from pymongo import MongoClient
from django.conf import settings
import bcrypt
from datetime import datetime
from bson import ObjectId

class UserManager:
    def __init__(self):
        client = MongoClient(settings.MONGO_URI)
        self.db = client[settings.MONGO_DB_NAME]
        self.users = self.db.users

    def create_user(self, username, email, password):
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        user = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now()
        }
        result = self.users.insert_one(user)
        return str(result.inserted_id)

    def find_user_by_email(self, email):
        return self.users.find_one({'email': email})
    
    def find_user_by_id(self, user_id):
        return self.users.find_one({'_id': ObjectId(user_id)})
