from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from _datetime import datetime
from sqlalchemy import event
from sqlalchemy import DDL



class User(db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Two roles 0-> Account Executive, 1-> Cashier
    role_id = db.Column(db.Integer, index=True)
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    #login stores when the user succefully logged in
    login = db.Column(db.DateTime, nullable=True)



    
   
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
    ssnid=db.Column(db.Integer,index=True, unique=True)
    name = db.Column(db.String(60),nullable=False )
    age = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(300),nullable=False)
    state=db.Column(db.String(60),nullable=False)
    city=db.Column(db.String(60),nullable=False)
    accounts=db.relationship('Account', backref='customer', lazy='dynamic')
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.DateTime, nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)

class Account(db.Model):
    """
    Create a Account table
    """

    __tablename__ = 'accounts'
    
    accntid=db.Column(db.Integer,primary_key=True)
    customer_cid = db.Column(db.Integer, db.ForeignKey('customers.cid'))
    accnt_type = db.Column(db.String(30),nullable=False)
    ammount=db.Column(db.Integer,nullable=False)
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.DateTime, nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)
    
