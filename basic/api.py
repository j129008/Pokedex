from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy.exc import IntegrityError
from basic.models import Info as InfoModel
from basic.models import Type as TypeModel
from basic.models import Evolution as EvolutionModel
from basic.models import PokemonType
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

    try:
        db.session.flush()
    except IntegrityError as err:
        db.session.rollback()
        if 'Duplicate entry' in str(err):
            return jsonify({'Status': 'Duplicate Pokemon'})

    for t in req_data['types']:
        type_obj = TypeModel()
        type_obj.from_json({'pid': info_obj.id, 'type': t})
        db.session.add(type_obj)

    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        if 'Duplicate entry' in str(err):
            return jsonify({'Status': 'Duplicate Type'})

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


@basic_api.route('/search', methods=['GET'])
def search():
    req_data = request.args

    search_type = req_data.get('type')
    if not search_type:
        return jsonify({'Status': 'Invalid Input'}), 406

    if search_type not in PokemonType.__members__:
        return jsonify({'Status': 'Invalid Type'}), 406

    type_objs = TypeModel.query.filter_by(type=PokemonType[search_type]).all()

    return jsonify({'PokemonIds': [obj.pid for obj in type_objs]})


@basic_api.route('/evolution/<int:before_pid>', methods=['POST'])
def add_evolution(before_pid):
    req_data = request.json
    after_pid = req_data.get('after_pid')
    after_pid = int(after_pid) if type(after_pid) is str and after_pid.isnumeric() else after_pid

    evo_obj = EvolutionModel()
    evo_obj.from_json({
        'before': before_pid,
        'after': after_pid
    })

    db.session.add(evo_obj)
    db.session.commit()

    return jsonify({'Status': 'Add Success'})


@basic_api.route('/evolution/<int:before_pid>', methods=['DELETE'])
def delete_evolution(before_pid):
    req_data = request.json
    after_pid = req_data.get('after_pid')
    after_pid = int(after_pid) if type(after_pid) is str and after_pid.isnumeric() else after_pid

    evo_obj = EvolutionModel.query.filter_by(before=before_pid).filter_by(after=after_pid)

    if evo_obj:
        evo_obj.delete()

    db.session.commit()

    return jsonify({'Status': 'Delete Success'})
