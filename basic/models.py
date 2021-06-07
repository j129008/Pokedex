import enum
from db import db


class PokemonType(enum.Enum):
    Grass = 1
    Poison = 2
    Fire = 3


class Type(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    pid = db.Column(db.BigInteger)
    type = db.Column(db.Enum(PokemonType), default=PokemonType.Grass)


class Evolution(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    before = db.Column(db.BigInteger)
    after = db.Column(db.BigInteger)

    def to_json(self):
        info_obj = Info.query.filter_by(id=self.after).first()
        type_objs = Type.query.filter_by(pid=info_obj.id).all()

        return {
            'number': info_obj.number,
            'name': info_obj.name,
            'type': [type_obj.type.name for type_obj in type_objs]
        }


class Info(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    number = db.Column(db.String(10))
    name = db.Column(db.String(100))

    def to_json(self):
        evolution_objs = Evolution.query.filter_by(id=self.id).all()
        type_objs = Type.query.filter_by(pid=self.id).all()

        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'type': [type_obj.type.name for type_obj in type_objs],
            'evolutions': [obj.to_json() for obj in evolution_objs]
        }
