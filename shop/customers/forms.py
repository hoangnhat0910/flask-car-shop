from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, Form, ValidationError
from flask_wtf.file import FileAllowed, FileRequired, FileField
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), 
                                            validators.EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Repeat password: ', [validators.DataRequired()])

    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zipcode: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please.')]) 
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username = username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email = email.data).first():
            raise ValidationError("This email address is already in use!")
        
class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])