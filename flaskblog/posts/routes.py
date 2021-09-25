
from flask_login.utils import  current_user,  login_required
from flask import request, abort,Blueprint,render_template, url_for, flash, redirect
from flaskblog.models import  Post
from flaskblog import  db
from flaskblog.posts.forms import NewPostForm



posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    legend = 'New Post'
    if form.validate_on_submit():
        
        post = Post(title = form.title.data, content=form.body.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('post created succesfully', 'succes')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.content
    
    return render_template('new_post.html', title=post.title, post=post, form=form, legend=legend)


@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted succesfully', 'info')
    return redirect(url_for('main.home'))
