from flask import render_template, flash, redirect, url_for, session, g, request
from flask import current_app as app

from . import users_blueprint
from .forms import LoginForm

@users_blueprint.route('/', methods=['GET', 'POST'])
def index():    
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

@users_blueprint.route('/logout')
def logout():    
    session.clear()    
    return redirect(url_for('users.index'))