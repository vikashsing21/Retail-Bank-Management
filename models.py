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
    login = db.Column(db.TIMESTAMP, nullable=True)



    
   
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
    accounts=db.relationship('Account', backref='customers', lazy='dynamic',cascade='all, delete-orphan')
    cusotmer_status=db.relationship('CustomerStatus', backref='customers', uselist=False)
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.TIMESTAMP, nullable=False,default=datetime.now(),onupdate=datetime.now())

class Account(db.Model):
    """
    Create a Account table
    """

    __tablename__ = 'accounts'
    
    accntid=db.Column(db.Integer,primary_key=True)
    customer_cid = db.Column(db.Integer, db.ForeignKey('customers.cid',ondelete='CASCADE'))
    accnt_type = db.Column(db.String(30),nullable=False)
    ammount=db.Column(db.Integer,nullable=False)
    account_status=db.relationship('AccountStatus', backref='accounts', uselist=False)
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.TIMESTAMP, nullable=False,default=datetime.now(),onupdate=datetime.now())

class CustomerStatus(db.Model):
    """
    Create a Cusotmer Status table
    """

    __tablename__ = 'cusotmer_status'
    
    id=db.Column(db.Integer,primary_key=True)
    customer_cid = db.Column(db.Integer, db.ForeignKey('customers.cid'))
    customer_ssnid = db.Column(db.Integer)
    status=db.Column(db.String(30))
    message=db.Column(db.String(100))
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.TIMESTAMP, nullable=False,default=datetime.now(),onupdate=datetime.now())
    
class AccountStatus(db.Model):
    """
    Create a Account Status table
    """

    __tablename__ = 'account_status'
    
    id=db.Column(db.Integer,primary_key=True)
    customer_cid = db.Column(db.Integer)
    account_id = db.Column(db.Integer,db.ForeignKey('accounts.accntid'))
    accnt_type = db.Column(db.String(30))
    status=db.Column(db.String(30))
    message=db.Column(db.String(100))
    created_on = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_on= db.Column(db.TIMESTAMP, nullable=False,default=datetime.now(),onupdate=datetime.now())
    
