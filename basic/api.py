from flask import Blueprint
from flask import jsonify
from flask import request
from basic.models import Info as InfoModel
from basic.models import Type as TypeModel
from basic.models import Evolution as EvolutionModel
from db import db

basic_api = Blueprint('basic', __name__)


@basic_api.route('/info/<int:pid>', methods=['GET'])
def info(pid):
    info_obj = InfoModel.query.filter_by(id=pid).first()

    if info_obj:
        return jsonify(info_obj.to_json())

    return jsonify({'Status': 'Pokemon not found'}), 404


@basic_api.route('/add', methods=['POST'])
def add_pokemon():
    req_data = request.json
    if not InfoModel.verify(req_data):
        return jsonify({'Status': 'Invalid Input'}), 406

    info_obj = InfoModel()
    info_obj.from_json(req_data)
    db.session.add(info_obj)
    db.session.flush()

    for t in req_data['types']:
        type_obj = TypeModel()
        type_obj.from_json({'pid': info_obj.id, 'type': t})
        db.session.add(type_obj)

    db.session.commit()

    return jsonify({'Status': 'Create Success'})


@basic_api.route('/delete/<int:pid>', methods=['DELETE'])
def delete_pokemon(pid):
    info_obj = InfoModel.query.filter_by(id=pid).first()
    if not info_obj:
        return jsonify({'Status': 'Pokemon not Exist'}), 404

    evo_obj = EvolutionModel.query.filter_by(before=pid)
    if evo_obj:
        evo_obj.delete()

    evo_obj = EvolutionModel.query.filter_by(after=pid)
    if evo_obj:
        evo_obj.delete()

    type_obj = TypeModel.query.filter_by(pid=pid)
    if type_obj:
        type_obj.delete()

    db.session.delete(info_obj)
    db.session.commit()

    return jsonify({'Status': 'Delete Success'})
