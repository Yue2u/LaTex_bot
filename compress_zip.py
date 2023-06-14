import os
import zipfile
from create_bot import USER_DATA
from utils import path_join


def make_zip(uid, pr_name):
    zip_path = path_join(USER_DATA, uid, pr_name, pr_name + ".zip")
    project_path = path_join(USER_DATA, uid, pr_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Iterate over all the files in the folder
        for root, dirs, files in os.walk(path_join(project_path, "sections")):
            for file in files:
                # Get the absolute path of the file
                file_path = os.path.join(root, file)
                # Get the relative path of the file with respect to the folder
                relative_path = os.path.relpath(file_path, project_path)
                # Add the file to the zip file using the relative path
                zipf.write(file_path, arcname=relative_path)
        zipf.write(path_join(project_path, pr_name + ".tex"), arcname=f"{pr_name}.tex")
    return zip_path
