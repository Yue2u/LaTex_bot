import os
import json
import shutil


def path_join(*args):
    """Joins path with system separator"""
    return os.sep.join([str(arg) for arg in args])


def get_ext(filename):
    """Returns extension of file"""
    return filename.rsplit(".", 1)[-1]


def files_in_dir(path):
    """Return amount of files in 'path' folder"""
    return len([name for name in os.listdir(path)])


def create_folder(path):
    """Creates new folder/file if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)


def recreate_folder(path):
    """Deletes folder if exists and creates it empty"""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def basement(path):
    """Return basement of path (cut last element)"""
    return path.rsplit(os.sep, 1)[0]


def list_projects(path):
    """List all projects folders except tmp"""
    if not os.path.exists(path):
        return []
    return [folder for folder in os.listdir(path) if folder != "tmp"]


def dumps_message(message):
    """Returns meesage converted to json string"""
    msg = json.loads(str(message))
    return json.dumps(msg, indent=4)