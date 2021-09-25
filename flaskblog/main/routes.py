from flask import request, Blueprint, render_template, current_app
from flaskblog.models import Post



main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page,per_page=current_app.config['POST_PER_PAGE'])

    return render_template('home.html', posts = posts, title='learning flask')

@main.route('/about')
def about_us():

    return render_template('about.html')