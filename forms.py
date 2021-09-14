from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email,EqualTo

class BaseForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class Registration(BaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(BaseForm):
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
