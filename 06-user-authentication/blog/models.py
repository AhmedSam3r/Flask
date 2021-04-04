from datetime import datetime
from blog import db, login_manager  
#It contains is_authenticated
from flask_login import UserMixin

'''this part affects blog.routes module in login part
where it takes user_id from login_user(user,remember=form.remember.data)
so that user_id is stored through the session 
as if user went for register or login route it redirect them to the home page '''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpeg')  
    password=db.Column(db.String(60),nullable=False)
    #backref author is to get the user who made the post
    #lazy argument just defines when SQL alchemy loads the data from DB ,true means it will load the data as necessacy in one go
    #it's a relationship not a column,running an addition query in the background
    #when running on cmd >>> post.author
    #User('Ahmed','ah@gmail.com','default.jpeg')
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    #user is lowercase as we refer to the user tablename and  id column name
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"