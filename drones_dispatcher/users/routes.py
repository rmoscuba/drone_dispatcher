from flask_restful import Api
from users.views import Login, SignUp


def create_authentication_routes(api: Api):
    """Adds endpoints to the api.
    :param api: Flask-RESTful Api Object
    """
    api.add_resource(SignUp, "/api/auth/register/")
    api.add_resource(Login, "/api/auth/login/")