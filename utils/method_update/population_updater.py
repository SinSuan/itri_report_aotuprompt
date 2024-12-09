""" general class to update population
"""

from copy import deepcopy
import re
from abc import ABC, abstractmethod

# from utils.get_score.judge_cls import JudgeSST2
# from utils.get_score.judge_quality import JudgeQuLAITY
# from utils.score import get_score

from utils.call_model.llm import CallTGI
from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]




class Updater(ABC):
    """ general evoluatior of population

    required to implement:
        self.sample_prompt()
        self.update()
        self.template        ( for evoprompt)
    """

    def __init__(self, **kwargs):
        """
        Var
            llm: utils.call_model.llm.CallTGI
            judge: Judge
                "SST-2"

            prompter: GetPrompt

            population: list
                formation of the element in list is dict with at least:
                    {
                        "prompt": str,
                        "train_score": float,
                        "dev_score": float
                    }
        
        Attribute
            llm
            judge
            prompter
            ttl_type_prompt: list[str]
            population: list
            size_population: int
        """
        if DEBUGGER=="True": print("enter Updater.__init__")

        self.judge = kwargs.get("judge", None)
        print(f"{self.judge=}")
        llm = kwargs.get("llm", None)
        if llm is None:
            llm = CallTGI()
        self.llm = llm

        prompter = kwargs.pop("prompter", None)
        self.set_prompter(prompter)

        # 回歸初始狀態，看 record 的時候才能一眼看出哪個 iteration 變了
        population = deepcopy(kwargs["population"])
        if not isinstance(population, list):
            raise ValueError(f"population should be list, but got {type(population)}\npopulation =\n{population}")
        population_formulate = self.formulate_population(population)
        self.set_population(population_formulate)
        self.size_population = len(self.population)

        if DEBUGGER=="True": print("exit Updater.__init__")

    def check_abstract(self):
        """ check abstract method
        """

    def set_prompter(self, prompter):
        """ usually for set default prompter
        """
        self.prompter = prompter
        if self.prompter is not None:
            self.ttl_key = self.prompter.get_ttl_key()

    def set_population(self, population):
        """ usually for self.update()
        """
        self.population = population
        self.size_population = len(self.population)

    def get_population(self):
        """ to ensure the population is not changed
        """
        return deepcopy(self.population)

    def get_dataset(self):
        """ to ensure the population is not changed
        """
        dataset = deepcopy(self.judge.get_dataset())
        return dataset

    def sort_population(self, population, type_score="train_score"):
        """ 依照 train_score 由高到低排序。因為太常被 pylint 警告 "Line too long (x/100)"，所以另外寫一個 function
        Var

            population: list
                formation of the element in list is dict with at least:
                    {
                        "prompt": str,
                        "train_score": float,
                        "dev_score": float
                    }

            type_score: str
                "train_score" or "dev_score"
        """
        population_sorted = sorted(population,  key=lambda x: x[type_score],  reverse=True)
        return population_sorted

    def evaluate(self, os_prompt):
        """ 用來評估 prompt 的分數
        Var
            prompt: str
        """

        ttl_score = self.judge.get_score(os_prompt)

        score_train, precision_train, dataset_confusing_train, dataset_wrong_train = ttl_score["train_split"]
        score_dev, precision_dev, dataset_confusing_dev, dataset_wrong_dev = ttl_score["dev_split"]

        prompt_score = {
            "prompt": os_prompt,
            "train_score": score_train,
            "dev_score": score_dev,
            "preicision": {
                "train": precision_train,
                "dev": precision_dev
            },
            "data_sick": {
                "train": {
                    "confusing": dataset_confusing_train,
                    "wrong": dataset_wrong_train
                },
                "dev": {
                    "confusing": dataset_confusing_dev,
                    "wrong": dataset_wrong_dev
                }
            }
        }
        return prompt_score

    def formulate_pair(self, pair):
        """ prompt 可能紀錄很多資訊只留下 prompt、*_score、precision，方便讀檔的時候知道從哪個 iteration 開始變化
        Var
            pair: dict or str
                dict formation:
                {
                    "prompt": str,
                    "train_score": int,
                    "dev_score": int,
                }
                str formation:
                "prompt"
        
        Return: dict
            {
                "prompt": str,          (required)
                "train_score": int,     (required)
                "dev_score": int,       (required)
                "preicision": {         (optional)
                    "train": float,
                    "dev": float
                }
            }
        """
        pair = deepcopy(pair)

        if isinstance(pair, str):       # ex: 新生出來的 prompt
            formulated_pair = self.evaluate(pair)
        elif isinstance(pair, dict):    # 從上一輪 population 拿出來的
            formulated_pair = {
                "prompt": pair['prompt'],
                "train_score": pair['train_score'],
                "dev_score": pair['dev_score'],
                }

            if "precision" in pair:
                formulated_pair["precision"] = pair["precision"]

        return formulated_pair

    def formulate_population(self, population):
        """ 將 population
            1. 轉換成只有 prompt 跟 *_score 的形式
            2. 依照 train_score 由高到低排序
        """
        population = [ self.formulate_pair(pair) for pair in population ]
        population = self.sort_population(population)
        return population

    def prompt_in_list(self, new_prompt, population_current=None):
        """
        Var
            new_prompt: str
                the prompt to be check whether or not the in ttl_prompt
        """
        if population_current is None:
            population_current = self.get_population()

        # 預設不在
        in_list = False

        # 然後檢查
        for pair in population_current:
            if pair['prompt'] == new_prompt:
                in_list = True
                break

        return in_list

    def get_new_prompt(self, prompt_4_create_new_os_prompt, temperature=0.5):
        """ call model 並 用正則表達抓<prompt></prompt>間的字
        Var
            temperature:
                EvoPrompt 論文的溫度設 0.5
        """
        if DEBUGGER=="True": print("enter Updater.get_new_prompt")

        new_prompt = " and "
        while new_prompt==" and ":
            reply = self.llm.generate(prompt_4_create_new_os_prompt, temperature)
            # print(f"{reply=}")
            match_all = re.findall(r'<\s*prompt\s*>(.*?)<\s*/\s*prompt\s*>', reply, re.DOTALL)
            if DEBUGGER=="True": print(f"{match_all=}")

            while match_all == []:
                reply = self.llm.generate(prompt_4_create_new_os_prompt, temperature)
                # print(f"{reply=}")
                match_all = re.findall(r'<\s*prompt\s*>(.*?)<\s*/\s*prompt\s*>', reply, re.DOTALL)
                if DEBUGGER=="True": print(f"{match_all=}")

            new_prompt = match_all[-1]

        if DEBUGGER=="True": print("exit Updater.get_new_prompt")
        return new_prompt, reply

    def get_distinct_new_propmt(self, population_current, prompt_4_create_new_os_prompt, temperature=0.5, **for_debug):
        """ 用來確保 new_prompt 不在 population 裡
        Var
            temperature:
                EvoPrompt 論文的溫度設 0.5
            
            for_debug:
                用來 debug 的參數

        """
        # 嘗試生出新的 prompt
        num_inc_temp = int((1-temperature)//0.1)    # 生不出新的 prompt 就提高溫度
        num_prompt = len(population_current) + self.size_population

        # 溫度設最高之後給 pop 裡的每個參數各一次機會
        # temperature 升到 1.0 都有重複，old pop 跟 new pop 裡的每個 prompt 都生過一次，最後再試一次（類似鴿籠原理）
        num_try = num_inc_temp + num_prompt + 1

        temperature = 0.5
        new_prompt, reply = self.get_new_prompt(prompt_4_create_new_os_prompt, temperature)
        for _ in range(num_try):
            if self.prompt_in_list(new_prompt, population_current) is False:
                break
            temperature = min(1, temperature + 0.1) # prompt 重複的話就增加變化度
            new_prompt, reply = self.get_new_prompt(prompt_4_create_new_os_prompt, temperature)

        # 如果經過 num_try 次還是重複，就 raise error
        if self.prompt_in_list(new_prompt, population_current) is True:
            print(f"{self.population=}")

            for k, v in for_debug.items():
                print(f"{k}={v}")

            print(f"{new_prompt=}")
            print(f"{reply=}")
            print(f"{prompt_4_create_new_os_prompt=}")
            raise ValueError("想不到新的 prompt 了")

        return new_prompt

    @abstractmethod
    def sample_prompt(self, i=None) -> tuple[list]:
        """
        Var
            i: int
                用來 sample prompt 的 index (for EvoGA)

        Return
            ttl_pair: list[dict]
                dict formation:
                {
                    "prompt": str,
                    "train_score": float,
                    "dev_score": float
                }
        """

    @abstractmethod
    def update(self, new_population) -> None:
        """ 更新 self.population
        """

    @abstractmethod
    def f(self):
        """ main function of this class
        """


class TTLMethodUpdater(Updater):
    """ 只是要用那些 method 而已
    """
    def __init__(self, **kwargs):
        """ 不需要 population
        Var

            ttl_model: tuple(llm, tokenizer)
                llm: list of CallTGI in utils.call_model.call_model
                embedding_model: Encoder in utils.call_model.embedding

            judge: object int utils.get_score.*
        """
        if DEBUGGER=="True": print("enter TTLMethodUpdater.__init__")

        self.llm = kwargs.get("ttl_llm", None)
        self.encoder = kwargs.get("encoder", None)
        self.judge = kwargs.get("judge", None)

        if DEBUGGER=="True": print("exit TTLMethodUpdater.__init__")

    def sample_prompt(self, i=None):
        pass

    def update(self, new_population):
        pass

    def f(self):
        pass
