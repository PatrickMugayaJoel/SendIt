
class Validator:
    """ Data validation methods """

    def __init__(self):
        """ class variables """
        self.invalid_data_messages = list()
        self.strings = list()
        self.integers = list()
        self.schemaa = list()

    def schema(self, schem):
        """
        setting a schema to compare the data against
        [{'key':'value', 'type':'value', 'min_length':'value'}]
        types => integer, string, email
        """
        self.schemaa = schem
    
    def separate_datatypes(self):
        """ Seperating data types """
        for item in self.schemaa:

            item.update(value = self.data[item['key']])
            
            if item['type'] == 'string':
                self.strings.append(item)

            if item['type'] == 'integer':
                self.integers.append(item)

    def is_valid_string(self):
        """ Validating strings """

        for string in self.strings:

            if not isinstance(string['value'], str):
                self.invalid_data_messages.append(string['key']+" must be a string.")

            if isinstance(string['value'], str) and not len(string['value'])>0:
                self.invalid_data_messages.append(string['key']+" can not be empty.")
    
    def validate(self, data):
        """ setting data and calling validating methods """
        self.data = data
        self.separate_datatypes()
        self.is_valid_string()

        if self.invalid_data_messages:
            print({'message':self.invalid_data_messages, 'status':False})
        else:
            print({'message':'successfully validated', 'status':True})

        self.invalid_data_messages.clear()

if __name__ == '__main__':
    validator = Validator()
    user = {'name':'Joel', 'username':'Josean','password':'password'}
    schema = [{'key':'name', 'type':'string'}, {'key':'username', 'type':'string', 'min_length':4}]
    validator.schema(schema)
    validator.validate(user)
