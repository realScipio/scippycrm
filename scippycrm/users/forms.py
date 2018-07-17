from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    user_id = HiddenField('_id')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('First name')
    sirname = StringField('Sirname')    
    email = StringField('Email')    
    submit = SubmitField('Save')

class UserForm_existing(FlaskForm):
    user_id = HiddenField('_id')
    username = StringField('Username', validators=[DataRequired()])    
    firstname = StringField('First name')
    sirname = StringField('Sirname')    
    email = StringField('Email')    
    submit = SubmitField('Save') 