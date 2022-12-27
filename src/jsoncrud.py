import json
from pathlib import Path


class JsonCrud:
    """json handler"""

    def __init__(self, filename, keys):
        self._filename = Path(filename).absolute()
        self._keys = keys
        self._dictionary = {}

        if not self._filename.is_file():
            self.create_dict()
            self.create_file(self._filename, self._dictionary)
        else:
            self._dictionary = self.json_to_dict(self._filename)

    def json_to_dict(self, filename):
        """open a json and place its content to a dict"""
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def create_dict(self):
        """create a dict with keys and null values"""
        for key in self._keys:
            self._dictionary[key] = str(Path.home().absolute())

    def open(self):
        """open a file in reading"""

    def create_file(self, filename, _dict):
        """create json file"""

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(_dict, file)

    def create_key(self):
        """create a key/value pair"""

    def read_key(self, key):
        """retrieve a value from a key"""

        return self._dictionary[key]

    def update_key(self, key, value):
        """update a value from a key"""

        self._dictionary[key] = value
        self.refresh_file()

    def refresh_file(self):
        """resave file"""
        with open(self._filename, 'w', encoding='utf-8') as file:
            json.dump(self._dictionary, file)

    def delete_key(self, key):
        """delete a key (and its value)"""
