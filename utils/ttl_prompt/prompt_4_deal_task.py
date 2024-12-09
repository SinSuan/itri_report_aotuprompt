""" 針對不同的任務、模型、資料集製作 prompt
"""
from copy import deepcopy
from utils.ttl_prompt.template.task import TEMPLATE_TASK_EVOPROMPT_CLS
from utils.ttl_prompt.get_prompt import GetPrompt

class Prompt4DealTask(GetPrompt):
    """ 針對 cls 任務製作 prompt
    """

    def __init__(self, **kwargs):
        """
        Var
            type_dataset: str
                "SST2"
            
            model: str
                "alpaca", "gpt", "opt"
        
        Attribute

            type_dataset: str
                "SST2"
            
            model: str
                "alpaca", "gpt", "opt"
            
            example: list[dict]
                the formate of each dict is {"question": str, "answer": str}
            
            template_shot: str
                這個 task 的 few_shot 的 template, 須包含 {question}, {answer}
        """
        self.type_dataset = kwargs.pop("type_dataset")
        self.type_model = kwargs.pop("type_model")
        self.example = deepcopy(TEMPLATE_TASK_EVOPROMPT_CLS["dataset"][self.type_dataset][self.type_model]["example"])
        self.template_shot = TEMPLATE_TASK_EVOPROMPT_CLS["dataset"][self.type_dataset][self.type_model]["template_shot"]

        super().__init__(**kwargs)

    def get_template_default(self, **kwargs) -> str:
        """
        Var
            kwargs: just for coherence
        """
        instruction = TEMPLATE_TASK_EVOPROMPT_CLS["instruction"][self.type_model]
        template = instruction + "{few_shot}" + self.template_shot[:-8] # len("{answer}")==8
        return template

    def create_few_shot(self, **kwargs):
        """ zero-shot/few-shot 的 prompt
        Var
            question: str
                屬於該 dataset 的問題

            kwargs
                num_example: int
                    default: 0 for zero-shot
                
                some_example: list[dict]
                    the formate of each dict is {"question": str, "answer": str}
        """

        # init
        num_example = kwargs.pop("num_example", 0)
        example_given = kwargs.pop("some_example", deepcopy(self.example))
        ttl_example = example_given[:num_example]
        if kwargs!={}:
            unexpected_keys = kwargs.keys()
            raise ValueError(f"""Unexpected kwargs: {", ".join(unexpected_keys)}""")

        # few-shot
        final_shot = ""
        for example in ttl_example:
            shot = self.template_shot.format(
                question=example["question"],
                answer=example["answer"]
            )
            final_shot += shot

        return final_shot

    def get_kwargs(self, **kwargs):
        """ zero-shot/few-shot 的 prompt
        Var
            os_prompt: str
                這個 task 的 os_prompt

            question: str
                屬於該 dataset 的問題

            num_example: int
                default: 0 for zero-shot
            
            some_example: list[dict]
                the formate of each dict is {"question": str, "answer": str}
        """

        # 加上 few_shot
        num_example = kwargs.pop("num_example", 0)
        some_example = kwargs.pop("some_example", deepcopy(self.example))
        few_shot = self.create_few_shot(num_example=num_example, some_example=some_example)
        kwargs["few_shot"] = few_shot

        kwargs_4_create_prompt = super().get_kwargs(**kwargs)
        return kwargs_4_create_prompt

