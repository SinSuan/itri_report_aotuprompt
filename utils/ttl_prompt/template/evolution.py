""" 偽 json 檔

「更新 population」、「生新 prompt」 的 instruction
"""

TEMPLATE_RESS_ENGLISH = {
    # example: form: "[Old prompt]:"{p['prompt']}"\n[Scores]:{p['score']}\n\n"
    "original": \
"""You are an expert at crafting prompts.
Based on the example task given below for an LLM, fill in the most suitable prompt in the place marked [new_prompt].
The following describes the task you will undertake:

"
Article excerpt:
[article_chunk]

The above is the article excerpt related to my question.
Below is the question I want to ask.
Please select the text content that can answer this question.
[new_prompt]

Question:
[input_question]
"

Here are some example prompts and their scores, ranging from 0 to 100, with higher scores indicating better performance.
Please help me think of a unique new_prompt where higher scores are better.

{example}

### You only need to return the new_prompt ###
DON'T return the [Scores] or explanation.
Your new_prompt:__""",

}

TEMPLATE_EVOPROMPT_ENGLISH = {

    # p_1, p_2: the random selected parent prompts to be mutated
    # p_best: the prompt is with the highest score
    # p_i: the prompt to crossover
    "EvoDE":\
"""Please follow the instruction step-by-step to generate a better prompt.
1. Identify the different parts between the Prompt 1 and Prompt 2:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Randomly mutate the different parts
3. Combine the different parts with Prompt 3, selectively replace it with the different parts in step 2 and generate a new prompt.
Prompt 3: Rewrite the given input text into simpler English sentences while preserving the same meaning, so it can be understood by non-native English speakers.
4. Crossover the prompt in the step3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: Make the sentence easier for people who do not speak English fluently to comprehend.

1. Identifying the different parts between Prompt 1 and Prompt 2:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
Different parts:
"input text" vs "my complex sentence"
"simpler text" vs "simpler terms, but keep the meaning"

2. Randomly mutate the different parts:
"input text" -> "provided text"
"my complex sentence" -> "the difficult sentence"
"simpler text" -> "easier language"
"simpler terms, but keep the meaning" -> "simpler words while maintaining the meaning"

3. Combine the different parts with Prompt 3, selectively replace it with the different parts in step 2 and generate a new prompt:
Prompt 3: Rewrite the given input text into simpler English sentences while preserving the same meaning, so it can be understood by non-native English speakers.
New Prompt: Transform the provided text into easier language while maintaining the meaning, making it accessible for non-native English speakers.

4. Crossover the prompt in step 3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: Make the sentence easier for people who do not speak English fluently to comprehend.
Final Prompt: <prompt>Convert the difficult sentence into simpler words while preserving the meaning, so it's easier for non-native English speakers to understand.</prompt>


Please follow the instruction step-by-step to generate a better prompt.
1. Identify the different parts between the Prompt 1 and Prompt 2:
Prompt 1: {p_1}
Prompt 2: {p_2}
2. Randomly mutate the different parts
3. Combine the different parts with Prompt 3, selectively replace it with the different parts in step2 and generate a new prompt.
Prompt 3: {p_best}
4. Crossover the prompt in the step3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: {p_i}

1. """,

    # p_1, p_2: the random selected parent prompts to crossover
    "EvoGA": \
"""Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Mutate the prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. Crossover Prompt: Simplify the complex text while maintaining its meaning.
2. <prompt>Simplify the complex text while maintaining its meaning.</prompt>

Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: {p_1}
Prompt 2: {p_2}
2. Mutate the prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. """,

    "EvoGA_mutate": \
"""Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Mutate the new prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. Crossover the following prompts and generate a new prompt:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
new prompt: Simplify the complex text while maintaining its meaning.
2. Mutate the new prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.
new prompt: Simplify the complex text while maintaining its meaning.
final prompt: <prompt>Make the complex text easier while maintaining its meaning.</prompt>

Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: {p_1}
Prompt 2: {p_2}
2. Mutate the new prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. """,

    # p_1, p_2: the random selected parent prompts to crossover
    "testGA": \
"""Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Mutate the prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. Crossover Prompt: Simplify the complex text while maintaining its meaning.
2. <prompt>Simplify the complex text while maintaining its meaning.</prompt>

Please follow the instruction step-by-step to generate a better prompt.
1. Crossover the following prompts and generate a new prompt:
Prompt 1: {p_1}
Prompt 2: {p_2}
2. Mutate the prompt generated in Step 1 and generate a final prompt bracketed with <prompt> and </prompt>.

1. """,

    # p_better: prompt with the highest score
    # p_normal: prompt with the lower score
    "ContrGA": \
"""Please follow the instruction step-by-step to generate a worse prompt.
1. Crossover the following prompts and generate a new prompt:
better prompt: Rewrite the input text into simpler text.
normal prompt: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Mutate the prompt generated in Step 1 and generate a worse prompt bracketed with <prompt> and </prompt>.

1. Crossover Prompt: Simplify the complex text while maintaining its meaning.
2. <prompt>Make the complex text easier while maintaining its meaning.</prompt>

Please follow the instruction step-by-step to generate a worse prompt.
1. Crossover the following prompts and generate a new prompt:
better prompt: {p_better}
normal prompt: {p_normal}
2. Mutate the prompt generated in Step 1 and generate a worse prompt bracketed with <prompt> and </prompt>.

1. """,

    # p_contr: mutated from p_worst in high_pop and random p_init
    # p_best: the prompt is with the highest score
    # p_i: the prompt to crossover
    "CoEvo": \
""""Please follow the instruction step-by-btep to generate a better prompt.
1. Identify the same parts and the different parts between Prompt 1 and Prompt 2:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Randomly mutate the same parts and the different parts.
3. Combine the same parts and the different parts with Prompt 3, selectively replace it with the same parts and the different parts in step 2 and generate a new prompt.
Prompt 3: Rewrite my complex sentence in simpler terms, but keep the meaning.
4. Crossover the prompt in the step3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: Make the sentence easier for people who do not speak English fluently to comprehend.

1.  Identifying the same parts and the different parts between Prompt 1 and Prompt 2:
Prompt 1: Rewrite the input text into simpler text.
Prompt 2: Rewrite my complex sentence in simpler terms, but keep the meaning.
Same parts:
"rewrite"
"simpler"

Different parts:
"input text" vs "my complex sentence"
"simpler text" vs "simpler terms, but keep the meaning"

2. Randomly mutate the same parts and the different parts:
Same parts:
"rewrite" -> "transform"
"simpler" -> "easier"

Different parts:
"input text" -> "provided text"
"my complex sentence" -> "the difficult sentence"
"simpler text" -> "easier language"
"simpler terms, but keep the meaning" -> "simpler words while maintaining the meaning"

3. Combine the different parts with Prompt 3, selectively replace it with the different parts in step 2 and generate a new prompt:
Prompt 3: Rewrite my complex sentence in simpler terms, but keep the meaning.
New Prompt: Transform the difficult sentence in easier words while maintaining the meaning.

4. Crossover the prompt in step 3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: Make the sentence easier for people who do not speak English fluently to comprehend.
Final Prompt: <prompt>Transform the difficult sentence in easier words while maintaining the meaning to make it easier for people who do not speak English fluently to comprehend.</prompt>

Please follow the instruction step-by-btep to generate a better prompt.
1. Identify the same parts and the different parts between Prompt 1 and Prompt 2:
Prompt 1: {p_contr}
Prompt 2: {p_best}
2. Randomly mutate the same parts and the different parts.
3. Combine the same parts and the different parts with Prompt 3, selectively replace it with the same parts and the different parts in step 2 and generate a new prompt.
Prompt 3: {p_best}
4. Crossover the prompt in the step3 with the following basic prompt and generate a final prompt bracketed with <prompt> and </prompt>:
Basic Prompt: {p_i}

1. """,

    # p_contr: mutated from p_worst in high_pop and random p_init
    # p_best: the prompt is with the highest score
    # p_i: the prompt to crossover
    "CoEvo_compare": \
""""Please follow the instruction step-by-btep to generate a better prompt.
1. Identify the same parts and the different parts between worse prompt and normal prompt:
worse prompt: Rewrite the input text into simpler text.
normal prompt: Rewrite my complex sentence in simpler terms, but keep the meaning.
2. Randomly mutate the same parts and the different parts.
3. Combine the same parts and the different parts with normal prompt, selectively replace it with the same parts and the different parts in step 2 and generate a new prompt.
normal prompt: Rewrite my complex sentence in simpler terms, but keep the meaning.
4. Crossover the prompt in the step 3 with the following basic prompt and generate a better prompt bracketed with <prompt> and </prompt>:
basic prompt: Make the sentence easier for people who do not speak English fluently to comprehend.

1.  Same parts:
"rewrite"
"simpler"

Different parts:
"input text" vs "my complex sentence"
"simpler text" vs "simpler terms, but keep the meaning"

2. Same parts:
"rewrite" -> "transform"
"simpler" -> "easier"

Different parts:
"input text" -> "provided text"
"my complex sentence" -> "the difficult sentence"
"simpler text" -> "easier language"
"simpler terms, but keep the meaning" -> "simpler words while maintaining the meaning"

3. new prompt: Transform the difficult sentence in easier words while maintaining the meaning.

4. <prompt>Transform the difficult sentence in easier words while maintaining the meaning to make it easier for people who do not speak English fluently to comprehend.</prompt>

Please follow the instruction step-by-btep to generate a better prompt.
1. Identify the same parts and the different parts between worse prompt and normal prompt:
worse prompt: {p_contr}
normal prompt: {p_best}
2. Randomly mutate the same parts and the different parts.
3. Combine the same parts and the different parts with normal prompt, selectively replace it with the same parts and the different parts in step 2 and generate a new prompt.
normal prompt: {p_best}
4. Crossover the prompt in the step 3 with the following basic prompt and generate a better prompt bracketed with <prompt> and </prompt>:
basic prompt: {p_i}

1. """,

}

TEMPLATE_EVOLUTION = {
    "ReSS": {
        "English": TEMPLATE_RESS_ENGLISH,
    },
    "EvoPrompt": {
        "English": TEMPLATE_EVOPROMPT_ENGLISH,
    },
}
