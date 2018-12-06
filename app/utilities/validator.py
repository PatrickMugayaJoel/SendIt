

class Validator:
    """ Data validation methods """

    def __init__(self):
        """ class variables """

        self.__invalid_data_messages = list()
        self.__schemaa = list()

    def schema(self, schem):
        """
        setting a schema to compare the data against
        [{'key':'value', 'type':'value', 'min_length':'value', 'max_length':'value', 'not_null':True}]
        types => integer, string, email
        """
        self.__schemaa = schem
    
    def __worker(self):
        """ Seperating data types """

        for item in self.__schemaa:

            if self.data.get(item['key']):
                item.update(value = self.data[item['key'].strip()])
            else:
                self.__invalid_data_messages.append(item['key']+" is required.")
                item.clear()
            
            if item.get('type'):

                if item['type'] == 'string':
                    self.__is_valid_string(item)

                if item['type'] == 'integer':
                    self.__is_valid_integer(item)

            if item.get('not_null'):
                if item['not_null'] == True:
                    self.__is_not_null(item)

            if item.get('min_length'):
                if isinstance(item['min_length'], int):
                    self.__is_min_length(item)

    def __is_valid_string(self, item):
        """ Validating if is a strings """

        if not isinstance(item['value'], str):
            self.__invalid_data_messages.append(item['key']+" must be a string.")

    def __is_valid_integer(self, item):
        """ Validating if is an integet """

        if not isinstance(item['value'], int):
            self.__invalid_data_messages.append(item['key']+" must be an integer.")

    def __is_min_length(self, item):
        """ Validating if is correct min length """

        if not len(item['value'])>(item['min_length']-1):
            self.__invalid_data_messages.append(item['key']+" must be at least "+str(item['min_length'])+" characters long.")

    def __is_not_null(self, item):
        """ Validating if not null """

        if not isinstance(item['value'], str):
            item['value'] = str(item['value'])

        if not len(item['value'])>0:
            self.__invalid_data_messages.append(item['key']+" can not be empty.")
    
    def validate(self, data):
        """ setting data and calling validating methods """

        self.data = data
        self.__worker()

        if self.__invalid_data_messages:
            return({'status':False, 'message':self.__invalid_data_messages})
        else:
            return({'status':True, 'message':'successfully validated'})

        self.__invalid_data_messages.clear()

# if __name__ == '__main__':
#     validator = Validator()
#     user = {'name':1, 'username':'Jos','password':'','age':'5'}
#     schema = [{'key':'name', 'type':'string', 'not_null':True}, {'key':'username', 'type':'string', 'min_length':4, 'not_null':True}, {'key':'age', 'type':'integer', 'not_null':True}, {'key':'password', 'not_null':True}]
#     validator.schema(schema)
#     print(validator.validate(user))
