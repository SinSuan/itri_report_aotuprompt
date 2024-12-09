import configparser
from pathlib import Path
import sys

def get_folder_project():
    """ 幾乎每個 function 都要用到 PATH_PROJECT，所以寫成一個 function
    """

    path = None
    for path in sys.path:   # 為了讓 .ipynb 也可以用所以要這樣寫
        path = Path(path)
        if path.name == "itri":
            break

    return path

def get_config(path_config=None):
    """ 幾乎每個 function 都要用到 config.ini，所以寫成一個 function
    """

    if path_config is None:
        path = get_folder_project()
        path_config = path / "config.ini"

    config = configparser.ConfigParser()
    config.read(path_config)

    return config
