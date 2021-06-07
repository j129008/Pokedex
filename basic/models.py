import enum
from db import db


class PokemonType(enum.Enum):
    Grass = 1
    Poison = 2
    Fire = 3


class Info(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.BigInteger, primary_key=True)
    number = db.Column(db.String(10))
    name = db.Column(db.String(100))
    type = db.Column(db.Enum(PokemonType), default=PokemonType.Grass)

    def to_json(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'type': self.type.name
        }
