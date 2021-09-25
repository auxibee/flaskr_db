from flask import Blueprint,request, abort, render_template, url_for, flash, redirect
from flask_login.utils import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import delete_profile_picture, save_picture, send_reset_email
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt, mail
from flaskblog.users.forms import (LoginForm, RegistrationForm, RequestResetForm, 
                                UpdateAccountForm, RequestResetForm, ResetPasswordForm)


users = Blueprint('users', __name__)

@users.route('/register',methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} ! you can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title = 'Register')

@users.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data).first()
        if user  and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you have been logged in', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('login unsuccessful please check email and password', 'danger')
    return render_template('login.html', form=form, title = 'Login')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            old_profile_pic = current_user.profile_pic 
            picture_file = save_picture(form.picture.data)

            if old_profile_pic == 'default.jpg':
                pass
            else:
                delete_profile_picture(old_profile_pic)
            
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Info updated succesfully', 'info')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
        
    profile_pic = url_for('static',filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title = 'Account details', form=form,profile_pic=profile_pic)



@users.route('/posts/<string:username>')
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1, type=int)
 
    posts = Post.query.filter_by(author=user)\
                    .order_by(Post.created_at.desc())\
                    .paginate(page=page,per_page=app.config['POST_PER_PAGE'])
    return render_template('user_posts.html', title=f'Posts by {user.username}', posts=posts, user=user)


@users.route('/resetpassword', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    
    if form.validate_on_submit():
       
        user = User.query.filter_by(email=form.email.data).first()
        
        # send_reset_email(user) will work on this functionality latter
        flash('An email has been sent with instructions to reset your password', 'success')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)


@users.route('/resetpassword/<string:token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('invalid token or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your account password has been updated! You can now log in with your new password', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form, title='Reset Password')
    
