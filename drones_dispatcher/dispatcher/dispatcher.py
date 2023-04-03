from flask import current_app as app

def dispatch():

    from app import create_app
    from app import db
    from drones.model import Drone
    from drones.model import StateEnum

    app = create_app()
    with app.app_context():
        for drone in Drone.query.all():

            # Consume battery when not idle
            if drone.battery_capacity > 25 and drone.state != StateEnum.IDLE:
                drone.battery_capacity -= 2

            # Charge in IDLE state
            if drone.state == StateEnum.IDLE and drone.battery_capacity < 98:
                drone.battery_capacity += 2

            # Delete medications when delivered
            if drone.state == StateEnum.DELIVERED:
                drone.medications = []
            
            if drone.state == StateEnum.RETURNING:
                # Cange to IDLE after returning
                drone.state = StateEnum.IDLE

            else:
                # else change to next stage
                drone.state = drone.state.next()
                
            # Save changes to DB
            db.session.commit()
