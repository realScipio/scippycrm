from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class OrganisationForm(FlaskForm):
    org_id = HiddenField('_id')
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    zipcode = StringField('Zipcode')
    city = StringField('City')
    country = StringField('Country')
    phone = StringField('Phone')
    email = StringField('Email')
    url = StringField('URL')
    submit = SubmitField('Save') 