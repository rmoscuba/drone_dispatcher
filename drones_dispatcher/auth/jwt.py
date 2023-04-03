import datetime
from functools import wraps
import os
from flask import abort, current_app, request

import jwt

from users.model import User


class Token:
    @staticmethod
    def encode_token(user):
        """
        Encode the user data into a jwt token
        :param user: The user
        :return: The token
        """

        payload = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }
        token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token):
        """
        Decode an auth jwt token
        :param token: The token to be decoded
        :return: The valid token or None
        """
        try:
            token = jwt.decode(
                token,
                os.environ.get("SECRET_KEY"),
                algorithms="HS256",
                options={"require_exp": True},
            )
            return token
        except Exception as e:
            return None


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        Enforce a valid jwt token decorator
        :param token: The token to be decoded
        :return: Decorated function
        """
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=Token.decode_token(token)
            if data is None:
                return {
                "message": "Invalid Authentication",
                "data": None,
                "error": "Unauthorized"
            }, 401
            current_user=User.query.filter_by(id = data["id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Invalid Authentication error",
                "data": None,
                "error": str(e)
            }, 500

        return func(*args, **kwargs)

    return decorated
    

token_generator = Token()