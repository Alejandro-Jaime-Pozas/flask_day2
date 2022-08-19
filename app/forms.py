from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField # we are importing classes to implement forms
from wtforms.validators import InputRequired, EqualTo

# this form allows end user to input their information, then allows us to store and manipulate that data
class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()]) # validators make sure there is some data input by user
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')]) # here the EqualTo has to be a str for some reason...but refers to the variable
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    body = StringField('Body', validators=[InputRequired()])
    submit = SubmitField()