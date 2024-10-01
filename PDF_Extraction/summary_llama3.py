from text_extraction import extract_text_from_pdf_pagewise, extract_text_from_ppt_pagewise
from translation import translate_extracted_text_list
from generate_pdf import generate_text_pdf
from llm_call import get_domain_of_document, summarize_text_stuff
# from formate_text import break_long_words_in_text_list
import streamlit as st
import time

# Streamlit UI
st.title("PDF Summary Translator")
st.write("Upload a PDF file containing Chinese text, and get an English summary.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "ppt", "pptx"])

if uploaded_file is not None:
    start_time_main = time.time()

    file_type = uploaded_file.name.split('.')[-1]

    page_docs = None

    if file_type == "pdf":
        # Extract text from the PDF
        with st.spinner("Extracting text from the PDF..."):
            page_docs = extract_text_from_pdf_pagewise(uploaded_file)  # List of text per page
    elif file_type in ["ppt", "pptx"]:
        # Extract text from the PDF
        with st.spinner("Extracting text from the PDF..."):
            page_docs = extract_text_from_ppt_pagewise(uploaded_file)
    else:
        st.write(f"Unsupported file type: {uploaded_file.type}")

    st.write(f"Extraction Time: {(time.time() - start_time_main):.2f} seconds")
    start_time_main1 = time.time()
    if page_docs:
        # Process the long text for translation and summarization
        with st.spinner("Translating Text..."):
            translated_docs = translate_extracted_text_list(page_docs)
            print(len(translated_docs))

        st.write(f"Translation Time: {(time.time() - start_time_main1):.2f} seconds")
        start_time_main1 = time.time()

        with st.spinner("Generating PDF..."):
            generate_text_pdf(translated_docs)

        st.write(f"PDF Generation Time: {(time.time() - start_time_main1):.2f} seconds")
        start_time_main1 = time.time()

        combined_translated_text = " ".join(translated_docs)
        st.write("Total Tokens:", len(combined_translated_text))

        with st.spinner("Generating Title..."):
            if combined_translated_text.strip():  # Check if there's any valid translated text
                domain_name = get_domain_of_document(combined_translated_text)
            else:
                print("No valid translated text available for summarization.", "", "")

        st.write(f"Title Time: {(time.time() - start_time_main1):.2f} seconds")
        start_time_main1 = time.time()

        with st.spinner("Generating Summary..."):
            if combined_translated_text.strip():  # Check if there's any valid translated text
                english_summary = summarize_text_stuff(combined_translated_text)
            else:
                print("No valid translated text available for summarization.", "", "")

        st.write(f"Summary Time: {(time.time() - start_time_main1):.2f} seconds")
        start_time_main1 = time.time()

        # Display the domain name and summary
        st.subheader("Title of Document:")
        st.write(domain_name)

        st.subheader("Summary:")
        st.write(english_summary)

        # Show original extracted text with page separations in an expander
        with st.expander("See extracted text from PDF"):
            for i, page_text in enumerate(page_docs, 1):
                st.write(f"**Page {i}:**\n\n{page_text}")  # Show each page separately

        # Show the translated text with page separations in an expander
        with st.expander("See translated text with page breaks"):
            # updated_translated_text_list = break_long_words_in_text_list(translated_text_list, max_length=15)
            for i, page_text in enumerate(translated_docs, 1):
                st.write(f"**Page {i}:**\n\n{page_text}")
        
        st.write(f"Total time taken for the entire process: {(time.time() - start_time_main):.2f} seconds")
    else:
        st.warning("No text could be extracted from the PDF.")

# from text_extraction import extract_documents_from_pdf, extract_documents_from_ppt
# from llm_call import make_data_frame, page_wise_summary, title_of_document_refine, summarize_refine
# from translation import translate_document
# if uploaded_file is not None:
#     start_time_main = time.time()

#     file_type = uploaded_file.name.split('.')[-1]

#     page_docs = None

#     if file_type == "pdf":
#         # Extract text from the PDF
#         with st.spinner("Extracting text from the PDF..."):
#             page_docs = extract_documents_from_pdf(uploaded_file)  # List of text per page
#     elif file_type in ["ppt", "pptx"]:
#         # Extract text from the PDF
#         with st.spinner("Extracting text from the PDF..."):
#             page_docs = extract_documents_from_ppt(uploaded_file)
#     else:
#         st.write(f"Unsupported file type: {uploaded_file.type}")

#     st.write(f"Extraction Time: {(time.time() - start_time_main):.2f} seconds")
#     start_time_main1 = time.time()
#     if page_docs:
#         # Process the long text for translation and summarization
#         with st.spinner("Translating Text..."):
#             translated_docs = translate_document(page_docs)

#         st.write(f"Translation Time: {(time.time() - start_time_main1):.2f} seconds")
#         start_time_main1 = time.time()

#         with st.spinner("Generating PDF..."):
#             translated_docs_list =[]    
#             for doc in translated_docs:
#                 translated_docs_list.append(doc.page_content)
#             generate_text_pdf(translated_docs_list)

#         st.write(f"PDF Generation Time: {(time.time() - start_time_main1):.2f} seconds")
#         start_time_main1 = time.time()

#         with st.spinner("Generating Title..."):
#             # domain_name = title_of_document(translated_docs)
#             domain_name = title_of_document_refine(translated_docs)

#         st.write(f"Title Time: {(time.time() - start_time_main1):.2f} seconds")
#         start_time_main1 = time.time()

#         with st.spinner("Generating Summary..."):
#             # english_summary = summarize_map_reduce(translated_docs)
#             english_summary = summarize_refine(translated_docs)

#         st.write(f"Summary Time: {(time.time() - start_time_main1):.2f} seconds")
#         start_time_main1 = time.time()

#         # Display the domain name and summary
#         st.subheader("Title of Document:")
#         st.write(domain_name['output_text'])

#         st.subheader("Summary:")
#         st.write(english_summary['output_text'])

#         # Show original extracted text with page separations in an expander
#         with st.expander("See extracted text from PDF"):
#             for i, page_text in enumerate(page_docs, 1):
#                 st.write(f"**Page {i}:**\n\n{page_text.page_content}")  # Show each page separately

#         # Show the translated text with page separations in an expander
#         with st.expander("See translated text with page breaks"):
#             for i, page_text in enumerate(translated_docs_list, 1):
#                 st.write(f"**Page {i}:**\n\n{page_text}")
        
#         with st.expander("See the Page wise Summary"):
#             sum_df = make_data_frame(english_summary)
#             for i, page_text in enumerate(translated_docs_list, 1):
#                 st.write(f"**Page {i}:**\n\n{page_wise_summary(sum_df, i-1, "concise_summary")}")
        
#         st.write(f"Total time taken for the entire process: {(time.time() - start_time_main):.2f} seconds")
#     else:
#         st.warning("No text could be extracted from the PDF.")