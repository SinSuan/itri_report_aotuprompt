import json
import requests

from utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

SUGGEST_SYSTEM_PROMPT = CONFIG["model"]["SUGGEST_SYSTEM_PROMPT"]

HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

class CallTGI:
    """ call tgi to:
        1. tokenize     return the tokenized prompt
        2. count_token  return the number of tokens in the prompt
        3. generate     return the generated text
    """

    def __init__(self, host=None, headers=None) -> None:
        """
        Var
            host: str
                the host url of the tgi
                prefix: "http://"
        
        Attribute
            host: str
                the host url of the tgi
                prefix: "http://"
            headers: dict
                the headers of the request
        """
        if DEBUGGER=="True": print(f"\t{host=},\tenter CallTGI.__init__")

        if host is None:
            host = CONFIG["model"]["llm"]
        self.host = host

        if headers is None:
            self.headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = headers
        
        if DEBUGGER=="True": print(f"\t{host=},\texit CallTGI.__init__")

    def call_tgi(self, url, prompt, parameter):
        if DEBUGGER=="True": print(f"\t{self.host=},\tenter CallTGI.call_tgi")

        data = json.dumps({
            "inputs": prompt,
            "parameters": parameter
        })
        kwargs = {
            "headers": self.headers,
            "data": data
        }
        if "generate" in url:
            kwargs["stream"] = True

        response = requests.post(url, **kwargs)

        if DEBUGGER=="True": print(f"\t{self.host=},\texit CallTGI.call_tgi")
        return response

    def tokenize(self, prompt):
        if DEBUGGER=="True": print(f"\t{self.host=},\tenter CallTGI.tokenize")

        parameter = {
            "max_new_tokens": 0
        }
        url = f"{self.host}/tokenize"
        response = self.call_tgi(url, prompt, parameter)

        if DEBUGGER=="True": print(f"\t{self.host=},\texit CallTGI.tokenize")
        return response

    def count_token(self, prompt):
        """ count the number of tokens in the prompt
        """
        if DEBUGGER=="True": print(f"\t{self.host=},\tenter CallTGI.count_token")

        try:
            response = self.tokenize(prompt)
            response = response.json()
            num_token = len(response)
        except Exception as e:
            num_token = "fail to count token"
            print(f"Except in CallTGI.count_token =\n{e}")

        if DEBUGGER=="True": print(f"\t{self.host=},\texit CallTGI.count_token")
        return num_token

    def generate(self, user_prompt, temperature=None, max_new_tokens=1000):
        if DEBUGGER=="True": print(f"\t{self.host=},\tenter CallTGI.generate")

        prompt = f"<s> {SUGGEST_SYSTEM_PROMPT} [INST] {user_prompt} [/INST]"
        # print(f"{prompt=}")
        num_token_input = self.count_token(prompt)
        max_new_tokens = min(max_new_tokens, 8192-num_token_input)

        parameter = {
            "do_sample": temperature is not None,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }
        url = f"{self.host}/generate"

        try:
            response = self.call_tgi(url, prompt, parameter)
            j_result = response.json()
            if "generated_text" in j_result.keys():
                r = j_result['generated_text']
            else:
                r = j_result
        except Exception as e:
            print(f"{prompt=}")
            print(f"Except in CallTGI =\n{e}")
            raise e

        if DEBUGGER=="True": print(f"\t{self.host=},\texit CallTGI.generate")
        return r
