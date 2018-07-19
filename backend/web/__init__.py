from flask import Blueprint

main = Blueprint('main', __name__, template_folder="templates", static_folder='static/js')
swagger = Blueprint('swagger', __name__, static_folder='static/docs')

from . import controller
