import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()
os.environ['GROQ_API_KEY'] = "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"
# os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# LLm model using GOQ online but versy fast but limits
# llm = ChatGroq(model_name = "llama-3.1-70b-versatile")
llm = ChatGroq(model_name = "llama-3.1-8b-instant")

# LLM model using Ollama on system offline
# from langchain_community.llms import Ollama
# llm = Ollama(model="llama3:latest")

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
    
from langchain.chains import load_summarize_chain
from prompt_template import combine_prompt, main_prompt, title_prompt, question_prompt, refine_prompt
from pathlib import Path
import pandas as pd

# Map reduce Chain
def create_map_reduce_chain(llm, main_prompt, combine_prompt, chain_type="map_reduce"):
    map_reduce_chain = load_summarize_chain(
        llm=llm,
        chain_type=chain_type,
        map_prompt = main_prompt,
        combine_prompt=combine_prompt,
        return_intermediate_steps = True,    
    )
    return map_reduce_chain

def summarize_map_reduce(translated_docs):
    map_reduce_chain = create_map_reduce_chain(llm, main_prompt,combine_prompt)
    response = map_reduce_chain({"input_documents":translated_docs})
    return response

def title_of_document_map_reduce(translated_docs):
    map_reduce_chain = create_map_reduce_chain(llm, main_prompt, title_prompt)
    response = map_reduce_chain({"input_documents":translated_docs})
    return response

# Refine Chain
def create_refine_chain(llm, question_prompt, refine_prompt, chain_type="map_reduce"):
    refine_chain = load_summarize_chain(
        llm=llm,
        chain_type=chain_type,
        map_prompt=question_prompt,
        combine_prompt=refine_prompt,
        return_intermediate_steps = True,
    )
    return refine_chain
def summarize_refine(translated_docs):
    map_reduce_chain = create_refine_chain(llm, question_prompt, refine_prompt)
    response = map_reduce_chain({"input_documents":translated_docs})
    return response

def title_of_document_refine(translated_docs):
    map_reduce_chain = create_refine_chain(llm, question_prompt, title_prompt)
    response = map_reduce_chain({"input_documents":translated_docs})
    return response

# Page wise content data frame and summary
def page_wise_content(response):
    final_mp_data = []
    for doc, out in zip(response["input_documents"], response["intermediate_steps"]):
        output = {}
        output["file_name"] = Path(doc.metadata["source"]).stem
        output["file_type"] = Path(doc.metadata["source"]).suffix
        output["page_number"] = doc.metadata["page"]
        output["chunks"] = doc.page_content
        output["concise_summary"] = out
        final_mp_data.append(output)
    return final_mp_data

def make_data_frame(response):
    final_data_list = page_wise_content(response)
    pdf_mp_summary = pd.DataFrame.from_dict(final_data_list)
    pdf_mp_summary = pdf_mp_summary.sort_values(by=["file_name", "page_number"])
    pdf_mp_summary.reset_index(inplace=True, drop=True)
    return pdf_mp_summary

def page_wise_summary(data_frame, page_number = 0, data = "concise_summary"):
    return data_frame[data].iloc[page_number]