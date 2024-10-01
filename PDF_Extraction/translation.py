from deep_translator import GoogleTranslator

def translate_text(text):
    """Translate Chinese text to English using Deep Translator."""
    try:
        translated_text = GoogleTranslator(source='zh-CN', target='en').translate(text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""
    
def translate_extracted_text_list(pages_text):
    translated_pages = []
    for page in pages_text:
        # Translate each page separately
        translated_text = translate_text(page)
        if translated_text:
            translated_pages.append(translated_text)
    return translated_pages


from langchain_core.documents import Document
def translate_document(documents):
    translated_docs = []
    
    for doc in documents:
        # Translate the content
        translated_content = GoogleTranslator(source='zh-CN', target='en').translate(doc.page_content)
        
        # Create a new Document with the translated content
        translated_doc = Document(metadata=doc.metadata, page_content=translated_content)
        
        # Append the new Document to the list
        translated_docs.append(translated_doc)
    
    return translated_docs