import json
import os


FIXTURES_DIR_NAME = 'fixtures'


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, FIXTURES_DIR_NAME, file_name)


def read(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def get_fixture_data(file_name):
    content = read(get_fixture_path(file_name))
    return json.loads(content)


def get_test_data(file_name):
    return get_fixture_data(file_name)
