from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, validators, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
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


class updateAccountForm(FlaskForm):                           
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email',
                            validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','jpg','png'])])
    submit = SubmitField('Update Account\'s info')
    

    def validate_username(self,username):
        if username.data != current_user.username:    
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')

    def validate_email(self,email):
        if email.data != current_user.email:    
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')



class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')