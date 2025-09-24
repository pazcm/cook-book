from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        
    def get_id(self):
        return str(self.user_data['_id'])
        
    @property
    def is_authenticated(self):
        return True
        
    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)