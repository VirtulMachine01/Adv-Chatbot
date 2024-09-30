from langchain.prompts import PromptTemplate

# Map reduce prompts
map_prompt_template = """
Write a summary of this chunk of text that includes the main points and any important details. just write in 40-50 words.
{text}
"""

main_prompt = PromptTemplate(template = map_prompt_template, input_variables=["text"])

combined_prompt_template = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
BULLET POINT SUMMARY:
"""

combine_prompt = PromptTemplate(
    template=combined_prompt_template, input_variables=["text"]
)