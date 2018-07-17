from flask import Flask, render_template#, flash, redirect, url_for, session, g, request
from flask_pymongo import PyMongo
from .utils import login_required

def create_app(config_file=None):    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)    
    app.mongo = PyMongo(app)   

    # ToDo: move to own Blueprint
    @app.route('/faq')
    def faq():
        return render_template('faq.html', title='FAQ')

    # ToDo: move to own Blueprint
    @app.route('/dashboard')
    @login_required
    def dashboard():
        stats = {}
        stats['num_orgs'] = app.mongo.db.organisations.find().count()
        stats['num_users'] = app.mongo.db.users.find().count()
        return render_template('dashboard.html', title='Dashboard', stats=stats)

    register_blueprints(app)
    return app

def register_blueprints(app):    
    from scippycrm.organisations import organisations_blueprint
    app.register_blueprint(organisations_blueprint)

    from scippycrm.users import users_blueprint
    app.register_blueprint(users_blueprint)