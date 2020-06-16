from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField,validators,TextAreaField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):  

    username = StringField('Username', validators=[DataRequired(),validators.Regexp(regex='^[a-zA-Z][a-zA-Z0-9]+$', message="Username must start with alphabets"),validators.Length(min=5, max=25)])
    password = PasswordField('password', validators=[DataRequired(),validators.Regexp(regex='((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%?=*&]).{8,20})',message='password must contain At least one lowercase,uppercase,digit,special character,8 characters long.')])

class LoginForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])

class CreateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN Id',validators=[DataRequired(),validators.Length(9)])
    customername = StringField('Customer Name', [validators.Regexp(regex='^[a-zA-Z]+$', message="Username must contains alphabets")])
    age = IntegerField('Age',validators=[DataRequired(),validators.Length(3)])
    address = TextAreaField('Address',validators=[DataRequired()])
