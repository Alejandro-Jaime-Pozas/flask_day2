from . import api
from flask import jsonify

# here we are linking the __init__.py to this file, returning a json api object
@api.route('/')
def index():
    names = ['Al', 'By', 'Tay']
    return jsonify(names)