from flask_restful import Resource
from flask_restful import reqparse


users = [
    {'name': 'lucien'}
]

class Users(Resource):
    def get(self):
        return {
            'message': '',
            'users': users
        }

class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email', 
        required=True,
        location=['form', 'json'],
        help='Email is required'
    )
    parser.add_argument('password', 
        required=True, 
        location=['form', 'json'],
        help='Password is required'
    )

    def get(self, name):
        find = [item for item in users if item['name'] == name]
        if len(find) == 0:
            return {
                'message': 'username not exist!'
            }, 403
        user = find[0]
        if not user:
            return {
                'message': 'username not exist!'
            }, 403

        return {
            'message': '',
            'user': user
        }


    def post(self, name):
        arg = self.parser.parse_args()
        user = {
            'name': name,
            'email': arg['email'],
            'password': arg['password']
        }
        global users
        users.append(user)
        return {
            'message': 'Insert user success',
            'user': user
        }

    def put(self, name):
        arg = self.parser.parse_args()
        find = [item for item in users if item['name'] == name]
        if len(find) == 0:
            return {
                'message': 'username not exist!'
            }, 403

        user = find[0]
        user['email'] = arg['email']
        user['password'] = arg['password']

        return {
            'message': 'Update user success',
            'user': user
        }


    def delete(self, name):
        global users
        users = [item for item in users if item['name'] != name]
        return {
            'message': 'Delete done!'
        }