from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')