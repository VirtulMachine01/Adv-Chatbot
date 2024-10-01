from langchain.prompts import PromptTemplate

# Map reduce prompts
map_prompt_template = """
Write a summary of this chunk of text that includes the main points and any important details.
{text}
"""

main_prompt = PromptTemplate(template = map_prompt_template, input_variables=["text"])

combined_prompt_template = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
BULLET POINT SUMMARY:
"""


# Refine PROMPTS
question_prompt_template = """
Please provide a summary of the following text.
TEXT: {text}
SUMMARY:
"""

question_prompt = PromptTemplate(template = question_prompt_template, input_variables=["text"])

refine_prompt_template = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
BULLET POINT SUMMARY:
"""

refine_prompt = PromptTemplate(
    template=refine_prompt_template, input_variables=["text"]
)


# PROMPT FOR TITLE
combine_prompt = PromptTemplate(
    template=combined_prompt_template, input_variables=["text"]
)

combined_title_prompt_template = """
Give a title of 3-4 words to the following text delimited by triple backquotes.
```{text}```
"""

title_prompt = PromptTemplate(
    template=combined_title_prompt_template, input_variables=["text"]
)