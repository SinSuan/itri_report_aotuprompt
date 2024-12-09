"""
這個檔案目前沒有用到，但 data preprocess 時會用到 data_format
"""

import json
from pathlib import Path

# import random
# from utils.call_model.encoder import Encoder
# from utils.call_model.llm import CallTGI
# from utils.score import get_score

from utils.get_config import get_config, get_folder_project
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

# Read data from path
def get_data(path):
    if DEBUGGER=="True": print("enter get_data")

    with open(path,"r",encoding="utf-8")as file:
        data=json.load(file)

    if DEBUGGER=="True": print("exit get_data")
    return data

# format universal data format
def data_format(content,question,answer):
    if DEBUGGER=="True": print("enter data_format")
    
    return_format={
        "content":content,
        "question":question,
        "answer":answer
    }
    
    if DEBUGGER=="True": print("exit data_format")
    return return_format

# def init_setting(host_llm: str, type_embedding: str, path_data: str, path_prompt: str):
#     """
#     Var
#         all are string

#     Return
#         ttl_model: (llm, embedding_model)
#             llm: function
#             embedding_model: Encoder in utils.call_model.embedding
#     """

#     # 指定 llm
#     llm = CallTGI(host_llm)

#     # 指定 embedding model
#     if type_embedding is None:
#         embedding_model = None
#     else:
#         embedding_model = Encoder(type_embedding)

#     ttl_model = (llm, embedding_model)

#     # 指定訓練資料
#     num_training_data = 180
#     with open(path_data,  'r', encoding='utf-8') as file:
#         data = json.load(file)
#     # training_data=data[-num_training_data:]
#     dataset = random.sample(data, num_training_data)
#     train_split = dataset[:150]
#     dev_split = dataset[150:]
#     ttl_dataset = {
#         "train_split": train_split,
#         "dev_split": dev_split,
#     }

#     # 指定起始的 prompt
#     with open(path_prompt,  'r') as file:
#         ttl_prompt = json.load(file)

#     # 製作 prompt-scores pairs
#     ttl_prompt_scores=[]
#     for prompt in ttl_prompt:
#         # print(len(train_split))
#         # print(len(dev_split))
#         train_score = get_score(ttl_model, prompt, train_split, 3000, 10)
#         dev_score = get_score(ttl_model, prompt, dev_split, 3000, 10)
#         prompt_scores = {
#             'prompt': prompt,
#             'train_score': train_score,
#             'dev_score': dev_score
#         }
#         ttl_prompt_scores.append(prompt_scores)

#     return ttl_model, ttl_dataset, ttl_prompt_scores

def get_dataset(dataset):
    """
    Var
        dataset: str
            ex: "SST-5", "AGNnews"
    """
    folder_project = get_folder_project()
    folder_dataset = Path(f"/user_data/intern/new_branch/newnew/Ress/dataset/{dataset}")
    for idx_seed in [5,10,15]:
        folder_seed = folder_dataset / f"raw/clean_json/seed{idx_seed}"
        path_file_test = folder_seed / "test.json"
        with open(path_file_test, "r", encoding="utf-8") as f:
            file_test = json.load(f)

        for num_data in [200,500]:
            is500 = "_500" if num_data == 500 else ""
            name_file_dev = f"dev{is500}.json"
            path_file_dev = folder_seed / name_file_dev
            with open(path_file_dev, "r", encoding="utf-8") as f:
                file_dev = json.load(f)
            
            data = {"train_split": file_dev, "dev_split": file_test}
            folder_data = folder_dataset / f"seed{idx_seed}_{num_data}/"
            folder_data.mkdir(parents=True, exist_ok=True)
            path_data = folder_data / f"seed{idx_seed}_{num_data}.json"
            with open(path_data, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
