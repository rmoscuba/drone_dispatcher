from http import HTTPStatus
from flask import Response, current_app, send_from_directory, url_for
from flask_restful import Resource
from flask import request, make_response
from drones.service import get_drone
from drones.service import create_drone
from drones.service import update_drone
from drones.service import get_drone_medications
from drones.service import get_drones_available
from drones_dispatcher.auth.jwt import token_required


class Drone(Resource):
    @staticmethod
    @token_required
    def post() -> Response:
        """
        New drone response.
        :return: JSON of new medication data
        """
        input_data = request.get_json()
        response = create_drone(request, input_data)
        object_response = make_response(response, response['status'])
        if object_response.status_code == HTTPStatus.CREATED:
            object_response.headers['Location'] = url_for('dronebyid', id=response['data']['id'])
        return object_response


class DroneById(Resource):
    @staticmethod
    @token_required
    def get(id) -> Response:
        """
        Get drone response.
        :return: JSON of the medication data
        """
        response = get_drone(request, id)
        return make_response(response, response['status'])

    @staticmethod
    @token_required
    def put(id) -> Response:
        """
        Update drone response.
        :return: JSON of updated medication data
        """
        input_data = request.get_json()
        response = update_drone(request, input_data, id)
        return make_response(response, response['status'])


class DroneMedicationsById(Resource):
    @staticmethod
    @token_required
    def get(id) -> Response:
        """
        Get drone medications items by drone id response.
        :return: JSON of the medications list data
        """
        response = get_drone_medications(request, id)
        return make_response(response, response['status'])


class DronesLoadingAvailable(Resource):
    @staticmethod
    @token_required
    def get() -> Response:
        """
        Get available drones for loading response.
        :return: JSON of the medication data
        """
        response = get_drones_available(request)
        return make_response(response, response['status'])
