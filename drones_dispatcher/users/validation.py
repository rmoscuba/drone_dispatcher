from marshmallow import Schema, fields, validate


# User valitation schema
# Requires username with at least 4 chars, a valid fomatted email, 
# and an at least 6 chars long password. 
class SignupInputSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


# User login data valitation schema
# Requires username with at least 4 chars, a valid fomatted email, 
# and an at least 6 chars long password. 
class LoginInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
