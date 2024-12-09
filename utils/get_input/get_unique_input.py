""" get user input (only once)
"""

from functools import wraps
from utils.get_config import get_config, get_folder_project
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

# get_unique_input

def get_unique_input(hint:str, message_retry=""):
    """ Decorator Factory for 讀取使用者指定的變數
    """
    def decorator(func_check=int):
        @wraps(func_check)
        def wrapper(**kwargs):
            if DEBUGGER=="True": print("enter get_unique_input")
            nonlocal hint  # 告訴 Python 不要創建新的局部變量，因為下面有賦值所以會混淆
            while True:
                if "hint2" in kwargs:
                    hint += kwargs["hint2"]
                var = input(hint)
                var = var.strip()
                try:
                    var = func_check(var)
                    if DEBUGGER=="True": print("exit get_unique_input")
                    return var
                except ValueError as e:
                    print(message_retry)
                    print(e)
        return wrapper
    return decorator

# # determinant condition

@get_unique_input(
        hint="type_evaluator: ",
        message_retry="錯誤"
)
def get_type_evaluator(var):
    """ get num_new_prompt
    """
    if DEBUGGER=="True": print("\tenter get_type_evaluator")
    ttl_type_evaluator = ["EvoDE", "EvoGA", "CoEvo", "ReSS", "contr"]
    string_in_error = "\n".join(ttl_type_evaluator)

    if var not in ttl_type_evaluator:
        raise ValueError(f"Got {var}, but only following are allowed:\n{string_in_error}")

    if DEBUGGER=="True": print("\texit get_type_evaluator")
    return var

@get_unique_input(
        hint="stop_score (練蠱終止條件，即train_score目標分數): ",
        message_retry="stop_score 必須是整數"
)
def get_stop_score(var):
    """ get stop_score
    """
    if DEBUGGER=="True": print("\tenter get_stop_score")
    if DEBUGGER=="True": print("\texit get_stop_score")
    return int(var)

@get_unique_input(
        hint="num_new_prompt (必須是 prompt_population 的倍數): ",
        message_retry="num_new_prompt 必須是 prompt_population 的倍數"
)
def get_num_new_prompt(var):
    """ get num_new_prompt
    """
    if DEBUGGER=="True": print("\tenter get_num_new_prompt")
    if DEBUGGER=="True": print("\texit get_num_new_prompt")
    return int(var)


# # experiment setting
@get_unique_input(
        hint="num_experiment (實驗次數): ",
        message_retry="num_experiment 必須是整數"
)
def get_num_experiment(var):
    """ get num_experiment
    """
    if DEBUGGER=="True": print("\tenter get_num_experiment")
    if DEBUGGER=="True": print("\texit get_num_experiment")
    return int(var)

@get_unique_input(
        hint="name_experiment (絕對路徑 or Ress/record/ 之後的路徑): ",
        message_retry="name_experiment 格式錯誤"
)
def get_folder_experiment(var):
    """ get folder_experiment
    """
    if DEBUGGER=="True": print("\tenter get_folder_experiment")

    folder_project = get_folder_project()
    folder_record = folder_project / "record"

    folder_experiment = folder_record / var
    
    if DEBUGGER=="True": print("\texit get_folder_experiment")
    return folder_experiment

@get_unique_input(
        hint="type_embedding from kwargs of from population? (kwargs/population/N)",
        message_retry="再選一次"
)
def get_type_embedding(var):
    """ get type_embedding
    """
    if DEBUGGER=="True": print("\tenter get_type_embedding")

    if var=="N":
        raise KeyboardInterrupt("ambiguous on type_embedding")

    if DEBUGGER=="True": print("\texit get_type_embedding")
    return var
