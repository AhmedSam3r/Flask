from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#will be used at validate_field to check user
from blog.models import User


class registrationForm(FlaskForm):                           
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email',
                            validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                            validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),Length(min=6),EqualTo('password')])
    submit = SubmitField('Sign up')
    
    #validate functions where we pass the field we want to validate to avoid errors

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
    

class loginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(),])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
