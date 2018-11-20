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

        schema = {'userid': {'type': 'integer'}, 'name': {'type': 'string'},
                  'username': {'type': 'string'}, 'password': {'type': 'string'},
                   'role': {'type': 'string'}}

        v = Validator(schema)
        v.allow_unknown = True

        if v.validate(user, schema):
            self.userid = user['userid']
            self.name = user['name'].strip()
            self.username = user['username'].strip()
            self.password = user['password'].strip()
            self.role = user['role'].strip()
            return(True)
        return(v.errors)
