from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self._id = user_data['_id']
        self.email = user_data['email']
        self.password = user_data['password']
    
    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
        
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self._id)