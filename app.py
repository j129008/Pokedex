from flask import Flask
from db import db
from flask_migrate import Migrate
from basic.api import basic_api

app = Flask(__name__)
migrate = Migrate(app, db)
app.config.from_pyfile('local.cfg')
app.config.update(migrate=migrate)

app.register_blueprint(basic_api, url_prefix='/basic')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
