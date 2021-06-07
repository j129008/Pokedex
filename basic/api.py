from flask import Blueprint
from flask import jsonify
from basic.models import Info as InfoModel

basic_api = Blueprint('basic', __name__)


@basic_api.route('/info/<int:pid>', methods=['GET'])
def info(pid):
    info_obj = InfoModel.query.filter_by(id=pid).first()

    if info_obj:
        return jsonify(info_obj.to_json())

    return jsonify({'Status': 'Pokemon not found'}), 404
