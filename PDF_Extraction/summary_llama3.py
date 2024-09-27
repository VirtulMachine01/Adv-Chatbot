from deep_translator import GoogleTranslator
import textwrap
import streamlit as st
import pdfplumber
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# summarization_model = ChatGroq(model_name = "llama-3.1-70b-versatile")
summarization_model = ChatGroq(model_name = "llama-3.1-8b-instant")

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n\n\n\n"
    return all_text

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

def process_long_text(long_text, chunk_size=1000):
    """Process a long text: translate and summarize."""
    # Split the long text into manageable chunks
    chunks = textwrap.wrap(long_text, width=chunk_size, break_long_words=False)
    
    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translate_text(chunk)
        if translated_chunk:  # Ensure translated chunk is not empty
            translated_chunks.append(translated_chunk)
    
    # Combine all translated chunks
    combined_translated_text = " ".join(translated_chunks)
    st.write("Total Tokens:- ",len(combined_translated_text)) # +54 other
    # print(combined_translated_text)

    # Only summarize if we have valid translated text
    if combined_translated_text.strip():  # Check if there's any valid translated text
        summary = summarize_text(combined_translated_text)
        domain_name = get_doman_of_document(combined_translated_text)
        return summary.content, domain_name.content, combined_translated_text
    else:
        return "No valid translated text available for summarization."

# Streamlit UI
st.title("PDF Summary Translator")
st.write("Upload a PDF file containing Chinese text, and get an English summary.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from the PDF
    with st.spinner("Extracting text from the PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text:
        # Process the long text
        with st.spinner("Generating Summary..."):
            english_summary, domain_name, translated_text = process_long_text(extracted_text)

        # Display the summary
        st.subheader("Doamain of Document:")
        st.write(domain_name)

        st.subheader("Summary:")
        st.write(english_summary)

        with st.expander("See extracted text from PDF"):
            st.write(extracted_text)

        with st.expander("See Translated text from PDF"):
            st.write(translated_text)
    else:
        st.warning("No text could be extracted from the PDF.")