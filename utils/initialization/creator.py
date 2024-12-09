import json
from utils.tools import time_now
from utils.initialization.initializtion import init_judge, init_updater
from utils.get_config import get_config, get_folder_project
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


def create_ttl_dataset(dataset):
    """
    Var
        dataset: str
            ex: "SST-5", "AGNnews"
    
    data path:
        dataset
            |- raw
            |   |- clean_json
            |       |- seed5
            |           |- dev_500.json
            |           |- dev.json
            |           |- test.json
            |       |- seed10
            |           |- ...
            |
            |- seed5_200
            |   |- seed5_200.json
            |- seed5_500
            |   |- seed5_500.json
            |- seed10_200
            |   |- ...
    """
    folder_project = get_folder_project()
    folder_dataset = folder_project / f"dataset/{dataset}"
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

def create_population_init(**kwargs):
    """
    Var
        population_raw: list
        path_dataset: dict
        task: str
    """

    path_dataset = kwargs["path_dataset"]
    judge = init_judge(path_dataset=path_dataset)
    def get_semi_pair(prompt, type_split, folder_trace, t):
        """ 取得 semi-pair
        """
        if DEBUGGER=="True": print("\tenter get_semi_pair")

        score, precision, ttl_data_confusing, ttl_data_wrong = judge.get_score_result(prompt, type_split)
        path_trace = folder_trace / f"{t}_{type_split}.json"
        semi_pair = {
            'prompt': prompt,
            f"{type_split}_score": score,
        }
        with open(path_trace, 'w', encoding='utf-8') as file:
            json.dump(semi_pair, file, indent=4)

        if DEBUGGER=="True": print("\texit get_semi_pair")
        return semi_pair, precision, ttl_data_confusing, ttl_data_wrong

    # 製作 prompt-scores pairs
    population_raw = kwargs["population_raw"]
    task = kwargs["task"]
    folder_project = get_folder_project()
    ttl_pair=[] # pop_init
    for idx, prompt in enumerate(population_raw):
        if DEBUGGER=="True": print(f"\t{idx=}\t{prompt=}")

        folder_trace = folder_project / f"prompt/population_init/{task}/p{idx}"
        folder_trace.mkdir(parents=True, exist_ok=True)
        t = time_now()

        pair = {
            "prompt": prompt,
            "train_score": None,
            "dev_score": None,
            "precision": {},
            "data_sick": {}
        }
        for split in ["train", "dev"]:
            semi_pair, precision, ttl_data_confusing, ttl_data_wrong = get_semi_pair(prompt, split, folder_trace, t)
            pair.update(semi_pair)
            pair["precision"][split] = precision
            pair["data_sick"][split] = {
                "confusing": ttl_data_confusing,
                "wrong": ttl_data_wrong
            }

        ttl_pair.append(pair)

    if DEBUGGER=="True": print("exit create_population_init")
    return ttl_pair

def create_population_contr(**kwargs):
    """ 製作 coevo 中的 p_contr
    Var
        path_population_init: str
        path_dataset: dict
    """

    path_population_init = kwargs["path_population_init"]

    path_dataset = kwargs["path_dataset"]
    judge = init_judge(path_dataset=path_dataset)
    print(f"creator\t\t{judge=}")

    type_updater = "contr"

    updater = init_updater(
        path_population=path_population_init,
        judge=judge,
        type_updater=type_updater
    )

    population_contr = updater.f()

    return population_contr
