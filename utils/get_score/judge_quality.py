""" 針對不同資料集的 score keeper
他有兩個 prompter，目前不知道該怎麼辦，但應該短期內都不用到這個資料集了所以先不管
"""

from utils.ttl_prompt.simple import PromptSimple
from utils.ttl_prompt.template.summary import TEMPLATE_SUMMARY_ENGLISH
from utils.get_score.judge_abstract import Judge
from utils.split_into_chunk import get_ttl_chunk
from utils.call_model.prompt import get_prompt

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


class JudgeQuLAITY(Judge):
    """ QuLAITY score; 原 os_ap_sss_answer
    """
    def __init__(self, **kwargs):
        """
        Var
            size_chunck: int
            num_overlap: int
        """
        if DEBUGGER=="True": print("enter QuLAITYKeeper.__init__")
        super().__init__(**kwargs)
        if self.prompter is None:
            template = TEMPLATE_SUMMARY_ENGLISH["new"]
            prompter = PromptSimple(template=template)
            self.set_prompter(prompter)

        self.encoder = kwargs.get("encoder", None)

        size_chunck = kwargs.get("size_chunck", 3000)
        num_overlap = kwargs.get("num_overlap", 10)
        params = {
            "size_chunck": size_chunck,
            "num_overlap": num_overlap
        }
        self.set_params(params)

    def method(self, data, **kwargs):
        """
        Var
            size_chunck: int
                the number of words in each chunk
                
            num_overlap: int
                the number of senetences that overlap between two chunks
        """
        if DEBUGGER=="True": print("enter QuLAITYKeeper.method")

        size_chunck = kwargs.get("size_chunck", self.params["size_chunck"])
        num_overlap = kwargs.get("num_overlap", self.params["num_overlap"])

        content = data['content']   # 參考文章
        question = data['question'] # 問題(多選題)

        # 切分摘要完要輸入給llm的內容
        new_content = content
        while len(new_content.split(" "))>size_chunck:

            ttl_chunck = get_ttl_chunk(new_content, size_chunck, num_overlap, self.encoder)
            # 這一輪的新內容
            new_content = ""
            for chunk in ttl_chunck:

                # 請llm幫我們把重要資訊留下
                prompt_4_summarize_chunk =  get_prompt.sum("new", chunk, self.os_prompt, question)
                chunk_summary = self.llm.generate(prompt_4_summarize_chunk)
                # if chunk_summary==None:
                #     continue
                new_content+= chunk_summary+" "

            # 防錯(如果LLM api無回傳 直接比照truncate)
            if new_content=="":
                new_content = " ".join(content.split(" ")[:3000])
                break

        # 找完有用的內容後，進行問答
        prompt_4_exam_multichoice = get_prompt.exam(new_content,  question)
        answer_from_llm = self.llm.generate(prompt_4_exam_multichoice)

        if DEBUGGER=="True": print("exit QuLAITYKeeper.method")
        return answer_from_llm

    def pick_up(self, result):
        # init
        answer_predict = "unknown"

        # process result to determine answer_predict
        for option in range(1, 5):
            if str(option) in result:
                answer_predict = option
                break

        return answer_predict()
