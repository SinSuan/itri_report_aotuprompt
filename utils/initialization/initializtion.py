import json

from utils.method_update.evo_prompt import CoEvo, CoEvo2, EvoDE, EvoGA, EvoGA4Contr
from utils.get_score.judge_cls import JudgeAGNnews, JudgeCR, JudgeMR, JudgeSST2, JudgeSST5, JudgeSubj, JudgeTREC
from utils.ttl_prompt.prompt_4_deal_task import Prompt4DealTask
from utils.call_model.llm import CallTGI

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

# def init_llm(host, headers=None):
#     llm = CallTGI(host, headers)
#     return llm

# def init_prompter(type_dataset, model="alpaca"):
#     prompter = Prompt4DealTask(
#         type_dataset=type_dataset,
#         model=model
#     )
#     return prompter

def init_judge(**kwargs):
    """
    Var
        llm: utils.call_model.llm.CallTGI       (optional)
        path_dataset: str                       (optional)
        type_dataset: str                       (optional)
    """
    if DEBUGGER=="True": print("enter init_judge")

    llm = kwargs.pop("llm", None)
    if llm is None:
        # host = input("judge, llm_host: ")
        # llm = CallTGI(host)
        llm = CallTGI()

    path_dataset = kwargs.pop("path_dataset", None)
    if path_dataset is None:
        path_dataset = input("judge, path_dataset: ")
    with open(path_dataset, "r", encoding='utf-8') as f:
        dataset = json.load(f)

    type_dataset = kwargs.pop("type_dataset", None)
    if type_dataset is None:
        path_dataset = str(path_dataset)
        type_dataset = path_dataset.split("/dataset/")[1].split("/")[0]
    prompter = Prompt4DealTask(
        type_dataset=type_dataset,
        type_model="alpaca"
    )
    switch_judge = {
        "AGNews": JudgeAGNnews,
        "CR": JudgeCR,
        "SST-2": JudgeSST2,
        "SST-5": JudgeSST5,
        "MR": JudgeMR,
        "Subj": JudgeSubj,
        "TREC": JudgeTREC
    }
    class_judge = switch_judge[type_dataset]

    judge = class_judge(
        llm=llm,
        prompter=prompter,
        dataset=dataset
    )

    if DEBUGGER=="True": print("exit init_judge")
    return judge

def init_updater(**kwargs):
    """
    Var
        llm: utils.call_model.llm.CallTGI                               (optional)
        path_population: str                                            (optional)
        judge: utils.get_score.judge_abstract.JudgeAbstract             (optional)
        type_updater: str                                               (optional)
        prompter: utils.ttl_prompt.prompt_4_deal_task.Prompt4DealTask   (optional)
        path_dataset
    """
    if DEBUGGER=="True": print("enter init_updater")

    llm = kwargs.pop("llm", None)
    if llm is None:
        # host = input("updater, llm_host: ")
        # llm = CallTGI(host)
        llm = CallTGI()

    path_population = kwargs.pop("path_population", None)
    if path_population is None:
        path_population = input("updater, path_population: ")
    with open(path_population, "r", encoding='utf-8') as f:
        population = json.load(f)
    
    path_population_contr = kwargs.pop("path_population_contr", None)
    population_contr = None
    if path_population_contr is not None:
        with open(path_population_contr, "r", encoding='utf-8') as f:
            population_contr = json.load(f)

    judge = kwargs.pop("judge", None)
    print(f"init_updater\t{judge=}")
    if judge is None:
        path_dataset = kwargs.pop("path_dataset", None)
        task = kwargs.pop("task", None)
        judge = init_judge(
            llm=llm,
            path_dataset=path_dataset,
            task=task
        )

    type_updater = kwargs.pop("type_updater", None)
    if type_updater is None:
        type_updater = input("updater, type_updater: ")
    switch_updater = {
        "EvoDE": EvoDE,
        "EvoGA": EvoGA,
        "CoEvo": CoEvo,
        "CoEvo2": CoEvo2,
        "contr": EvoGA4Contr
    }
    class_updater = switch_updater[type_updater]
    kwargs_4_updater = {
        "llm": llm,
        "population": population,
        "judge": judge,
        "population_contr": population_contr,
    }

    prompter = kwargs.pop("prompter", None)
    if prompter is not None:
        kwargs_4_updater["prompter"] = prompter

    updater = class_updater(**kwargs_4_updater)

    if DEBUGGER=="True": print("exit init_updater")
    return updater
