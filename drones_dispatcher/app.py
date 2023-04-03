"""App entry point."""
"""Initialize Flask app."""
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from dispatcher import dispatcher

db = SQLAlchemy()
migrate = Migrate()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(dispatcher.dispatch,'interval',seconds=60)
scheduler.start()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object("config.Config")

    api = Api(app=app)

    from users.routes import create_authentication_routes
    from medications.routes import create_medications_routes
    from drones.routes import create_drone_routes

    create_authentication_routes(api=api)
    create_medications_routes(api=api)
    create_drone_routes(api=api)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # do in context stuff
        return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)