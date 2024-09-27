from deep_translator import GoogleTranslator
import textwrap
import streamlit as st
import pdfplumber
from langchain_groq import ChatGroq
import os
import re
import time
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

summarization_model = ChatGroq(model_name = "llama-3.1-70b-versatile")
# summarization_model = ChatGroq(model_name = "llama-3.1-8b-instant")

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n\n\n\n"
    return all_text

def extract_text_from_pdf_pagewise(pdf_path):
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
    return pages_text

def translate_text(text):
    """Translate Chinese text to English using Deep Translator."""
    try:
        translated_text = GoogleTranslator(source='zh-CN', target='en').translate(text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

def get_doman_of_document(text):
    """Get the domain of the document."""
    try:
        # Check if text is not empty
        if len(text) > 0:
            # Ensure the text is within the summarization model's limits
            text = f"From the given content give the domain of document in 2 words only. Document is '{text}'"
            domain_name = summarization_model.invoke(text)
            return domain_name
        else:
            print("No text to domain.")
            return ""
    except Exception as e:
        print(f"Error during domain finding: {e}")
        return ""

def summarize_text(text):
    """Summarize English text."""    
    try:
        # Check if text is not empty
        if len(text) > 0:
            # Ensure the text is within the summarization model's limits
            text = f"Summarize the following text in 100-200 words only. '{text}'"
            summary = summarization_model.invoke(text)
            return summary
        else:
            print("No text to summarize.")
            return ""
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""

# def process_long_text(long_text, chunk_size=1000):
#     """Process a long text: translate and summarize."""
#     # Split the long text into manageable chunks
#     chunks = textwrap.wrap(long_text, width=chunk_size, break_long_words=False)
    
#     translated_chunks = []
#     for chunk in chunks:
#         translated_chunk = translate_text(chunk)
#         if translated_chunk:  # Ensure translated chunk is not empty
#             translated_chunks.append(translated_chunk)
    
#     # Combine all translated chunks
#     combined_translated_text = " ".join(translated_chunks)
#     st.write("Total Tokens:- ",len(combined_translated_text)) # +54 other
#     # print(combined_translated_text)

#     # Only summarize if we have valid translated text
#     if combined_translated_text.strip():  # Check if there's any valid translated text
#         summary = summarize_text(combined_translated_text)
#         domain_name = get_doman_of_document(combined_translated_text)
#         return summary.content, domain_name.content, combined_translated_text
#     else:
#         return "No valid translated text available for summarization."

def process_long_text(pages_text, chunk_size=1000):
    """Process each page of text separately: translate and summarize."""
    translated_pages = []
    for page in pages_text:
        # Translate each page separately
        translated_text = translate_text(page)
        if translated_text:
            translated_pages.append(translated_text)  # Append translated page
    # Combine all translated pages with a delimiter
    combined_translated_text = " ".join(translated_pages)
    
    # Display total tokens and translated text (optional)
    st.write("Total Tokens:", len(combined_translated_text))  # +54 other overheads

    # Only summarize if we have valid translated text
    if combined_translated_text.strip():  # Check if there's any valid translated text
        summary = summarize_text(combined_translated_text)
        domain_name = get_doman_of_document(combined_translated_text)
        return summary.content, domain_name.content, translated_pages
    else:
        return "No valid translated text available for summarization.", "", ""

def split_long_word(word, max_length=15):
    """
    Split a long word into smaller segments of 'max_length' characters or intelligently insert spaces.
    """
    # If the word length is already acceptable, return it as is
    if len(word) <= max_length:
        return word

    # Check if the word contains meaningful patterns (e.g., CamelCase or hyphens)
    segments = re.findall(r'[a-z]+|[A-Z][a-z]*', word)
    
    # If the word can be split into segments (e.g., CamelCase), return with spaces
    if len("".join(segments)) < len(word):
        return " ".join(segments)
    else:
        # Otherwise, insert a space every max_length characters
        return " ".join([word[i:i + max_length] for i in range(0, len(word), max_length)])


def break_long_words_in_text_list(text_list, max_length=15):
    """
    Process each page's translated text in the list and break long words into smaller ones.
    
    Args:
        text_list (list): List of translated text for each page.
        max_length (int): Maximum length of a word before it gets broken down.
        
    Returns:
        list: Updated text list with long words broken down.
    """
    # Initialize an empty list to store updated text for each page
    updated_text_list = []
    
    for page_text in text_list:
        # Split the page text into individual words
        words = page_text.split()

        # Process each word to check for long words and break them down if necessary
        formatted_words = [split_long_word(word, max_length) for word in words]

        # Rejoin the words to form the updated page content
        formatted_page_text = " ".join(formatted_words)

        # Append the updated page content to the new list
        updated_text_list.append(formatted_page_text)
    
    return updated_text_list


# Streamlit UI
st.title("PDF Summary Translator")
st.write("Upload a PDF file containing Chinese text, and get an English summary.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    start_time_main = time.time()
    # Extract text from the PDF
    with st.spinner("Extracting text from the PDF..."):
        pages_text = extract_text_from_pdf_pagewise(uploaded_file)  # List of text per page

    if pages_text:
        # Process the long text for translation and summarization
        with st.spinner("Generating Summary..."):
            english_summary, domain_name, translated_text_list = process_long_text(pages_text)

        # Display the domain name and summary
        st.subheader("Title of Document:")
        st.write(domain_name)

        st.subheader("Summary:")
        st.write(english_summary)

        # Show original extracted text with page separations in an expander
        with st.expander("See extracted text from PDF"):
            for i, page_text in enumerate(pages_text, 1):
                st.write(f"**Page {i}:**\n\n{page_text}")  # Show each page separately

        # Show the translated text with page separations in an expander
        with st.expander("See translated text with page breaks"):
            updated_translated_text_list = break_long_words_in_text_list(translated_text_list, max_length=15)
            for i, page_text in enumerate(updated_translated_text_list, 1):
                st.write(f"**Page {i}:**\n\n{page_text}")
        
        st.write(f"Total time taken for the entire process: {(time.time() - start_time_main):.2f} seconds")
    else:
        st.warning("No text could be extracted from the PDF.")

# if uploaded_file is not None:
#     # Extract text from the PDF
#     with st.spinner("Extracting text from the PDF..."):
#         extracted_text = extract_text_from_pdf(uploaded_file)

#     if extracted_text:
#         # Process the long text
#         with st.spinner("Generating Summary..."):
#             english_summary, domain_name, translated_text = process_long_text(extracted_text)

#         # Display the summary
#         st.subheader("Doamain of Document:")
#         st.write(domain_name)

#         st.subheader("Summary:")
#         st.write(english_summary)

#         with st.expander("See extracted text from PDF"):
#             st.write(extracted_text)

#         with st.expander("See Translated text from PDF"):
#             st.write(translated_text)
#     else:
#         st.warning("No text could be extracted from the PDF.")