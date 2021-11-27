from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

class loginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(),])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
