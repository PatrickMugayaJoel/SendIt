"""
User model structure
"""

class User:
    """
    User model structure
    """
    def __init__(self):
        pass

    def add(self, user):

        if isinstance(user['name'], str) and isinstance(user['username'], str):
            self.name = user['name'].strip()
            self.username = user['username'].strip()
            self.password = user['password'].strip()
            return(True)
        return({'msg':"Name and Username must be strings","status":"failed"})

