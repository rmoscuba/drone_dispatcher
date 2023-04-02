
from flask_restful import Api
from drones.views import Drone
from drones.views import DroneById


def create_drone_routes(api: Api):
    """Adds endpoints to the api.
    :param api: Flask-RESTful Api Object
    """
    # api.add_resource(Medication, "/api/medication/")
    api.add_resource(Drone, "/api/drone/")
    api.add_resource(DroneById, "/api/drone/<string:id>/")
