
from flask_login.utils import login_user, current_user, logout_user, login_required
from flask import request, abort
from flaskblog.utils import delete_profile_picture, save_picture
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask import  render_template, url_for, flash, redirect
from flaskblog.forms import LoginForm, RegistrationForm, UpdateAccountForm, NewPostForm
from flaskblog.models import load_user


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page,per_page=app.config['POST_PER_PAGE'])

    return render_template('home.html', posts = posts, title='learning flask')

@app.route('/about')
def about_us():

    return render_template('about.html')

@app.route('/register',methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('home'))

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


@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            old_profile_pic = current_user.profile_pic 
            picture_file = save_picture(form.picture.data)

            delete_profile_picture(old_profile_pic)
            
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Info updated succesfully', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
        
    profile_pic = url_for('static',filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title = 'Account details', form=form,profile_pic=profile_pic)


@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    legend = 'New Post'
    if form.validate_on_submit():
        
        post = Post(title = form.title.data, content=form.body.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('post created succesfully', 'succes')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    legend = 'Edit Post'
    if post.author != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.body.data
        db.session.commit()
        flash('your post has been update', 'success')
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.content
    
    return render_template('new_post.html', title=post.title, post=post, form=form, legend=legend)


@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted succesfully', 'info')
    return redirect(url_for('home'))


@app.route('/posts/<string:username>')
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1, type=int)
 
    posts = Post.query.filter_by(author=user)\
                    .order_by(Post.created_at.desc())\
                    .paginate(page=page,per_page=app.config['POST_PER_PAGE'])
    return render_template('user_posts.html', title=f'Posts by {user.username}', posts=posts, user=user)
  


