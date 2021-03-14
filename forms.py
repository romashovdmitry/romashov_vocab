from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField, validators
from wtforms.validators import Email, Length, EqualTo, ValidationError
from models import users, whole_vocab


class register_form(FlaskForm):
    email = StringField('Email', [Email()])
    password = PasswordField('Password')  
    submit = SubmitField('To register')
    remember = BooleanField('Remember Me')
    
    def validate_email(self, email):
        email = users.query.filter_by(email=register_form().email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class login_form(FlaskForm):
    remember = BooleanField('Remember Me')
    email = StringField('Email', [Email()])
    password = PasswordField('Password')
    submit = SubmitField('To log in')

class word_and_definition(FlaskForm):
    word = StringField('Word', [Length(min=3)])
    definition = StringField('Definition')
    submit = SubmitField('To put new word')