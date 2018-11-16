"""
User model structure
"""

class User:
    """
    User model structure
    """
    def __init__(self, user):
        self.userid = user['userid']
        self.name = user['name']
        self.username = user['username']
        self.password = user['password']
        self.role = user['role']

    def serialize(self):
        return {'userid':self.userid, 'name':self.name, 'username':self.username, 'password':self.password, 'role':self.role}
