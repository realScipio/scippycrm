import os
from functools import wraps
from flask import Flask, Markup, render_template, flash, redirect, url_for, session, g, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo

def create_app(config_file=None):    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)    
    app.mongo = PyMongo(app)

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):        
            if 'logged_in' in session:
                return f(*args, **kwargs)        
            return redirect(url_for('index'))
        return decorated_function

    @app.route('/faq')
    def faq():
        return render_template('faq.html', title='FAQ')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        stats = {}
        stats['num_orgs'] = app.mongo.db.organisations.find().count()
        return render_template('dashboard.html', title='Dashboard', stats=stats)

    register_blueprints(app)
    return app

def register_blueprints(app):    
    from scippycrm.organisations import organisations_blueprint
    app.register_blueprint(organisations_blueprint)

    from scippycrm.users import users_blueprint
    app.register_blueprint(users_blueprint)
    