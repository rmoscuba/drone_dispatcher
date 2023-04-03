import json
import os
import uuid
import jwt
import datetime
from utils.response import generate_response
from app import db
from os import environ
from drones.model import Drone
from auth.jwt import Token
from drones.validation import DroneInputSchema
from drones.validation import UUIDSchema
from http import HTTPStatus
from werkzeug.utils import secure_filename
from flask import current_app

def create_drone(request, input_data):
    """
    Create a new drone service

    :param request: The request
    :param input_data: Drone input data
    :return: A dictionary response
    """
    create_validation_schema = DroneInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_serial_number_exist = Drone.query.filter_by(serial_number=input_data.get("serial_number")).first()
    if check_serial_number_exist:
        return generate_response(
            message="A drone already exist with this serial number", status=HTTPStatus.BAD_REQUEST
        )

    new_drone = Drone(**input_data)  # Create an instance of the Medication model
    db.session.add(new_drone)  # Adds new Medication to the DB
    db.session.commit()
    return generate_response(
        data=new_drone.as_dict(), message="Drone Created", status=HTTPStatus.CREATED
    )


def get_drone(request, id):
    """
    Get a drone by id service

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

    drone = Drone.query.filter_by(id=canon_id).first()
    if not drone:  
        return generate_response(
            message="A drone does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    return generate_response(
        data=drone.as_dict(), message="Drone", status=HTTPStatus.OK
    )


def get_drone_medications(request, id):
    """
    Checking loaded medication items for a given drone id

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

    drone = Drone.query.filter_by(id=canon_id).first()
    if not drone:  
        return generate_response(
            message="A drone does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    medications = []
    for medication in drone.medications:
        medications.append(medication.as_dict())

    return generate_response(
        data={"medications": medications, "count": len(medications)}, message="Drone", status=HTTPStatus.OK
    )


def get_drones_available(request):
    """
    Checking available drones for loading

    :param request: The request
    :return: A dictionary response
    """
    drones = Drone.query.filter_by(state="IDLE").all()

    drones_list = []
    for drone in drones:
        drones_list.append(drone.as_dict())

    return generate_response(
        data={"drones": drones_list, "count": len(drones_list)}, message="Drones", status=HTTPStatus.OK
    )


def update_drone(request, input_data, id):
    """
    Update a drone by id service

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

    create_validation_schema = DroneInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    drone = Drone.query.filter_by(id=canon_id).first()
    if not drone:  
        return generate_response(
            message="A medication does not exist with this id", status=HTTPStatus.NOT_FOUND
        )

    check_serial_number_exist = Drone.query.filter(Drone.id != canon_id).filter_by(serial_number=input_data.get("serial_number")).first()
    if check_serial_number_exist:
        return generate_response(
            message="A drone already exist with this name", status=HTTPStatus.BAD_REQUEST
        )

    drone.update(input_data)  # Update Drone to the DB
    db.session.commit()
    
    return generate_response(
        data=drone.as_dict(), message="Drone", status=HTTPStatus.CREATED
    )
