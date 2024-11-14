from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'customers'
    
    uid = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25))
    password = db.Column(db.String(100))
    
    def __repr__(self):
        return f'user {self.username} is registered'
    
    def get_id(self):
        return self.uid