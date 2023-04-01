import datetime
import os

import jwt


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
        :return: Fictionary the user's id and username
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

token_generator = Token()