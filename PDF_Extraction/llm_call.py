import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from translation import translate_document


load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# llm = ChatGroq(model_name = "llama-3.1-70b-versatile")
llm = ChatGroq(model_name = "llama-3.1-8b-instant")

def get_domain_of_document(text):
    """Get the domain of the document."""
    try:
        # Check if text is not empty
        if len(text) > 0:
            # Ensure the text is within the summarization model's limits
            text = f"From the given content give the domain of document in four(4) words only. Document is '{text}'"
            domain_name = llm.invoke(text)
            # Check if the response has the expected content field
            if hasattr(domain_name, 'content'):
                return domain_name.content
            else:
                # print("No valid content found in the response.")
                return "No valid content found in the response."
        else:
            # print("No text to determine the domain.")
            return "No text to determine the domain."
    except Exception as e:
        # print(f"Error during domain finding: {e}")
        return "Error during domain finding: {e}"

def summarize_text_stuff(text):
    """Summarize English text."""    
    try:
        # Check if text is not empty
        if len(text) > 0:
            # Ensure the text is within the summarization model's limits
            text = f"Summarize the following text in 100-200 words only. '{text}'"
            summary = llm.invoke(text)

            # # Check if the response has the expected content field
            if hasattr(summary, 'content'):
                return summary.content
            else:
                # print("No valid content found in the response.")
                return "No valid content found in the response."
        else:
            # print("No text to summarize.")
            return "No text to summarize."
    except Exception as e:
        # print(f"Error during summarization: {e}")
        return "Error during summarization: {e}"
    
# from langchain.chains import load_summarize_chain
# from prompt_template import combine_prompt

# def create_map_reduce_chain(llm, combine_prompt):
#     map_reduce_cahin = load_summarize_chain(
#         llm,
#         chain_type="map_reduce",
#         combine_prompt=combine_prompt,
#         return_intermediate_steps = True,    
#     )
#     return map_reduce_cahin

# def summarize_map_reduce(documents):
#     map_reduce_chain = create_map_reduce_chain(llm, combine_prompt)
#     translated_docs = translate_document(documents)
#     response = map_reduce_chain({"input_documents":translated_docs})
#     return response['output_text']