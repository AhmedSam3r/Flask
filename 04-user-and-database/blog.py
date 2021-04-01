from datetime import datetime
from flask import Flask, render_template, url_for, redirect,flash 
from flask_sqlalchemy import SQLAlchemy
from forms  import registrationForm, loginForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Python39/flaskCodes/04-user-database/site.db'
app.config['SECRET_KEY'] = '2ee1ab3b023f02962acf192762d3fd0c' #Go to Cmd write Python Enter, Write import secrets, Write secrets.token_hex(16)
db = SQLAlchemy(app)

class User(db.Model):
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





posts = [
    {
        'author': 'Ahmed Samer',
        'title': 'Indoor Positiong System',
        'content': 'The importance of IPS',
        'date_posted': 'March 28, 2020'
    },
    {
        'author': 'Mohamed fathy',
        'title': 'Wedding Ceremony',
        'content': 'The importance of getting married',
        'date_posted': 'March 30, 2020'
    }
]



@app.route('/') 
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        #a flash msg an easy way to send one time alert
        flash(f'Account Created, Welcome {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods={'GET','POST'})
def login():
    form = loginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("Logged Successfully")
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessfuly please check username and password','danger')

    return render_template('login.html',title='Login',form=form)



if __name__ == '__main__':
    app.run(debug=True)
