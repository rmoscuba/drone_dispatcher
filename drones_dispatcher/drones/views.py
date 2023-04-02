from http import HTTPStatus
from flask import Response, current_app, send_from_directory, url_for
from flask_restful import Resource
from flask import request, make_response
from drones.service import get_drone
from drones.service import create_drone
from drones.service import update_drone


class Drone(Resource):
    @staticmethod
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
    def get(id) -> Response:
        """
        Get drone response.
        :return: JSON of the medication data
        """
        response = get_drone(request, id)
        return make_response(response, response['status'])

    @staticmethod
    def put(id) -> Response:
        """
        Update drone response.
        :return: JSON of updated medication data
        """
        input_data = request.get_json()
        response = update_drone(request, input_data, id)
        return make_response(response, response['status'])
