from marshmallow import Schema, fields, validate, ValidationError
import os

def validate_non_negative(value):
    if value < 0:
        raise ValidationError("Value must be non-negative.")
    
class UserSchema(Schema):
    username = fields.Str(required=True, 
                        validate=[validate.Regexp('^[a-zA-Z0-9_]+$', error='Username only allows alphanumeric characters and underscores'),
                        validate.Length(min=6, max=20, error='Password must be between 6 and 20 characters long')])
    password = fields.Str(required=True, 
                        validate=[validate.Regexp('^[a-zA-Z0-9_]+$', error='Username only allows alphanumeric characters and underscores'),
                        validate.Length(min=6, max=20, error='Password must be between 6 and 20 characters long')])
    link_icon = fields.Str(required=True)

class ReviewSchema(Schema):
    id_user = fields.Int(required=True, validate=validate_non_negative)
    id_route = fields.Int(required=True, validate=validate_non_negative)
    star_vote = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True)

class AccountSchema(Schema):
    username = fields.Str(required=True, 
                        validate=[validate.Regexp('^[a-zA-Z0-9_]+$', error='Username only allows alphanumeric characters and underscores'),
                        validate.Length(min=6, max=20, error='Password must be between 6 and 20 characters long')])
    password = fields.Str(required=True, 
                        validate=[validate.Regexp('^[a-zA-Z0-9_]+$', error='Username only allows alphanumeric characters and underscores'),
                        validate.Length(min=6, max=20, error='Password must be between 6 and 20 characters long')])

class PasswordSchema(Schema):
    password = fields.Str(required=True, 
                        validate=[validate.Regexp('^[a-zA-Z0-9_]+$', error='Username only allows alphanumeric characters and underscores'),
                        validate.Length(min=6, max=20, error='Password must be between 6 and 20 characters long')])

class LinkIconSchema(Schema):
    link_icon = fields.Str(required=True)

class StatusUpdateSchema(Schema):
    status = fields.Bool(required=True)