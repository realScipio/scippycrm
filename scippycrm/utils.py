from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):        
        if 'logged_in' in session:
            return f(*args, **kwargs)        
        return redirect(url_for('users.index'))
    return decorated_function