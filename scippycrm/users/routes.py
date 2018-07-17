from flask import render_template, flash, redirect, url_for, session, g, request, Markup
from flask import current_app as app
from bson.objectid import ObjectId

from scippycrm import login_required
from . import users_blueprint
from .forms import LoginForm, UserForm

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
    return render_template('users/index.html', title='Login', form=form)

@users_blueprint.route('/logout')
def logout():    
    session.clear()    
    return redirect(url_for('users.index'))

@users_blueprint.route('/users')    
@login_required
def users():
    coll = app.mongo.db.users
    users = coll.find()
    return render_template('users/users.html', title='Users', users=users)

@users_blueprint.route('/user/new', methods=['GET', 'POST'])
@users_blueprint.route('/user/<ObjectId:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id='new'):
    coll = app.mongo.db.users
    if user_id == 'new':
        user = {}
        title = 'New user'
    else:            
        user = coll.find_one_or_404({'_id': user_id})
        title = 'User: ' + user['username']
    
    form = UserForm(obj=user)        

    if form.validate_on_submit():
        obj_for_update = {}
        for fieldname, value in form.data.items():
            if (fieldname != 'submit' and fieldname != 'csrf_token' and fieldname != 'user_id'):
                obj_for_update[fieldname] = value            

        # insert new organisation record with POST-data from OrganisationForm
        if user_id == 'new':
            user_id = coll.insert_one(obj_for_update).inserted_id

        # update Mongo organisation record with POST-data from OrganisationForm
        else:
            result = coll.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": obj_for_update}
            )
        
        # clean up Mongo records (no empty keys)
        user = coll.find_one_or_404({'_id': user_id})            
        clean_obj = {}
        for key in user:
            if user[key] != None and user[key] != "":
                clean_obj[key] = user[key]            
        result = coll.replace_one({'_id': ObjectId(user_id)}, clean_obj)            

        return redirect(url_for('users.user', user_id=user_id))         

    return render_template('users/user.html', title=title, user=user, form=form)