from flask import Flask
from flask_restful import Api

from resources.user import User, Users
from common.db import db
from common.ma import ma

import pymysql
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api = Api(app)

    api.add_resource(User, '/api/user/<string:name>')
    api.add_resource(Users, '/api/users/')

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    return app