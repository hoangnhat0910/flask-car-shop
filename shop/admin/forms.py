from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

class RegistrationForm(Form):
    #them name = ...
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    # add validators.email vao cuoi dong
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # dell => accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])

class LoginForm(Form):
    username = username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])

