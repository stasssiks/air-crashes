import os


def load_data(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    file_path = os.path.join(parent_dir + "/data/", filename)
    return file_path
