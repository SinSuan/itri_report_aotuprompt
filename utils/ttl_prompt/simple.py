""" 使用者指定的 template
"""

from utils.ttl_prompt.get_prompt import GetPrompt

class PromptSimple(GetPrompt):
    """ class 的 kwargs 有現成的 template
    """
    def get_template_default(self, **kwargs) -> str:
        pass
