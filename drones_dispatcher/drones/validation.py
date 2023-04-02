from marshmallow import Schema, fields, validate


# Drone validation schema
# Requires name with only letters, numbers, -, _ , 
# code with only upper case letters, _ and numbers
# and weight
class DroneInputSchema(Schema):
    serial_number = fields.Str(required=True,
                      validate=validate.Length(max=100))
    model = fields.Str(required=True, 
                      validate=validate.OneOf([
                        "Lightweight", 
                        "Middleweight", 
                        "Cruiserweight", 
                        "Heavyweight"]))
    weight_limit = fields.Int(required=True,
                      validate=validate.Range(max=500))
    battery_capacity = fields.Int(required=True,
                      validate=validate.Range(max=100))
    state = fields.Str(required=True, 
                      validate=validate.OneOf([
                        "IDLE",
                        "LOADING",
                        "LOADED",
                        "DELIVERING",
                        "DELIVERED",
                        "RETURNING"]))

# UUID validation schema
# Requires a valid UUID
class UUIDSchema(Schema):
    id = fields.UUID(attribute="id")
