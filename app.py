from flask import Flask
from flask_restful import Api

from resources.user import User, Users
from common.db import db
from common.ma import ma

import pymysql

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/api/user/<string:name>')
api.add_resource(Users, '/api/users/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@127.0.0.1:3307/mydb'

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()