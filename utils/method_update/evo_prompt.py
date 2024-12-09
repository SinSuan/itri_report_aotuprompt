""" all versions of Updater
"""

from copy import deepcopy
import numpy as np
from utils.method_update.population_updater import Updater
from utils.ttl_prompt.template.evolution import TEMPLATE_EVOLUTION
from utils.ttl_prompt.simple import PromptSimple

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


class EvoPrompt(Updater):
    """ abstract base class
    
    still required to implement:

        def sample_prompt(self, i=None) -> tuple[list]:
            ""
            Var
                i: int
                    用來 sample prompt 的 index

            Return
                ttl_name: list[str]
                    prompt 的名字

                ttl_pair: list[dict]
                    dict formation:
                    {
                        "prompt": str,
                        "train_score": float,
                        "dev_score": float
                    }
            ""

        def update(self, new_population) -> None:
            "" 更新 self.population
            ""
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def f(self):
        """ main function of this class
        """
        if DEBUGGER=="True": print("\tenter EvoPrompt.f")

        new_population = []
        for i in range(self.size_population):
            ttl_pair = self.sample_prompt(i)

            # evolution
            try:
                ttl_prompt = [ pair["prompt"] for pair in ttl_pair ]
                kwargs_4_prompter = dict(zip(self.ttl_key, ttl_prompt))
            except Exception as e:
                print(f"{ttl_pair=}")
                raise ValueError("ttl_pair should be list of dict") from e
            prompt_4_create_new_os_prompt = self.prompter.create_prompt(**kwargs_4_prompter)

            for_debug = deepcopy(kwargs_4_prompter)
            new_prompt = self.get_distinct_new_propmt(new_population+self.get_population(), prompt_4_create_new_os_prompt, **for_debug)

            print(f"\nnew_prompt\n{new_prompt}")
            for key, value in kwargs_4_prompter.items():
                print(f"{key}\n{value}")

            # record
            prompt_score = self.evaluate(new_prompt)
            info = {
                type_prompt: self.formulate_pair(pair)
                for type_prompt, pair in zip(self.ttl_key, ttl_pair)
            }
            prompt_score["info"] = info
            new_population.append(prompt_score)

        self.update(new_population)

        population_return = self.get_population()

        # 確保 population 只有 prompt 跟 *_score
        population_formulate = self.formulate_population(self.population)
        self.set_population(population_formulate)

        if DEBUGGER=="True": print("\texit EvoPrompt.f")
        return population_return

class EvoDE(EvoPrompt):
    """ Differential Evolution
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.prompter is None:
            template = TEMPLATE_EVOLUTION["EvoPrompt"]["English"]["EvoDE"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

    def sample_prompt(self, i=None):
        """ outupt 要按照 template 的順序
        """
        pair_best = self.population[0]
        pair_i = self.population[i]

        remaining_pairs = [pair for pair in self.population if pair['prompt'] != pair_i['prompt']]
        pair_1, pair_2 = np.random.choice(remaining_pairs, size=2, replace=False)

        ttl_pair = [pair_1, pair_2, pair_best, pair_i]

        return ttl_pair

    def update(self, new_population):
        """ 兩個 population 對應比較，取 train_score 高者
        """
        for i in range(self.size_population):
            if new_population[i]["train_score"] > self.population[i]["train_score"]:
                self.population[i] = new_population[i]
            else:
                self.population[i]["fail"] = new_population[i]

        population_sorted = self.sort_population(self.population)
        self.set_population(population_sorted)

class EvoGA(EvoPrompt):
    """ Genetic Algorithm
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.prompter is None:
            template = TEMPLATE_EVOLUTION["EvoPrompt"]["English"]["EvoGA"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

    def get_weight(self, ttl_score):
        """ GA 抽樣使用輪盤法 (Roulette Wheel Selection)
        """
        ttl_weight = np.array(ttl_score, dtype=float)
        if np.sum(ttl_weight!=0)<=1:
            ttl_weight[ttl_weight==0]=0.01  # 權重 0 的話會抽不到

        ttl_weight = ttl_weight/np.sum(ttl_weight)
        return ttl_weight

    def sample_prompt(self, i=None):
        """
        Var
            i: None
                為了統一格式所以必須加入，但是這個 function 不需要這個參數
        """
        ttl_score = [pair['train_score'] for pair in self.population]
        ttl_weight = self.get_weight(ttl_score)
        pair_1, pair_2 = np.random.choice(self.population, size=2, replace=False, p=ttl_weight)

        ttl_pair = [pair_1, pair_2]

        return ttl_pair

    def update(self, new_population):
        """ 兩個 population 中、所有 prompt 中，前 self.size_population 高分的 prompt
        """
        population_combine = self.sort_population(self.population+new_population)
        self.set_population(population_combine[:self.size_population])

class CoEvo(EvoPrompt):
    """
    更新方式: new_population 直接取代舊的 population
    """
    def __init__(self, **kwargs):
        """ 因為 CoEvo 多 population_contr，所以要初始化的東西比 EvoPrompt 多
        Var
            population_contr : list
                formation of the element in list is dict with at least:
                    {
                        "prompt": str,
                        "train_score": float,
                        "dev_score": float
                    }
        """

        population_contr = kwargs.pop("population_contr", None)
        super().__init__(**kwargs)
        if self.prompter is None:
            template = TEMPLATE_EVOLUTION["EvoPrompt"]["English"]["CoEvo_compare"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

        if population_contr is None:
            self.population_contr = self.get_population()
        else:
            population_contr = deepcopy(population_contr)
            population_formulate = self.formulate_population(population_contr)
            self.population_contr = deepcopy(population_formulate)

    def sample_prompt(self, i=None):
        """ 123
        """
        pair_contr = np.random.choice(self.population_contr)
        pair_best = self.population[0]
        pair_i = self.population[i]

        ttl_pair = [pair_contr, pair_best, pair_i]

        return ttl_pair

    def update(self, new_population):
        """ 兩個 population 對應比較，取 train_score 高者
        """
        population_sorted = self.sort_population(new_population)
        self.set_population(population_sorted)

class CoEvo2(CoEvo):
    """
    更新方式: new_population 跟舊的 population 倆倆比較，取 train_score 高者
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, new_population):
        """ 兩個 population 對應比較，取 train_score 高者
        """
        for i in range(self.size_population):
            if new_population[i]["train_score"] > self.population[i]["train_score"]:
                self.population[i] = new_population[i]
            else:
                self.population[i]["fail"] = new_population[i]

        population_sorted = self.sort_population(self.population)
        self.set_population(population_sorted)

class EvoGA4Contr(EvoGA):
    """ 為了測試 GA 用不同 template 的效果
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.prompter is None:
            template = TEMPLATE_EVOLUTION["EvoPrompt"]["English"]["ContrGA"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

    def sample_prompt(self, i=None):
        pass

    def update(self, new_population):
        pass

    def f(self, high_ahead=True):
        """ main function of this class
        Var
            high_ahead: bool
                「高的在前面」
                True for create p_contr
        """
        new_population = []
        for i in range(self.size_population-1):
            for j in range(i+1, self.size_population):

                if high_ahead is True:
                    ttl_pair = [
                        self.population[i],
                        self.population[j]
                    ]
                elif high_ahead is False:
                    ttl_pair = [
                        self.population[j],
                        self.population[i]
                    ]

                # evolution
                ttl_prompt = [ pair["prompt"] for pair in ttl_pair ]
                kwargs_4_prompter = dict(zip(self.ttl_key, ttl_prompt))
                prompt_4_create_new_os_prompt = self.prompter.create_prompt(**kwargs_4_prompter)

                for_debug = deepcopy(kwargs_4_prompter)
                new_prompt = self.get_distinct_new_propmt(new_population+self.get_population(), prompt_4_create_new_os_prompt, **for_debug)
                print(f"{new_prompt=}")

                # record
                prompt_score = self.evaluate(new_prompt)
                info = {
                    type_prompt: self.formulate_pair(pair)
                    for type_prompt, pair in zip(self.ttl_key, ttl_pair)
                }
                prompt_score["info"] = info
                new_population.append(prompt_score)
        return new_population
