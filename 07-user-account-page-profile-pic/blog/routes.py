import os
from PIL import Image #we will use it to resize image-size (css)
import secrets
from flask import render_template, url_for, redirect,flash, request     #request: accessing query parameters in order to redirect user to the page they entered directly rather than to home page after login 
from blog import app, db, bcrypt
from blog.forms  import registrationForm, loginForm,  updateAccountForm
from blog.models import User, Post
#an extension make it easy to handle users' sessions 
from flask_login import login_user, current_user, logout_user, login_required

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
#we imported current user above as we want to avoid if user logged in 
# and retuned back to this page to be opened as if he didn't submit it
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = registrationForm()
    if form.validate_on_submit():
        #we want to hash our password to avoid vulnerability 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        #a flash msg an easy way to send one time alert
        flash('Account is created you can log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods={'GET','POST'})
def login():
    #we imported current user above as we want to avoid if user logged in 
    # and retuned back to this page to be opened as if he didn't submit it
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    

    
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #user.password as it's from db query not from the form itself like user.password.data
        #if condition is true we want to log user in 
        #need to import login user function
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            #args is a dictionnary but we're using get() instead of []
            # next parameter which is in the URL (eg.next=%2Faccount) it tells us where the user was heading to
            next_page = request.args.get('next')
            #a ternary conditon directs us to the next page if it exists else returns us to the home
            return redirect(next_page) if next_page else redirect(url_for('home'))
 

        else:
            flash('Login Unsucessful. Please check username and password','danger')

    return render_template('login.html',title='Login',form=form)

def save_picture(form_picture):
    #we randomize picture's name to avoid getting mixed up with any profile picture we have on our server
    random_hex = secrets.token_hex(8)
    #we don't need filename variable return  so we will use underscore _ to tell python it's useless var
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_fileName = random_hex + file_extension
    #31:58 You would probably want to use "os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)"instead of 
    #"os.path.join(app.root_path, 'static/profile_pics', picture_fn)"because that's what we actually use os.path.join for.
    #didn't work picture_path = os.path.join(app.root_path,'static/profile_pics','picture_fileName')
    picture_path= os.path.join(app.root_path, 'static/profile_pics', picture_fileName)
    
    #resizing image size --> speed up our app && save space on our server
    output_size=(125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    #save picture into our file system but not to the database yet
    img.save(picture_path)
    return picture_fileName





@app.route('/account',methods={'GET','POST'})
#it allows this route to logged in users only ,we  need to tell the extension where login is located at the __init__ file
@login_required
def account():
    form = updateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_profile = save_picture(form.picture.data)
            current_user.image_file = picture_profile


        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Info has been update successfully",'successs')
        #we redirect here instead of waiting to redirect downwards 
        #because of post-get redirect pattern
        #sometimes when we reload browser after submitting a form , a strange msg appears "are you sure you want to reload data will be resubmited"
        #browser is telling us we about to reload another post request when reloading so we avoid this situation 
        return redirect(url_for('account'))

    #in case user didn't enter any data we will display their data next to username and email fields
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

