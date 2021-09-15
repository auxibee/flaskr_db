from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already exits')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('email has been used to register an account')

    


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
