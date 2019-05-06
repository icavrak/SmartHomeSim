import json


class Load:
    json_data = {}

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.read_json()

    def read_json(self):
        with open('el_loads.json') as loads:
            self.json_data = json.load(loads)

    def get_consumption(self):
        for type_of_load in self.json_data['loads']:
            if type_of_load['name'] == self.name:
                for types in type_of_load['types']:
                    if types['name'] == self.type:
                        return types['consumption']
        return None


if __name__ == '__main__':
    l = Load('bulb', 'halogen')
    print(l.get_consumption())