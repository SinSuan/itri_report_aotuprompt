""" 跑實驗並取得分數
"""


from abc import ABC, abstractmethod
from copy import deepcopy
import sys

from utils.ttl_prompt.prompt_4_deal_task import Prompt4DealTask
from utils.get_config import get_config

# from tqdm.auto import tqdm
if 'ipykernel' in sys.modules:
    from tqdm.autonotebook import tqdm
else:
    from tqdm import tqdm

CONFIG = get_config()
# DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
DEBUGGER = False


class Judge(ABC):
    """ 跑實驗並取得分數
    
    如果要用 ray 就要另外寫一個 class，本 class 不支援 ray
    
    required to implement:
        self.extract_answer()
        self.method()
    """
    def __init__(self, **kwargs):
        """
        Var
            kwargs:
                prompter: GetPrompt                     (required)
                llm: utils.call_model.llm.CallTGI       (required)
                dataset: dict                           (required)
                    {
                        "train_split": list,
                        "dev_split": list
                    }
                    formation of the element in list:
                        {
                            "content": str,
                            "question": str,
                            "answer": str
                        }

                params: dict                            (optional)
        
        Attribute
            os_prompt: str                              (optional)
                SAP 在練的 prompt
        """
        if DEBUGGER=="True": print("enter GetScore.__init__")

        self.llm = kwargs.get("llm", None)
        prompter = kwargs.pop("prompter", None)
        if prompter is None:
            prompter = Prompt4DealTask(
                type_dataset=kwargs.get("type_dataset", None),
                type_model=kwargs.get("type_model", "alpaca")
            )
        self.set_prompter(prompter)

        dataset = deepcopy(kwargs.get("dataset", None))
        if dataset is not None:
            self.data_train = dataset.get("train_split", None)
            self.data_dev = dataset.get("dev_split", deepcopy(self.data_train))


        # parameter for self.method()
        self.params = kwargs.get("params", None)

        # init
        self.set_os_prompt(None)

        if DEBUGGER=="True": print("exit GetScore.__init__")

    def set_prompter(self, prompter):
        """ usually for set default prompter
        """
        self.prompter = prompter
        if self.prompter is not None:
            self.ttl_key = self.prompter.get_ttl_key()

    def set_params(self, kwargs):
        """
        Var
            kwargs: dict
                parameter for self.method()
        """
        self.params = kwargs

    def set_os_prompt(self, os_prompt):
        """
        Var
            os_prompt: str
                SAP 在練的 prompt
        """
        self.os_prompt = os_prompt

    def get_dataset(self, split):
        """
        Var
            split: str
                "train", "dev", "both"
        """
        if split=="train":
            dataset = {
                "train_split": deepcopy(self.data_train)
            }
        elif split=="dev":
            dataset = {
                "dev_split": deepcopy(self.data_dev)
            }
        elif split=="both":
            dataset = {
                "train_split": deepcopy(self.data_train),
                "dev_split": deepcopy(self.data_dev)
            }
        return dataset

    @abstractmethod
    def method(self, data, **kwargs):
        """ 針對不同 dataset，實驗方法可能不同
        Var
            正常來說直接使用 self.params，但也可以用 kwargs 自定義

        --------
        example:
            if kwargs=={}:
                kwargs = deepcopy(self.params)
        """

    def get_reply(self, data, **kwargs):
        """ 有時候 API或TGI 會出問題，就要重新 request
        Var
            kwargs:
                data to method
        
        Return
            str
        """
        if DEBUGGER=="True": print("enter GetScore.get_answer")

        try:
            reply = self.method(data, **kwargs)
        except Exception as e:
            print(f"Error in GetScore.get_reply: {e}")
            reply = "redo"
            # raise e

        if DEBUGGER=="True": print("exit GetScore.get_answer")
        return reply

    @abstractmethod
    def extract_answer(self, reply):
        """ 將 reply 轉換成可與資料集 answer 比較的東西
        Var
            reply: str
                replay from llm
        
        Return
            str or int
                "unknown" for no match
        
        --------
        example:
            # init
            answer_predict = "unknown"

            # process reply to determine answer_predict
            return answer_predict
        """

    def experiment(self, os_prompt, dataset, **kwargs):
        """ 實驗
        Var
            os_prompt: str
                SAP 在練的 prompt
            
            dataset: list[dict]
                dict is of the form:
                    {
                        "question": str,
                        "answer": str
                    }
        Return
            score: int
            precision: float
                其實是 accuracy
            dataset_confusing: list[dict]
                無法判斷的資料
            dataset_wrong: list[dict]
        """
        if DEBUGGER=="True": print("enter GetScore.experiment")

        self.set_os_prompt(os_prompt)

        dataset_confusing = []
        dataset_wrong = []
        score = 0    # 總分數
        for data in tqdm(dataset):

            # get answer_predict
            reply = self.get_reply(data, **kwargs)
            while reply=="redo":
                reply = self.get_reply(data, **kwargs)
            answer_predict = self.extract_answer(reply)
            # print(f"{reply=}\n{answer_predict=}")

            # 對答案、計分數
            answer_label = data['answer']
            # print(f"{answer_label=}")

            if answer_predict==answer_label:    # 答對
                score += 1

            else:
                data_sick = deepcopy(data)
                data_sick["reply"] = reply

                if answer_predict=="unknown":   # 無法判斷
                    dataset_confusing.append(data_sick)
                else:                           # 答錯
                    dataset_wrong.append(data_sick)

            precision = score / len(dataset)

        if DEBUGGER=="True": print("exit GetScore.experiment")
        return score, precision, dataset_confusing, dataset_wrong

    def get_score(self, os_prompt, split_dataset="both", **kwargs):
        """ 取得分數
        Var
            os_prompt: str
                SAP 在練的 prompt

            split_dataset: str or dict
                str:    "both", "train, "dev"
                dict:
                    {
                        "train_split": list,
                        "dev_split": list
                    }
                    elements of the lists:
                        {
                            "question": str,
                            "answer": str
                        }

        Return
            dict
                {
                    "train_split": int,
                    "dev_split": int
                }
        """
        if DEBUGGER=="True": print("enter GetScore.get_score")

        if isinstance(split_dataset, str):
            dataset = self.get_dataset(split_dataset)
        elif isinstance(split_dataset, dict):
            dataset = deepcopy(split_dataset)

        ttl_score = {
            split: self.experiment(os_prompt, dataset_split, **kwargs)
            for split, dataset_split in dataset.items()
        }

        if DEBUGGER=="True": print("exit GetScore.get_score")
        return ttl_score
    
    def get_score_result(self, os_prompt, split_dataset, **kwargs):
        """ 取得分數
        Var
            os_prompt: str
                SAP 在練的 prompt

            split_dataset: str or dict
                str:    "train, "dev"

        Return
            dict
                {
                    "train_split": int,
                    "dev_split": int
                }
        """
        if DEBUGGER=="True": print("enter GetScore.get_score_result")
        
        dataset = self.get_dataset(split_dataset)[f"{split_dataset}_split"]
        # score, _, dataset_confusing, dataset_wrong = \
        #     self.experiment(os_prompt, dataset, **kwargs)
        result = self.experiment(os_prompt, dataset, **kwargs)
        
        if DEBUGGER=="True": print("exit GetScore.get_score_result")
        # return score, dataset_confusing, dataset_wrong
        return result
