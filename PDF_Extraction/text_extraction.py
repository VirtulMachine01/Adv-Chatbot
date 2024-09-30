
from langchain_community.document_loaders import UnstructuredPowerPointLoader, PyPDFLoader
import os

TEMP_FILE_NAME = "temp_uploaded_file."

def get_filetype(uploaded_file):
    return uploaded_file.name.split('.')[-1]

def generate_temp_file(uploaded_file):
    file_type = get_filetype(uploaded_file)
    with open(f"{TEMP_FILE_NAME}{file_type}", "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    return f"{TEMP_FILE_NAME}{file_type}"

def delete_temp_file(file_type):
    os.remove(f"{TEMP_FILE_NAME}{file_type}")

def extract_text_from_ppt_pagewise(uploaded_file):
    file = generate_temp_file(uploaded_file)
    loader = UnstructuredPowerPointLoader(file, mode="elements")
    documents = loader.load()

    # Dictionary to hold text grouped by page number
    pagewise_text = {}

    # Group text based on page_number and avoid empty page content
    for doc in documents:
        page_number = doc.metadata.get("page_number", None)

        # Skip pages with None or empty content
        if page_number is None or not doc.page_content.strip():
            continue  # Skip this entry if no page number or content is empty

        # Initialize the key if not already present and concatenate text
        if page_number not in pagewise_text:
            pagewise_text[page_number] = doc.page_content
        else:
            pagewise_text[page_number] += f" {doc.page_content}"  # Concatenate with a space for better readability

    # Convert the grouped text to a list, sorted by page number
    list_docs = [text for _, text in sorted(pagewise_text.items())]

    delete_temp_file(get_filetype(uploaded_file))
    return list_docs

def extract_text_from_pdf_pagewise(uploaded_file):
    pdf_file = generate_temp_file(uploaded_file)
    pdf_loader = PyPDFLoader(pdf_file)
    documents = pdf_loader.load_and_split()
    list_docs = []    
    for doc in documents:
        list_docs.append(doc.page_content)
    return list_docs

# Return textlist with chinese content
# import pdfplumber
# def extract_text_from_pdf_pagewise(pdf_path):
#     pages_text = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             if text:
#                 pages_text.append(text)
#     return pages_text