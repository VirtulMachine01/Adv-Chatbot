
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

from collections import defaultdict
from langchain.schema import Document

def merge_documents_by_page(documents):
    # Use defaultdict to group content by page_number
    merged_pages = defaultdict(str)  # Dictionary to store merged content for each page_number
    metadata_by_page = {}  # Dictionary to store metadata for each page_number
    
    for doc in documents:
        page_number = doc.metadata.get('page_number', None)
        if page_number is not None:
            # Merge content for the same page number
            merged_pages[page_number] += doc.page_content + "\n"  # Add a newline between merged contents
            # Store the metadata (we'll use the metadata from the first occurrence of each page number)
            if page_number not in metadata_by_page:
                metadata_by_page[page_number] = doc.metadata
    
    # Create new Document objects with the merged content
    merged_documents = []
    for page_number, content in merged_pages.items():
        # Create a new Document object with merged content and metadata
        merged_doc = Document(
            page_content=content.strip(),  # Strip to remove any extra leading/trailing spaces or newlines
            metadata=metadata_by_page[page_number]
        )
        merged_documents.append(merged_doc)

    return merged_documents


def extract_documents_from_ppt(uploaded_file):
    file = generate_temp_file(uploaded_file)
    loader = UnstructuredPowerPointLoader(file, mode="elements")
    documents = loader.load()
    merged_docs = merge_documents_by_page(documents)
    delete_temp_file(get_filetype(uploaded_file))
    return merged_docs

def extract_documents_from_pdf(uploaded_file):
    pdf_file = generate_temp_file(uploaded_file)
    pdf_loader = PyPDFLoader(pdf_file)
    documents = pdf_loader.load_and_split()
    delete_temp_file(get_filetype(uploaded_file))
    return documents







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