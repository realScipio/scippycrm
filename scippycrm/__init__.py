import os
from functools import wraps
from flask import Flask, Markup, render_template, flash, redirect, url_for, session, g, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

def create_app(config_file=None):    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)
    mongo = PyMongo(app)

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):        
            if 'logged_in' in session:
                return f(*args, **kwargs)        
            return redirect(url_for('index'))
        return decorated_function

    @app.route('/', methods=['GET', 'POST'])
    def index():
        class LoginForm(FlaskForm):
            username = StringField('Username', validators=[DataRequired()])
            password = PasswordField('Password', validators=[DataRequired()])    
            submit = SubmitField('Login')

        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            if username == app.config['USERNAME'] and password == app.config['PASSWORD']:
                session['logged_in'] = True
                session['username'] = username            
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index'))
        return render_template('index.html', title='Login', form=form)

    @app.route('/logout')
    def logout():    
        session.clear()    
        return redirect(url_for('index'))

    @app.route('/faq')
    def faq():
        return render_template('faq.html', title='FAQ')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        stats = {}
        stats['num_orgs'] = mongo.db.organisations.find().count()
        return render_template('dashboard.html', title='Dashboard', stats=stats)

    @app.route('/organisations')    
    @login_required
    def organisations():
        coll = mongo.db.organisations
        orgs = coll.find()
        return render_template('organisations.html', title='Organisations', orgs=orgs)

    @app.route('/organisation/new', methods=['GET', 'POST'])
    @app.route('/organisation/<ObjectId:org_id>', methods=['GET', 'POST'])
    @login_required
    def organisation(org_id='new'):
        coll = mongo.db.organisations
        if org_id == 'new':
            org = {}
            title = 'New organisation'
        else:            
            org = coll.find_one_or_404({'_id': org_id})
            title = 'Organisation: ' + org['name']
        
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

        form = OrganisationForm(obj=org)        

        if form.validate_on_submit():
            obj_for_update = {}
            for fieldname, value in form.data.items():
                if (fieldname != 'submit' and fieldname != 'csrf_token' and fieldname != 'org_id'):
                    obj_for_update[fieldname] = value            

            # insert new organisation record with POST-data from OrganisationForm
            if org_id == 'new':
                org_id = coll.insert_one(obj_for_update).inserted_id

            # update Mongo organisation record with POST-data from OrganisationForm
            else:
                result = coll.update_one(
                    {"_id": ObjectId(org_id)},
                    {"$set": obj_for_update}
                )
            
            # clean up Mongo records (no empty keys)
            org = coll.find_one_or_404({'_id': org_id})            
            clean_obj = {}
            for key in org:
                if org[key] != None and org[key] != "":
                    clean_obj[key] = org[key]            
            result = coll.replace_one({'_id': ObjectId(org_id)}, clean_obj)            

            return redirect(url_for('organisation', org_id=org_id))         

        return render_template('organisation.html', title=title, org=org, form=form)


    return app
