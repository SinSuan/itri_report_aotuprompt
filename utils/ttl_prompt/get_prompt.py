""" get prompt for given ttl_key while fixing template
"""
from abc import ABC, abstractmethod
from copy import deepcopy
import re


class GetPrompt(ABC):
    """ fix a template, get the prompt for given ttl_key
    """
    def __init__(self, **kwargs):
        """
        Var
            template: str           (optional)
                evolution 的模板
        
        Attribute
            template: str
                evolution 的模板
            ttl_key_required: list[str]
                這個 template 需要哪些 key
        """
        self.template = kwargs.pop("template", self.get_template_default(**kwargs))
        self.ttl_key_required = self.get_ttl_key()

    @abstractmethod
    def get_template_default(self, **kwargs) -> str:
        """ get the template
        """

    def get_ttl_key(self, template=None):
        """
        Var
            template: str
                default: self.template

        Return
            set
        """
        if template is None:
            template = self.template

        ttl_keys_raw = re.findall('{(.*?)}', template)
        ttl_key = []
        for key in ttl_keys_raw:
            if key not in ttl_key:
                ttl_key.append(key)

        return ttl_key

    def get_kwargs(self, **kwargs):
        """
        args 跟 kwargs 只能擇一
        """
        ttl_key = kwargs.keys()
        ttl_key = set(ttl_key)
        ttl_key_required = set(self.ttl_key_required)
        if ttl_key != ttl_key_required:
            raise ValueError(f"The required keys are {self.ttl_key_required}, but got {ttl_key}. (diff in set)")
        kwargs_4_create_prompt = deepcopy(kwargs)
        return kwargs_4_create_prompt

    def create_prompt(self, **kwargs):
        """
        Var
            args: tuple
                這個 template 需要的 key
            kwargs: dict
                這個 template 需要的 key
        """
        kwargs_4_create_prompt = self.get_kwargs(**kwargs)
        prompt = self.template.format(**kwargs_4_create_prompt)
        return prompt
