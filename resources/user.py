from flask_restful import Resource
from flask import request

from models.schema.user_schema import UserSchema
from marshmallow import ValidationError

from models.user import UserModel


user_schema = UserSchema(many=False)


class Users(Resource):
    def get(self):
        users = UserModel.get_all_user()
        return {
            'message': '',
            'users': user_schema.dump(users, many=True)
        }

class User(Resource):

    @classmethod
    def get_param(cls, name):
        data = request.get_json(force=False)
        if data is None:
            data = request.form
        data['name'] = name
        return data

    def get(self, name):
        user = UserModel.get_user(name)
        if not user:
            return {
                'message': 'username not exist!'
            }, 403
        return {
            'message': '',
            'user': user_schema.dump(user)
        }


    def post(self, name):
        json_data = User.get_param(name)
        
        # marshmallow 3 開始沒有errors 欄位了
        # 所以改成以下用法
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data
            print(errors)
            print(valid_data)
            return {
                'message': errors
            }, 433
        
        user = UserModel(name, data['email'], data['password'])
        user.add_user()

        return {
            'message': 'Insert user success',
            'user': user_schema.dump(user)
        }

    def put(self, name):
        json_data = User.get_param(name)
        # marshmallow 3 開始沒有errors 欄位了
        # 所以改成以下用法
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data
            print(errors)
            print(valid_data)
            return {
                'message': errors
            }, 433

        user = UserModel.get_user(name)
        if not user:
            return {
                'message': 'username not exist!'
            }, 403

        user.email = data['email']
        user.password = data['password']
        user.update_user()

        return {
            'message': 'Update user success',
            'user': user_schema.dump(user)
        }


    def delete(self, name):
        user = UserModel.get_user(name)
        if not user:
            return {
                'message': 'username not exist!'
            }, 403
        user.delete_user()

        return {
            'message': 'Delete done!'
        }