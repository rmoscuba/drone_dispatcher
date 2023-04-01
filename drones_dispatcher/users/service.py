import json
import jwt
import datetime
from utils.response import generate_response
from app import db
from os import environ
from users.model import User
from flask_bcrypt import generate_password_hash
from auth.jwt import Token
from users.validation import (
    LoginInputSchema,
    SignupInputSchema
)
from http import HTTPStatus


def create_user(request, input_data):
    """
    Create a new user service

    :param request: The request
    :param input_data: User input data
    :return: A dictionary response
    """
    create_validation_schema = SignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.query.filter_by(
        username=input_data.get("username")
    ).first()
    check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
    if check_username_exist:
        return generate_response(
            message="An account already exist with this username", status=HTTPStatus.BAD_REQUEST
        )
    elif check_email_exist:
        return generate_response(
            message="An account already exist with this email", status=HTTPStatus.BAD_REQUEST
        )

    new_user = User(**input_data)  # Create an instance of the User model
    new_user.hash_password()
    db.session.add(new_user)  # Adds new User to the DB
    db.session.commit()
    del input_data["password"]
    return generate_response(
        data=input_data, message="User Created", status=HTTPStatus.CREATED
    )


def login_user(request, input_data):
    """
    Login user service

    :param request: The request
    :param input_data: User input data
    :return: A dictionary response with login result
    """
    create_validation_schema = LoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    get_user = User.query.filter_by(email=input_data.get("email")).first()
    if get_user is None:
        return generate_response(message="User not found", status=HTTPStatus.BAD_REQUEST)
    if get_user.check_password(input_data.get("password")):

        token = Token.encode_token(get_user)
        
        input_data["token"] = token
        return generate_response(
            data=input_data, message="User login successfully", status=HTTPStatus.CREATED
        )
    else:
        return generate_response(
            message="Password is wrong", status=HTTPStatus.BAD_REQUEST
        )
