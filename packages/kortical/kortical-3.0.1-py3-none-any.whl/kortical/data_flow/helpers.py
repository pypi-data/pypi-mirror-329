import os


def create_directory(dir):
    if not os.path.exists(dir):
        print(dir, 'does not exist, creating it')
        os.makedirs(dir)