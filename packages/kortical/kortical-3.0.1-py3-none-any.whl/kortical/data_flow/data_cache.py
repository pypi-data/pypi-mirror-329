import os
import pickle
import shutil
from . import helpers


class DataCache(object):

    def __init__(self, directory):
        self.directory = directory

    def _get_hash_dir(self, hash_value):
        # Some characters are not valid in windows file paths, so list them here and swap them for their ascii equivlanet
        unsafe_characters = [
            '<',
            '>',
            ':',
            '"',
            "'",
            '/',
            '\\',
            '|',
            '?',
            '!',
            '$',
            '%',
            '&',
            '#',
            '*',
            '=',
            '{',
            '}',
            '@',
        ]
        for char in unsafe_characters:
            hash_value = hash_value.replace(char, f"{ord(char)}")
        return os.path.join(self.directory, hash_value)

    def _get_data_names(self, hash_dir):
        return [os.path.splitext(x)[0] for x in os.listdir(hash_dir)]

    def replace_and_store(self, old_hash_value, hash_value, data):
        if old_hash_value:
            hash_dir = self._get_hash_dir(old_hash_value)
            shutil.rmtree(hash_dir)
        self.store(hash_value, data)

    def store(self, hash_value, data):
        hash_dir = self._get_hash_dir(hash_value)
        if os.path.isdir(hash_dir):
            return
        helpers.create_directory(hash_dir)
        if data:
            for k, v in data.items():
                file_path = os.path.join(hash_dir, f'{k}.bin')
                with open(file_path, 'wb') as f:
                    pickle.dump(v, f, protocol=-1)

    def fetch(self, hash_value):
        hash_dir = self._get_hash_dir(hash_value)
        if not os.path.isdir(hash_dir):
            return None
        data_names = self._get_data_names(hash_dir)
        data = {}
        for n in data_names:
            file_path = os.path.join(hash_dir, f'{n}.bin')
            with open(file_path, 'rb') as f:
                data[n] = pickle.load(f)
        return data
