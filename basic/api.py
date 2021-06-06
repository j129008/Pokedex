from flask import Blueprint
from flask import jsonify

basic_api = Blueprint('basic', __name__)


@basic_api.route('/info', methods=['GET'])
def info():
    return jsonify({'Status': 'hello world'})
