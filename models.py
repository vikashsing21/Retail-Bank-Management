from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from _datetime import datetime


class User(db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, index=True)
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    #login stores when the user succefully logged in
    login = db.Column(db.DateTime, nullable=True)
    # login = db.Column(db.DateTime, nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)

# Two roles 0-> Account Executive, 1-> Cashier

    
   
    def set_password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)



class Customer(db.Model):
    """
    Create a Customer table
    """

    __tablename__ = 'customers'

    cid = db.Column(db.Integer, primary_key=True)
    ssin_id=db.Column(db.Integer,index=True, unique=True)
    name = db.Column(db.String(60), unique=True)
    Age = db.Column(db.Integer)
    address_1 = db.Column(db.String(200))
    address_2 = db.Column(db.String(200))
