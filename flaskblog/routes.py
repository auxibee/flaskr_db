from flaskblog.models import User, Post
from flaskblog import app
from flask import  render_template, url_for, flash, redirect
from flaskblog.forms import LoginForm, RegistrationForm

posts = [
    {
        'author': 'yaw twumasi',
        'title' : 'this is good',
        'content': 'we start by making fight',
        'date_posted': 'April-2021'
    },
    {
        'author': 'jane doe',
        'title' : 'this is crasy',
        'content': 'we start by making fight',
        'date_posted': 'April-2021'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts, title='learning flask')

@app.route('/about')
def about_us():

    return render_template('about.html')

@app.route('/register',methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data} !', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title = 'Register')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'auxibee@gmail.com' and form.password.data == '123456':
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful please check username and password', 'danger')
    return render_template('login.html', form=form, title = 'Login')