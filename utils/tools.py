""" other functions
"""

from datetime import datetime
from pathlib import Path
import pytz

from utils.get_config import get_config
CONFIG = get_config()
# DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
DEBUGGER = "False"    # 可以單獨關掉這個檔案的 DEBUGGER

def count_words(sentences):
    """
    Var
        sentences: List[str]
            raw document
    
    Return
        int: the number of words in thees sentences
    """
    if DEBUGGER=="True": print("enter count_words")

    count = 0
    for sentence in sentences:
        count += len(sentence.split(" "))

    if DEBUGGER=="True": print("exit count_words")
    return count

def prompt_in_list(ttl_pire_prompt_score, new_prompt):
    """
    Var
        ttl_pire_prompt_score: List[Dict]
            list of "{'prompt': prompt, 'score': score}"

        new_prompt: str
            the prompt to be check whether or not the in ttl_prompt
    """
    if DEBUGGER=="True": print("enter prompt_in_list")

    # 預設不在
    in_list = False
    # 然後檢查
    for pire in ttl_pire_prompt_score:
        if pire['prompt'] == new_prompt:
            in_list = True
            break

    if DEBUGGER=="True": print("exit prompt_in_list")
    return in_list

def time_now():
    """ 取得現在的時間，格式為 YYYY_MMDD_HHMM
    """
    if DEBUGGER=="True": print("enter time_now")

    # Define the timezone for Taiwan
    taiwan_tz = pytz.timezone('Asia/Taipei')

    # Get the current time in Taiwan timezone
    taiwan_time = datetime.now(taiwan_tz)

    time_formated = taiwan_time.strftime('%Y_%m%d_%H%M')

    if DEBUGGER=="True": print("exit time_now")
    return time_formated

def get_file_name(path):
    """ get the corpus name only
    """
    if DEBUGGER=="True": print("enter get_file_name")

    path = Path(path)
    file_name = path.stem

    if DEBUGGER=="True": print("exit get_file_name")
    return file_name

def list_direct_files(directory):
    """ 列出資料夾下所有直屬文件名。
    Var
        directory: str
            目標資料夾的路徑。

    Returns
        ttl_file: list
        ttl_dir: list
    """
    directory = Path(directory)
    try:
        # 使用 os.listdir 獲取資料夾中的所有項目
        ttl_item = list(directory.iterdir())
        # 過濾出文件項目
        ttl_file = [item for item in ttl_item if item.is_file()]
        ttl_file = sorted(ttl_file)
        ttl_dir = [item for item in ttl_item if item.is_dir()]
        ttl_dir = sorted(ttl_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
        ttl_file = []
        ttl_dir = []
    return ttl_file, ttl_dir

def get_unique_file(directory):
    """ 取得 "唯一" 的文件名
    """
    if DEBUGGER=="True": print("enter get_unique_file")

    ttl_file, ttl_dir = list_direct_files(directory)
    if ttl_dir != [] or len(ttl_file) > 1:
        raise ValueError(f"directory {directory} has more than one file")

    if len(ttl_file) == 0:
        raise FileNotFoundError(f"directory {directory} has no file")

    path = ttl_file[0]

    if DEBUGGER=="True": print("exit get_unique_file")
    return path
