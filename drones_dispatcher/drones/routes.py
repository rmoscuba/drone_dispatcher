
from flask_restful import Api
from drones.views import Drone
from drones.views import DroneById
from drones.views import DroneMedicationsById
from drones.views import DronesLoadingAvailable


def create_drone_routes(api: Api):
    """Adds endpoints to the api.
    :param api: Flask-RESTful Api Object
    """
    # api.add_resource(Medication, "/api/medication/")
    api.add_resource(Drone, "/api/drone/")
    api.add_resource(DroneById, "/api/drone/<string:id>/")
    api.add_resource(DroneMedicationsById, "/api/drone/<string:id>/medications/")
    api.add_resource(DronesLoadingAvailable, "/api/drone/available/")
