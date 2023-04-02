from marshmallow import Schema, fields, validate


# Medication valitation schema
# Requires name with only letters, numbers, -, _ , 
# code with only upper case letters, _ and numbers
# and weight
class MedicationInputSchema(Schema):
    name = fields.Str(required=True,
                      validate=validate.Regexp("^[A-Za-z0-9\\-_]+$", 
                      error="Only letters, numbers, -, _ allowed"))
    code = fields.Str(required=True, 
                      validate=validate.Regexp("^[A-Z0-9_]+$", 
                      error="Only upper case letters, _ and numbers allowed"))
    weight = fields.Int(required=True)
    drone_id = fields.UUID(attribute="id")

# UUID valitation schema
# Requires a valid UUID
class UUIDSchema(Schema):
    id = fields.UUID(attribute="id")


# Medication file image valitation schema
# Requires a file type 
class MedicationUploadImageInputSchema(Schema):
    file = fields.Raw(type="file")
