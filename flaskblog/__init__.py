from flask import Flask
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e133c32c00b2eb8f676e8695531d0ee3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['POST_PER_PAGE'] = 5

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from flaskblog import routes