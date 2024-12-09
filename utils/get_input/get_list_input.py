""" user can input a list of input squentially until "end"
"""

from functools import wraps
from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def get_list_input(type_input):
    """ decorator to get list of input
    Var
        type_input: str
            ex: "host", "type_dataset", ...
    """
    def decorator(check_func):
        """ decorator to get list of input
        Var
            check_func: function
                check if the input is valid
        """
        @wraps(check_func)
        def wrapper():
            """ get list of input
            """
            if DEBUGGER=="True": print(f"\tenter get_list_input({type_input})")

            ttl_input = []
            num_input = 0
            while True:
                hint = f"""{type_input} {num_input} ("end" for no more input): """
                input_ = input(hint)
                input_ = input_.strip()

                # terminating condition
                if input_=="end":
                    break

                # check if the input is valid
                is_error, error_message = check_func(input_)
                if is_error:                # invalid: 「重複」以外的錯誤
                    print(error_message)

                elif input_ in ttl_input:   # invalid: 重複
                    print(f"\t{input_} is already in list")

                else:                       # valid
                    ttl_input.append(input_)
                    num_input += 1

            if DEBUGGER=="True": print(f"\texit get_list_input({type_input})")
            return ttl_input
        return wrapper
    return decorator

@get_list_input("host")
def get_ttl_host(input_):
    """ get ttl_host for tgi of llm
    """
    is_error = False
    massage = input_

    if "http://" not in input_:
        is_error = True
        massage = "wrong url"

    return is_error, massage

@get_list_input("type_dataset")
def get_ttl_type_dataset(input_):
    """ no other extra check
    """
    is_error = False
    massage = input_

    return is_error, massage

@get_list_input("type_pop_init")
def get_ttl_pop_init(input_):
    """ no other extra check
    """
    is_error = False
    massage = input_

    return is_error, massage
