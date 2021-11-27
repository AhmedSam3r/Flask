from flask import render_template, url_for, redirect,flash, request     #request: accessing query parameters in order to redirect user to the page they entered directly rather than to home page after login 
from blog import app, db, bcrypt
from blog.forms  import registrationForm, loginForm
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

@app.route('/account')
#it allows this route to logged in users only ,we  need to tell the extension where login is located at the __init__ file
@login_required
def account():
    return render_template('account.html',title='Account')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

