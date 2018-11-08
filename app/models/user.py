"""User model structure"""

class User:
    """User model structure"""
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
