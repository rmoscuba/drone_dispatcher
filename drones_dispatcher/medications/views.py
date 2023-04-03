from http import HTTPStatus
from flask import Response, current_app, send_from_directory, url_for
from flask_restful import Resource
from flask import request, make_response
from medications.service import get_medication
from medications.service import create_medication
from medications.service import update_medication
from medications.service import medication_image_upload
from auth.jwt import token_required


class Medication(Resource):
    @staticmethod
    @token_required
    def post() -> Response:
        """
        New medication response.
        :return: JSON of new medication data
        """
        input_data = request.get_json()
        response = create_medication(request, input_data)
        object_response = make_response(response, response['status'])
        if object_response.status_code == HTTPStatus.CREATED:
            object_response.headers['Location'] = url_for('medicationbyid', id=response['data']['id'])
        return object_response


class MedicationById(Resource):
    @staticmethod
    @token_required
    def get(id) -> Response:
        """
        Get medication response.
        :return: JSON of the medication data
        """
        response = get_medication(request, id)
        return make_response(response, response['status'])

    @staticmethod
    @token_required
    def put(id) -> Response:
        """
        Update medication response.
        :return: JSON of updated medication data
        """
        input_data = request.get_json()
        response = update_medication(request, input_data, id)
        return make_response(response, response['status'])


class MedicationImageUpload(Resource):
    @staticmethod
    @token_required
    def put(id) -> Response:
        """
        Medication image upload response.
        :return: JSON with image url 
        """
        input_data = request.files
        response = medication_image_upload(request, input_data, id)
        object_response = make_response(response, response['status'])
        if object_response.status_code == HTTPStatus.CREATED:
            object_response.headers['Location'] = url_for('medicationimageupload', id=response['data']['id'])
        return object_response

    @staticmethod
    @token_required
    def get(id) -> Response:
        """
        Medication image response
        :return: JSON with image url 
        """
        response = get_medication(request, id)
        if response['status'] != HTTPStatus.OK:
            return make_response(response, response['status'])
        image_name = response['data']['image']
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], image_name)