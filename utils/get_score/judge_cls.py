""" 針對不同資料集的 score keeper
"""

from abc import abstractmethod
from utils.get_score.judge_abstract import Judge

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


class JudgeCLS(Judge):
    """ 分類任務的 score keeper
    """
    def __init__(self, **kwargs):
        """
        Var: only for prompter
            type_dataset: str
            type_model: str
            
        Attributes
            switch_keyword: dict
                {
                    int: list[str],
                }
            num_label: int
        """
        # print("in JudgeSST2")
        super().__init__(**kwargs)
        # if self.prompter is None:
        #     self.prompter = Prompt4DealTask(
        #         type_dataset=kwargs.get("type_dataset", None),
        #         type_model=kwargs.get("type_model", "alpaca")
        #     )
        self.set_switch_keyword()
        self.num_label = len(self.switch_keyword)

    @abstractmethod
    def set_switch_keyword(self):
        """ set self.switch_keyword
        """
        # the str must be "lower case", as extract_answer() will convert the reply to lower case
        self.switch_keyword = {
            int: list[str],
        }

    def method(self, data, **kwargs):
        """
        Var
            data: dict
                {
                    "question": str
                    "answer": str
                }

            kwargs: just for coherence
        """
        if DEBUGGER=="True": print("enter JudgeSST2.method")
        question = data['question']

        # create prompt
        prompt_4_exam = self.prompter.create_prompt(
            os_prompt=self.os_prompt,
            question=question,
            num_example=0,
        )

        # call llm
        answer_from_llm = self.llm.generate(prompt_4_exam)
        reply = answer_from_llm.strip()

        if DEBUGGER=="True": print("exit JudgeSST2.method")
        return reply

    def check_keyword(self, reply: str, label: int):
        """ check if any keyword of the label is in reply
        """
        ttl_keyword = self.switch_keyword[label]
        for keyword in ttl_keyword:
            if keyword in reply:
                return True
        return False

    def extract_answer(self, reply):
        """ select the label of which the keyword is represented in the reply
        """
        reply_lower = reply.lower()

        # init
        answer_predict = "unknown"

        for label in range(self.num_label):
            # print(f"{label=}")
            if self.check_keyword(reply_lower, label):
                answer_predict = label
                break

        return answer_predict

class JudgeAGNnews(JudgeCLS):
    """ AGNnews score
    """

    def set_switch_keyword(self):
        self.switch_keyword = {
            0: ["world"],
            1: ["sports"],
            2: ["business"],
            3: ["tech"]
        }

class JudgeInsurance(JudgeCLS):
    pass

class JudgeLaw(JudgeCLS):
    pass

class JudgeSST2(JudgeCLS):
    """ 史丹佛 SST-2 score
    """
    def set_switch_keyword(self):
        """很頭痛，不確定是否應該保留 approval/disapproval、optimism/pessimism 這兩對關鍵字，仿照 SST-5 用編號讀起來也不順
        """
        self.switch_keyword = {
            0: ["negative", "disapproval", "pessimism", "2"],
            1: ["positive", "approval", "optimism", "1"]
        }

class JudgeSST5(JudgeCLS):
    """ 史丹佛 SST-5 score
    """

    def set_switch_keyword(self):
        self.switch_keyword = {
            0: ["terrible", "1"],
            1: ["bad", "2"],
            2: ["okay", "3"],
            3: ["good", "4"],
            4: ["great", "5"]
        }

class JudgeSubj(JudgeCLS):
    """ Subj: Subjective or Objective
    """
    def set_switch_keyword(self):
        self.switch_keyword = {
            0: ["objective"],
            1: ["subjective"],
        }

class JudgeTREC(JudgeCLS):
    """ Subj: Subjective or Objective
    """
    def set_switch_keyword(self):
        self.switch_keyword = {
            0: ["description", "1"],
            1: ["entity", "2"],
            2: ["expression", "3"], # 原本是 abbr，但"可能"因為語言模型會讀到題目的 abbr 所以改成 expression
            3: ["human", "4"],
            4: ["number", "5"],
            5: ["location", "6"],
        }

class JudgeMR(JudgeSST2):
    """ MR: Movie Reviews
    # there label is same as SST-2
    """

class JudgeCR(JudgeSST2):
    """ MR: Movie Reviews
    # there label is same as SST-2
    """
