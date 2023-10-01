from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Too long, max length is 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email(), Length(max=50, message="Too long, max length is 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message="Too long, max length is 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message="Too long, max length is 30 characters")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Too long, max length is 100 characters")])
    content = StringField("Content", validators=[InputRequired()])
