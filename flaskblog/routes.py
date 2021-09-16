from flask_login.utils import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask import  render_template, url_for, flash, redirect
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import load_user

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} ! you can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title = 'Register')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data).first()
        if user  and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful please check email and password', 'danger')
    return render_template('login.html', form=form, title = 'Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title = 'Account details')


