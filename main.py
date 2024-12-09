import json
from utils.tools import time_now
from utils.initialization.termination import get_ttl_termination, Termination
from utils.initialization.initializtion import init_judge, init_updater
from utils.initialization.creator import create_population_contr, create_population_init
from utils.get_config import get_folder_project


def for_pop_init(task):
    folder_project = get_folder_project()
    path_population_raw = folder_project / f"prompt/raw/{task}/generate/prompts.json"
    with open(path_population_raw, 'r', encoding='utf-8') as file:
        population_raw = json.load(file)

    path_dataset = folder_project / f"dataset/{task}/seed5_200/seed5_200.json"

    ttl_pair = create_population_init(
        population_raw=population_raw,
        path_dataset=path_dataset,
        task=task
    )
    folder_pop_init = folder_project / f"prompt/population_init/{task}/generate/seed5_200/"
    folder_pop_init.mkdir(parents=True, exist_ok=True)
    path_pop_init = folder_pop_init / "seed5_200.json"
    with open(path_pop_init, 'w', encoding='utf-8') as file:
        json.dump(ttl_pair, file, indent=4)

def for_pop_contr(task):
    folder_project = get_folder_project()
    path_population_init = folder_project / f"prompt/population_init/{task}/generate/seed5_200/seed5_200.json"
    path_dataset = folder_project / f"dataset/{task}/seed5_200/seed5_200.json"

    population_contr = create_population_contr(
        path_population_init=path_population_init,
        path_dataset=path_dataset
    )

    folder_population_contr = folder_project / f"prompt/contr/{task}/raw/generate"
    folder_seed = folder_population_contr / "seed5_200"
    folder_seed.mkdir(parents=True, exist_ok=True)
    path_populaiton_contr = folder_seed / "seed5_200.json"
    with open(path_populaiton_contr, 'w', encoding='utf-8') as file:
        json.dump(population_contr, file, indent=4)

def init_experiment(task, type_updater):
    # get updater
    folder_project = get_folder_project()
    path_population_init = folder_project / f"prompt/population_init/{task}/test.json"
    path_population_contr = folder_project / f"prompt/contr/{task}/test.json"
    path_dataset = folder_project / f"dataset/{task}/seed5_200/seed5_200.json"
    judge = init_judge(path_dataset=path_dataset)
    print(f"creator\t\t{judge=}")

    updater = init_updater(
        path_population=path_population_init,
        judge=judge,
        type_updater=type_updater,
        path_population_contr=path_population_contr
    )

    return updater

def run_experiment(task, updater, termination, folder_experiment):

    folder_experiment.mkdir(parents=True, exist_ok=True)

    condition_init = termination.get_condition()
    ttl_iteration = condition_init["rest_iteration"]

    population = updater.get_population()
    p_best = population[0]
    score_best = p_best["train_score"]

    # do until
    population = updater.get_population()
    record = {
        "corpus": f"{task}/seed5_200",
        "type_llm": "Breeze-7B-32k-Instruct-v1_0",
        "type_embedding": "bgem3",
        "best_promt": population[0],
        "prompt_popularion": population
    }
    condition_now = termination.get_condition()
    rest_iteration = condition_now["rest_iteration"]
    num_iteration = 0
    t = time_now()
    path_record = folder_experiment / f"{num_iteration:>03d}_{t}.json"
    with open(path_record, 'w', encoding='utf-8') as file:
        json.dump(record, file, indent=4)
    while not termination.check(score_best):
        new_population = updater.f()
        record = {
            "corpus": f"{task}/seed5_200",
            "type_llm": "Breeze-7B-32k-Instruct-v1_0",
            "type_embedding": "bgem3",
            "best_promt": new_population[0],
            "prompt_popularion": new_population
        }

        condition_now = termination.get_condition()
        rest_iteration = condition_now["rest_iteration"]
        
        num_iteration = ttl_iteration - rest_iteration + 1
        t = time_now()
        path_record = folder_experiment / f"{num_iteration:>03d}_{t}.json"
        with open(path_record, 'w', encoding='utf-8') as file:
            json.dump(record, file, indent=4)

        termination.update()

def single_experiment(task, type_updater, t, termination):
    updater = init_experiment(task, type_updater)

    folder_project = get_folder_project()
    folder_experiment = folder_project / f"record/experiment_test/{t}"

    folder_experiment_coevo = folder_experiment / type_updater
    run_experiment(task, updater, termination, folder_experiment_coevo)

def main_experiment(task, ttl_type_updater):
    updater = init_experiment(task, "CoEvo")
    # get termination
    size_population = updater.size_population
    ttl_termination = get_ttl_termination(size_population)
    
    termination = Termination()
    t = time_now()
    for type_updater in ttl_type_updater:
        termination.reset_condition(**ttl_termination)
        single_experiment(task, type_updater, t, termination)

def main_init(ttl_task):
    for task in ttl_task:
        for_pop_init(task)
        for_pop_contr(task)

if __name__=="__main__":
    # for_pop_init("TREC")
    # for_pop_contr("TREC")
    # main_init(["CR"])
    main_experiment("MR", ["EvoDE", "CoEvo2"])
