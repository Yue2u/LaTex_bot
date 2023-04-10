import json
import os
from utils import path_join, create_folder, basement


def get_current_dir():
    return os.getcwd()


def get_project_config(path):
    full_path = path_join(get_current_dir(), path)
    create_folder(basement(full_path))

    if not os.path.exists(full_path):
        return None

    with open(full_path, "r") as f:
        return json.loads(f.read())


def write_project_config(path, cfg):
    full_path = path_join(get_current_dir(), path)
    create_folder(basement(full_path))

    if not os.path.exists(full_path):
        return None

    with open(full_path, "w") as f:
        json.dump(cfg, f)


def init_project_config(path):
    cfg = json.loads('{"font_size": 12, "indent": 20}')

    full_path = path_join(get_current_dir(), path)
    create_folder(basement(full_path))

    with open(full_path, "w") as f:
        json.dump(cfg, f, indent=4)


def set_font_size(path, font_type):
    font_sizes = {"small": 10, "medium": 12, "large": 14}
    cfg = get_project_config(path)

    if cfg is None:
        raise ValueError("Wrong config path: " + f"{path}")
    if font_type not in font_sizes:
        raise ValueError("Wrong font size")

    cfg["font_size"] = font_sizes[font_type]
    write_project_config(path, cfg)


def set_indent_size(path, indent):  # indent in mm
    cfg = get_project_config(path)

    if cfg is None:
        raise ValueError("Wrong config path: " + f"{path}")
    if indent < 0:
        raise ValueError("Indent can not be less than 0")

    cfg["indent"] = indent
    write_project_config(path, cfg)
