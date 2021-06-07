import enum
from db import db


class PokemonType(enum.Enum):
    Grass = 1
    Poison = 2
    Fire = 3


class Evolution(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    before = db.Column(db.BigInteger)
    after = db.Column(db.BigInteger)

    def to_json(self):
        info_obj = Info.query.filter_by(id=self.after).first()

        return {
            'number': info_obj.number,
            'name': info_obj.name,
            'type': info_obj.type.name
        }


class Info(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    number = db.Column(db.String(10))
    name = db.Column(db.String(100))
    type = db.Column(db.Enum(PokemonType), default=PokemonType.Grass)

    def to_json(self):
        evolution_objs = Evolution.query.filter_by(id=self.id).all()

        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'type': self.type.name,
            'evolutions': [obj.to_json() for obj in evolution_objs]
        }
