from flask_restful import Resource, reqparse, request
from auth_api.models.user import UserModel
from auth_api.security import require_appkey

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field is required")  # parse the json and add specifications
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User "{}" already exists'.format(data['username'])}, 400

        UserModel(**data).save_to_db()
        return {'message': 'User "{}" created'.format(data['username'])}, 201


class UserAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field is required")  # parse the json and add specifications
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field is required")

    def post(self):
        data = UserAuth.parser.parse_args()
        u = UserModel.find_by_username(data['username'])
        if u:
            if u.check_password(data['password']):
                return u.json()
            return {'message': 'Incorrect password'}, 401

        else:
            return {'message': 'User "{}" does not exists'.format(data['username'])}, 400


class User(Resource):
    method_decorators = [require_appkey]

    def get(self):
        api_key = request.headers.get('api_key')
        u = UserModel.find_by_apikey(api_key)
        if u:
            return u.json()
        return {'message': 'Invalid api_key'}




