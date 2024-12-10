"""
unify the form to call embedding model
"""

import json
from typing import List

from copy import deepcopy
import requests
import torch
from sentence_transformers import SentenceTransformer
import numpy as np

from utils.get_config import get_config
CONFIG = get_config()
# DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
DEBUGGER = False
HOST = CONFIG["model"]["embedding"]

class Bgem3:
    """ bge-m3 from lab
    """
    def __init__(self) -> None:
        self.url = f"{HOST}/v1/embeddings"

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.data = {
            "model": "bge-m3",
            "user": "null"
        }


    def call_api(self, text):
        data = deepcopy(self.data)

        data["input"] = text
        data = json.dumps(data)
        kwargs = {
            "headers": self.headers,
            "data": data,
            # "timeout": 120,
        }

        response = requests.post(self.url, **kwargs)

        try:
            response = json.loads(response.text)
            embedding = response['data'][0]['embedding']
        except Exception as e:
            print("kwargs =")
            print(kwargs)
            print()
            print("response =")
            print(response)
            print()
            print("response.text =")
            print(response.text)
            print()
            raise e

        return embedding

    def encode(self, ttl_sentence: List[str])->List:
        ttl_embedding = []
        for sentence in ttl_sentence:
            if sentence=="":    # bgem3 無法處理空字串
                sentence = " "

            embedding = self.call_api(sentence)
            ttl_embedding.append(embedding)
        ttl_embedding = np.array(ttl_embedding)
        return ttl_embedding

class OtherEmdedding:
    """ other embedding model downloaded from SentenceTransformer
    """
    def __init__(self, type_model:str) -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(type_model).to(device)

    def encode(self, ttl_sentence):
        """ 很多餘，但不打這個的話 Encoder 會跑不動
        """
        ttl_embedding = self.model.encode(ttl_sentence)
        return ttl_embedding

class Encoder:
    """ unify the form to call embedding model
    """
    def __init__(self, type_model:str) -> None:
        """
        Var
            type_model:
                "bgem3"
                others  <-  "multi-qa-mpnet-base-dot-v1", ...
        """

        if type_model=="bgem3":
            self.model = Bgem3()
        else:
            self.model = OtherEmdedding(type_model)

    def encode(self, ttl_sentence: List[str]) -> List:
        """ encode a list of strings at once
        """
        if DEBUGGER=="True": print("enter Encoder.encode")

        ttl_embedding = self.model.encode(ttl_sentence)

        if DEBUGGER=="True": print("exit Encoder.encode")
        return ttl_embedding
