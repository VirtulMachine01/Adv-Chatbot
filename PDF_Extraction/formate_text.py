import re

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