"""
User model structure
"""

from cerberus import Validator

class User:
    """
    User model structure
    """
    def __init__(self):
        pass

    def add(self, user):

        schema = {'name': {'type': 'string'}, 'username': {'type': 'string'}, 'password': {'type': 'string'}}

        v = Validator(schema)
        v.allow_unknown = True

        if v.validate(user, schema):
            self.name = user['name'].strip()
            self.username = user['username'].strip()
            self.password = user['password'].strip()
            return(True)
        return(v.errors)
