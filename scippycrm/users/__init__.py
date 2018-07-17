from flask import Blueprint
users_blueprint = Blueprint('users', __name__, template_folder='templates')

from . import routes