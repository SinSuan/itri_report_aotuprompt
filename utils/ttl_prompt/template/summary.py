""" 偽 json 檔

回答 task 的格式

placeholder     (all required)
    {chunk}
        partial content of the article

    {os_prompt}
        prompt to enhance the model's performance

    {question}
        question and the options that needs to be answered

"""

# extract the key information from the chunk
    # chunk: The chunk that needs to be summarized
    # os_prompt: The prompt to enhance the model's performance
    # question_and_options: The question that needs to be answered
TEMPLATE_SUMMARY_ENGLISH = {
    "new": \
"""Article excerpt:
{chunk}

{os_prompt}

Question:
{question}""",

    "old": \
"""Article excerpt:
{chunk}

The above is the article excerpt related to my question.
Below is the question I want to ask.
Please select the text content that can answer this question.
{os_prompt}

Question:
{question}""",

}
