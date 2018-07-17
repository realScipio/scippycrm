from flask import Blueprint
organisations_blueprint = Blueprint('organisations', __name__, template_folder='templates')

from . import routes