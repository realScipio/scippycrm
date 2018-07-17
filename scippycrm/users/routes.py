from flask import render_template, flash, redirect, url_for, session, g, request, Markup
from flask import current_app as app
from bson.objectid import ObjectId
from passlib.hash import sha512_crypt

from scippycrm import login_required
from . import users_blueprint
from .forms import LoginForm, UserForm

# login page, for this app it's the index
@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        coll = app.mongo.db.users        
        num_users = coll.find().count()

        # Zero users registered in database,
        # default login with app.config['USERNAME']:app.config['PASSWORD']
        if num_users == 0:            
            username = form.username.data
            password = form.password.data
        
            # add default login to session data
            if username == app.config['USERNAME'] and password == app.config['PASSWORD']:
                session['logged_in'] = True
                session['username'] = username            
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('users.index'))

        # There's at least one registed user in database,
        # default login now prohibited
        else:            
            username = form.username.data
            password = form.password.data

            # get user data from mongo
            user = coll.find_one({"username": username})

            # the user is present in mongo
            if user != None:
                stored_pwd = user['password']

                # check if passwords match
                if sha512_crypt.verify(password, stored_pwd):
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('dashboard'))

                # passwords don't match
                else:
                    return redirect(url_for('users.index'))

            # user not present in mongo
            else:
                return redirect(url_for('users.index'))            
                      
    return render_template('users/index.html', title='Login', form=form)

# logout, flush session data
@users_blueprint.route('/logout')
def logout():    
    session.clear()    
    return redirect(url_for('users.index'))

# show users overview
@users_blueprint.route('/users')    
@login_required
def users():
    coll = app.mongo.db.users
    users = coll.find()
    num_users = users.count()
    return render_template('users/users.html', title='Users', users=users, num_users=num_users)

# show / insert / update single user data
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

    # validate form data when submitted via POST request
    if form.validate_on_submit():
        obj_for_update = {}
        for fieldname, value in form.data.items():
            # add hashed password, instead of plain text password,to `obj_for_update``
            if fieldname == 'password':
                obj_for_update[fieldname] = sha512_crypt.encrypt(str(value))
            elif (fieldname != 'submit' and fieldname != 'csrf_token' and fieldname != 'user_id'):
                obj_for_update[fieldname] = value        

        # insert new user record with POST-data from UserForm
        if user_id == 'new':
            user_id = coll.insert_one(obj_for_update).inserted_id

        # update Mongo user record with POST-data from UserForm
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