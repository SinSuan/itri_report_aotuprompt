""" 偽 json 檔

回答 task 的格式

placeholder
    {content}   optional
    {question}  required

{
    "instruction": {
        {model}: {os_prompt}
    },
    "few-shot": {
        {task}: {
            {model}: {
                "template": "{ f-string with {question} and {answer} }",
                "example": [
                    {
                        "question": "{question}",
                        "answer": "{answer}"
                    }
                ]
            }
        }
    }
}

"""

TEMPLATE_QUALTITY = {

# answer multichoice
    # content: summarized chuncks of the corresponding content
    # question: The question that needs to be answered
    "original": \
"""There will be an article question and four options. 
Please choose the option that answers the question based on the article.

article:
{content}

question:
{question}

Your answer must be the number of one of the options,meaning it should be either option1, option2, option3, or option4. 
The format for the answer should be as follows: Answer__optionX.""",

}

TEMPLATE_TASK_EVOPROMPT_CLS = {

    "instruction": {
        "opt": "Instruction: {os_prompt}",
        "gpt": "{os_prompt}",
        "alpaca": "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{os_prompt}"
        },

    "dataset": {
        "AGNews":{
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "Arafat expulsion has never been closer: Israeli FM JERUSALEM - Foreign Minister Silvan Shalom said Thursday that Israel had never been closer to expelling veteran Palestinian leader Yasser Arafat from his West Bank headquarters.",
                        "answer": "World"
                    },
                    {
                        "question": "Two US runners reach 100 hurdles final ATHENS, Greece - World champion Perdita Felicien and two United States runners reached the final of the 100-meter hurdles Monday, an event that lost Gail Devers to injury a day earlier.",
                        "answer": "Sports"
                    },
                    {
                        "question": "U.S., EU Spar Over Airbus, Boeing Aid  WASHINGTON (Reuters) - The United States and Europe on  Wednesday filed tit-for-tat World Trade Organization complaints  over billions of dollars in subsidies for top aircraft  manufacturers Airbus and Boeing.",
                        "answer": "Business"
                    },
                    {
                        "question": "Veritas buys KVault Software in \\$225M deal Storage and backup application vendor Veritas Software Corp. is acquiring e-mail archiving vendor KVault Software Ltd. (KVS) to bolster its offerings to customers.",
                        "answer": "Tech"
                    }
                ]
            },
        },
        "CR":{
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "one of the year 's best films , featuring an oscar-worthy performance by julianne moore .",
                        "answer": "positive"
                    },
                    {
                        "question": "great phone , i 'd buy another .",
                        "answer": "positive"
                    },
                    {
                        "question": "this product is absolutely not ready for release .",
                        "answer": "negative"
                    },
                ]
            },
        },
        "MR":{
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "wise and deadpan humorous .",
                        "answer": "positive"
                    },
                    {
                        "question": "shamelessly sappy and , worse , runs away from its own provocative theme .",
                        "answer": "negative"
                    }
                ]
            },
        },
        "SST-2": {
            "opt": {
                "template_shot": "\nInput: {question}\nOutput: {answer}",
                "example": [
                    {
                        "question": "one of the year 's best films , featuring an oscar-worthy performance by julianne moore .",
                        "answer": "positive"
                    },
                    {
                        "question": "it 's just merely very bad .",
                        "answer": "negative"
                    }
                ]
            },
            "gpt": {},
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "great phone , i 'd buy another .",
                        "answer": "positive"
                    },
                    {
                        "question": "it 's just merely very bad .",
                        "answer": "negative"
                    }
                ]
            },
        },
        "SST-5": {
            "opt": {
                "template_shot": "\nInput: {question}\nOutput: {answer}",
                "example": [
                    {
                        "question": "the heavy-handed film is almost laughable as a consequence .",
                        "answer": "terrible"
                    },
                    {
                        "question": "movie fans , get ready to take off ... the other direction .",
                        "answer": "bad"
                    },
                    {
                        "question": "Input: a movie that hovers somewhere between an acute character study and a trite power struggle .",
                        "answer": "okay"
                    },
                    {
                        "question": "Input: escaping the studio , piccoli is warmly affecting and so is this adroitly minimalist movie .",
                        "answer": "good"
                    },
                    {
                        "question": "seldom has a movie so closely matched the spirit of a man and his work .",
                        "answer": "great"
                    }
                ]
            },
            "gpt": {
                "template_shot": "\n\nSentence: {question}\nLabel: {answer}",
                "example": [
                    {
                        "question": "the heavy-handed film is almost laughable as a consequence .",
                        "answer": "terrible"
                    },
                    {
                        "question": "movie fans , get ready to take off ... the other direction .",
                        "answer": "bad"
                    },
                    {
                        "question": "a movie that hovers somewhere between an acute character study and a trite power struggle .",
                        "answer": "okay"
                    },
                    {
                        "question": "escaping the studio , piccoli is warmly affecting and so is this adroitly minimalist movie .",
                        "answer": "good"
                    },
                    {
                        "question": "seldom has a movie so closely matched the spirit of a man and his work .",
                        "answer": "great"
                    },
                ]
            },
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "the heavy-handed film is almost laughable as a consequence .",
                        "answer": "terrible"
                    },
                    {
                        "question": "movie fans , get ready to take off ... the other direction .",
                        "answer": "bad"
                    },
                    {
                        "question": "a movie that hovers somewhere between an acute character study and a trite power struggle .",
                        "answer": "okay"
                    },
                    {
                        "question": "escaping the studio , piccoli is warmly affecting and so is this adroitly minimalist movie .",
                        "answer": "good"
                    },
                    {
                        "question": "seldom has a movie so closely matched the spirit of a man and his work .",
                        "answer": "great"
                    },
                ]
            },
        },
        "Subj":{
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "a cold-hearted judge finds out when a seemingly crazy young couple break into his house and take him captive .",
                        "answer": "objective"
                    },
                    {
                        "question": "a heartening tale of small victories and enduring hope .",
                        "answer": "subjective"
                    },
                ]
            },
        },
        "TREC":{
            "alpaca": {
                "template_shot": "\n\n### Input:\n{question}\n\n### Response:\n{answer}",
                "example": [
                    {
                        "question": "What made Jane Goodall famous ?",
                        "answer": "Decription"
                    },
                    {
                        "question": "Which sex is denied voting rights in Kuwait ?",
                        "answer": "Entity"
                    },
                    {
                        "question": "What does RCA stand for ?",
                        "answer": "Expression"
                    },
                    {
                        "question": "Who was Lacan ?",
                        "answer": "Human"
                    },
                    {
                        "question": "hat attracts tourists to Reims ?",
                        "answer": "Location"
                    },
                    {
                        "question": "What is the gestation period for human pregnancies ?",
                        "answer": "Number"
                    },
                ]
            },
        },
    },
}
