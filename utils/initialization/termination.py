
from utils.get_input.get_unique_input import (
    get_stop_score,
    get_num_new_prompt,
)
from utils.get_config import get_config, get_folder_project
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def get_ttl_termination(size_population: int) -> None:
    """ set termination condition
    """
    if DEBUGGER=="True": print("enter get_ttl_termination")

    # path_stop_file
    folder_project =  get_folder_project()
    path_stop_file = folder_project / 'stop_true.txt' # 人工 early stop 的檔案位置

    # stop_score
    stop_score = get_stop_score()

    # rest_iteration
    num_new_prompt = get_num_new_prompt()
    rest_iteration = num_new_prompt//size_population

    ttl_termination = {
        "path_stop_file": path_stop_file,
        "stop_score": stop_score,
        "rest_iteration": rest_iteration,
    }

    if DEBUGGER=="True": print("exit get_ttl_termination")
    return ttl_termination

class Termination:
    """ termination condition for population evolution
    """

    def __init__(self) -> None:
        if DEBUGGER=="True": print("\tenter Termination.__init__")

        self.__path_stop_file = None
        self.__stop_score = None
        self.__rest_iteration = None

        if DEBUGGER=="True": print("\texit Termination.__init__")

    def reset_condition(self, **kwargs):
        """ set termination condition
        Var
            path_stop_file: pathlib.Path
            stop_score: int
            rest_iteration: int
        """
        if DEBUGGER=="True": print("\tenter Termination.reset_condition")

        if "path_stop_file" in kwargs:
            self.__path_stop_file = kwargs["path_stop_file"]
        if "stop_score" in kwargs:
            self.__stop_score = kwargs["stop_score"]
        if "rest_iteration" in kwargs:
            self.__rest_iteration = kwargs["rest_iteration"]

        if DEBUGGER=="True": print("\texit Termination.reset_condition")

    def get_condition(self):
        """ indirectly get termination condition
        """
        if DEBUGGER=="True": print("\tenter Termination.get_condition")

        ttl_condition = {
            "path_stop_file": self.__path_stop_file,
            "stop_score": self.__stop_score,
            "rest_iteration": self.__rest_iteration,
        }

        if DEBUGGER=="True": print("\texit Termination.get_condition")
        return ttl_condition

    def check_stop_file(self):
        if DEBUGGER=="True": print("\t\tenter Termination.check_stop_file")

        is_exist_stop_file = self.__path_stop_file.exists()

        if DEBUGGER=="True": print("\t\texit Termination.check_stop_file")
        return is_exist_stop_file

    def check_rest_iteration(self):
        if DEBUGGER=="True": print("\t\tenter Termination.check_rest_iteration")

        is_enough_iteration = self.__rest_iteration==0

        if DEBUGGER=="True": print("\t\texit Termination.check_rest_iteration")
        return is_enough_iteration

    def check_stop_score(self, score):
        if DEBUGGER=="True": print("\t\tenter Termination.check_stop_score")

        is_enough_score = score>=self.__stop_score

        if DEBUGGER=="True": print("\t\texit Termination.check_stop_score")
        return is_enough_score

    def check(self, score):
        if DEBUGGER=="True": print("\tenter Termination.check")

        if self.check_stop_file():
            return True
        if self.check_rest_iteration():
            return True
        if self.check_stop_score(score):
            return True

        if DEBUGGER=="True": print("\texit Termination.check")
        return False

    def update(self):
        if DEBUGGER=="True": print("\tenter Termination.update")

        self.__rest_iteration -= 1

        if DEBUGGER=="True": print("\texit Termination.update")
