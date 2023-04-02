
from flask_restful import Api
from medications.views import Medication
from medications.views import MedicationImageUpload
from medications.views import MedicationById


def create_medications_routes(api: Api):
    """Adds endpoints to the api.
    :param api: Flask-RESTful Api Object
    """
    # api.add_resource(Medication, "/api/medication/")
    api.add_resource(Medication, "/api/medication/")
    api.add_resource(MedicationById, "/api/medication/<string:id>/")
    api.add_resource(MedicationImageUpload, "/api/medication/<string:id>/image/")
