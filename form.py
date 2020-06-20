from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField,validators,TextAreaField,SelectField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):  

    username = StringField('Username', validators=[DataRequired(),validators.Regexp(regex='^[a-zA-Z][a-zA-Z0-9]+$', message="Field must start with a alphabet and no special characters allowed."),validators.Length(min=5, max=25)],render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[DataRequired(),validators.Regexp(regex='((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\$%\^\&*\)\(\]\[\\+=._\-]))',message='Field must contain at least one lowercase,uppercase,digit and special character.'),validators.length(min=8)],render_kw={"placeholder": "Password"})
    role = SelectField(u'Roles',[DataRequired()], choices=[('','Select Role'),('0', 'Account Executive'), ('1', 'Cashier')],default='')
class LoginForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()],render_kw={"placeholder": "Username"})
    password=PasswordField("Password:",validators=[DataRequired()],render_kw={"placeholder": "Password"})

class CreateCustomerForm(FlaskForm):
    ssnid = IntegerField('Customer SSN Id',validators=[DataRequired(),validators.Length(9)])
    customername = StringField('Customer Name', [validators.Regexp(regex='^[a-zA-Z]+$', message="Username must contains alphabets")])
    age = IntegerField('Age',validators=[DataRequired(),validators.Length(3)])
    address = TextAreaField('Address',validators=[DataRequired()])
