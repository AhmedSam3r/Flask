from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello_world():
    return '<h1>Hello world !</h1>'

@app.route('/about')
def info():
    return '<h1>We\'re Navigation company</h1>'

@app.route('/about/<username>')
def info_username(username):
    return f'<h1>Welcome {username} </h1>'      #formatted string

