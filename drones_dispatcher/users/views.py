from flask import Response
from flask_restful import Resource
from flask import request, make_response
from users.service import create_user, login_user


class SignUp(Resource):
    @staticmethod
    def post() -> Response:
        """
        New user creation response.
        :return: JSON of new user data
        """
        input_data = request.get_json()
        response = create_user(request, input_data)
        return make_response(response, response['status'])


class Login(Resource):
    @staticmethod
    def post() -> Response:
        """
        User login response.
        :return: JSON of logged in user data
        """
        input_data = request.get_json()
        response = login_user(request, input_data)
        return make_response(response, response['status'])
