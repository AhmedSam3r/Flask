from flask import Flask, render_template, url_for, redirect,flash 
from forms  import registrationForm, loginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '2ee1ab3b023f02962acf192762d3fd0c' #Go to Cmd write Python Enter, Write import secrets, Write secrets.token_hex(16)
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
