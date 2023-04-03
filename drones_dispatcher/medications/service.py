import json
import os
import uuid
import jwt
import datetime
from drones.model import Drone
from utils.response import generate_response
from app import db
from os import environ
from medications.model import Medication
from flask_bcrypt import generate_password_hash
from auth.jwt import Token
from medications.validation import (
    MedicationInputSchema,
    MedicationUploadImageInputSchema,
    UUIDSchema
)
from http import HTTPStatus
from werkzeug.utils import secure_filename
from flask import current_app

def create_medication(request, input_data):
    """
    Create a new medication service

    :param request: The request
    :param input_data: Medication input data
    :return: A dictionary response
    """
    create_validation_schema = MedicationInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    
    # Prevent the drone from being loaded with more weight that it can carry
    check_drone_exist = Drone.query.filter_by(id=input_data.get("drone_id")).first()
    if check_drone_exist:
        message = check_drone_exist.cannot_load_error(input_data.get("weight"))
        if message:
            return generate_response(
                message=message, status=HTTPStatus.BAD_REQUEST
            )

    check_name_exist = Medication.query.filter_by(name=input_data.get("name")).first()
    check_code_exist = Medication.query.filter_by(code=input_data.get("code")).first()
    if check_name_exist:
        return generate_response(
            message="A medication already exist with this name", status=HTTPStatus.BAD_REQUEST
        )
    elif check_code_exist:
        return generate_response(
            message="A medication already exist with this code", status=HTTPStatus.BAD_REQUEST
        )

    new_medication = Medication(**input_data)  # Create an instance of the Medication model
    db.session.add(new_medication)  # Adds new Medication to the DB
    db.session.commit()
    return generate_response(
        data=new_medication.as_dict(), message="Medication Created", status=HTTPStatus.CREATED
    )


def get_medication(request, id):
    """
    Get a medication by id service

    :param request: The request
    :param id: Medication id
    :return: A dictionary response
    """
    uuid_validation_schema = UUIDSchema()
    errors = uuid_validation_schema.validate({"id": id})
    if errors:
        return generate_response(message=errors)

    # Convert to a canonical UUID string
    canon_id = str(uuid.UUID(id))

    medication = Medication.query.filter_by(id=canon_id).first()
    if not medication:  
        return generate_response(
            message="A medication does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    return generate_response(
        data=medication.as_dict(), message="Medication", status=HTTPStatus.OK
    )


def update_medication(request, input_data, id):
    """
    Get a medication by id service

    :param request: The request
    :param id: Medication id
    :return: A dictionary response
    """
    uuid_validation_schema = UUIDSchema()
    errors = uuid_validation_schema.validate({"id": id})
    if errors:
        return generate_response(message=errors)

    # Convert to a canonical UUID string
    canon_id = str(uuid.UUID(id))

    create_validation_schema = MedicationInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    medication = Medication.query.filter_by(id=canon_id).first()
    if not medication:  
        return generate_response(
            message="A medication does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    # Prevent medication from being loaded by another drone
    if medication.drone_id and medication.drone_id != input_data.get("drone_id") and input_data.get("drone_id") is not None:
        return generate_response(
                message="Medication already loaded", status=HTTPStatus.BAD_REQUEST
            )

    # Prevent the drone from being loaded with more weight that it can carry
    if not medication.drone_id:
        check_drone_exist = Drone.query.filter_by(id=input_data.get("drone_id")).first()
        if check_drone_exist:
            message = check_drone_exist.cannot_load_error(input_data.get("weight"))
            if message:
                return generate_response(
                    message=message, status=HTTPStatus.BAD_REQUEST
                )

    check_name_exist = Medication.query.filter(Medication.id != canon_id).filter_by(name=input_data.get("name")).first()
    check_code_exist = Medication.query.filter(Medication.id != canon_id).filter_by(code=input_data.get("code")).first()
    if check_name_exist:
        return generate_response(
            message="A medication already exist with this name", status=HTTPStatus.BAD_REQUEST
        )
    elif check_code_exist:
        return generate_response(
            message="A medication already exist with this code", status=HTTPStatus.BAD_REQUEST
        )

    medication.update(input_data)  # Update Medication to the DB
    db.session.commit()
    
    return generate_response(
        data=medication.as_dict(), message="Medication", status=HTTPStatus.CREATED
    )


def medication_image_upload(request, input_data, id):

    def valid_file(file):
        return file.content_type in {"image/jpeg", "image/png"}

    uuid_validation_schema = UUIDSchema()
    errors = uuid_validation_schema.validate({"id": id})
    if errors:
        return generate_response(message=errors)
    canon_id = str(uuid.UUID(id))

    medication = Medication.query.filter_by(id=canon_id).first()
    if not medication:  
        return generate_response(
            message="A medication does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    create_validation_schema = MedicationUploadImageInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    request_file = request.files['file']
    image_name = ""
    if request_file and valid_file(request_file):
        file_ext = request_file.content_type.split("/")[1]
        filename = f"{canon_id}.{file_ext}"
        request_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_name = filename 
    else:
        return generate_response(message="Invalid file type, allowed: jpg, png")

    medication.update({"image": image_name})
    db.session.commit()
    return generate_response(
        data=medication.as_dict(), message="Medication", status=HTTPStatus.CREATED
    )
