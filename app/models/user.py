
from app.utilities.validator import Validator

class User:
    """ User model structure """

    def add(self, user):

        validator = Validator()
        validator.schema([
                            {'key':'name', 'type':'string', 'min_length':3, 'not_null':True},
                            {'key':'username', 'type':'string', 'min_length':3, 'not_null':True},
                            {'key':'password', 'not_null':True}
                        ])
        result = validator.validate(user)

        if result['status']:
            self.name = user['name'].strip()
            self.username = user['username'].strip()
            self.password = user['password'].strip()
            return(True)
        return(result)

