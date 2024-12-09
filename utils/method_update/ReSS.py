""" 信彰的方法
"""

from copy import deepcopy

from utils.method_update.population_updater import Updater
from utils.ttl_prompt.template.evolution import TEMPLATE_EVOLUTION
from utils.ttl_prompt.simple import PromptSimple

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

class Ress(Updater):
    """ 為了配合 EvoPrompt 而寫的 class
    """

    def __init__(self, **kwargs):

        self.encoder = kwargs.pop("encoder", None)
        self.example_num = kwargs.pop("example_num", 5)
        super().__init__(**kwargs)

        if self.prompter is None:
            template = TEMPLATE_EVOLUTION["ReSS"]["English"]["original"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

    def sample_prompt(self, i=None):
        """
        Var
            i: None
                為了統一格式所以必須加入，但是這個 function 不需要這個參數
        """
        pop_topk = self.population[:self.example_num]
        ttl_pair = deepcopy(pop_topk)

        return ttl_pair


    def get_new_prompt(self, prompt_4_create_new_os_prompt, temperature=0.5):
        """ call model 並 用正則表達抓<prompt></prompt>間的字
        Var
            temperature:
                EvoPrompt 論文的溫度設 0.5
        """
        if DEBUGGER=="True": print("enter get_new_prompt")

        reply = self.llm.generate(prompt_4_create_new_os_prompt, temperature)
        print(f"{reply=}")
        new_prompt = reply

        if DEBUGGER=="True": print("exit get_new_prompt")
        return new_prompt, ""


    def update(self, new_population):
        """ 更新 population
        """
        self.set_population(self.population+new_population)

    def create_example(self, ttl_pair):
        """ 用來產生 example
        """
        example = ""
        for pair in ttl_pair:
            prompt = pair["prompt"]
            score = pair["train_score"]
            example += f"[Old prompt]: {prompt}\n[Scores]: {score}\n\n"
        example = example[:-2]  # 把最後兩個換行拿掉
        return example

    def f(self):
        """ 因為 Ress 的模板跟 EvoPrompt 不同，所以要重新寫
        """
        ttl_pair = self.sample_prompt()

        # evolution

        # 主要是這段不一樣 (start)
        # example = ""
        # for pair in ttl_pair:
        #     prompt = pair["prompt"]
        #     score = pair["train_score"]
        #     example += f"[Old prompt]: {prompt}\n[Scores]: {score}\n\n"
        # example = example[:-2]
        example = self.create_example(ttl_pair)
        kwargs_4_prompter = dict(zip(self.ttl_key, [example]))
        prompt_4_create_new_os_prompt = self.prompter.create_prompt(kwargs_4_prompter)
        # prompt_4_create_new_os_prompt = get_prompt.create(self.type_update, example)
        # 主要是這段不一樣 (end)


        for_debug = {
            f"p_{idx}": pair["prompt"]
            for idx, pair in enumerate(ttl_pair)
        }
        new_prompt = self.get_distinct_new_propmt(self.population, prompt_4_create_new_os_prompt, **for_debug)

        # record
        prompt_score = self.evaluate(new_prompt)
        info = {
            f"p_{idx}": self.formulate_pair(pair)
            for idx, pair in enumerate(ttl_pair)
        }
        prompt_score["info"] = info
        new_population = [prompt_score]

        self.update(new_population)

        population_return = self.get_population()
        # 確保 population 只有 prompt 跟 *_score
        population_formulate = self.formulate_population(self.population)
        self.set_population(population_formulate)

        return population_return
