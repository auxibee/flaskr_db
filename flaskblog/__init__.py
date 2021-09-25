import os
from flask import Flask
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e133c32c00b2eb8f676e8695531d0ee3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['POST_PER_PAGE'] = 5
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yaw217@gmail.com'
app.config['MAIL_PASSWORD'] = "217317auxi"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
