import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensure you download the necessary NLTK resources
nltk.download('punkt')

def generate_tokens(translated_text_list, num_tokens=100):
    """
    Generate a list of tokens from the list of translated English text segments, excluding common stop words.

    Parameters:
    - translated_text_list (list[str]): The list of translated English text segments from the PDF.
    - num_tokens (int): The number of tokens to generate.

    Returns:
    - List[str]: A list of tokens related to the document.
    """
    # Expanded custom list of stop words to exclude
    custom_stop_words = set([
        'is', 'a', 'an', 'are', 'the', 'and', 'of', 'in', 'to', 'that', 
        'this', 'for', 'on', 'it', 'with', 'as', 'at', 'by', 'from', 
        'or', 'but', 'not', 'be', 'can', 'will', 'if', 'have', 'has', 
        'do', 'does', 'were', 'been', 'more', 'some', 'than', 'we', 
        'you', 'he', 'she', 'they', 'his', 'her', 'their', 'its', 
        'my', 'our', 'your', 'me', 'us', 'them', 'such', 'just', 
        'only', 'so', 'then', 'which', 'who', 'whom', 'when', 
        'where', 'why', 'how', 'if', 'as', 'like', 'about', 
        'also', 'very', 'many', 'much', 'no', 'not', 'all', 
        'any', 'each', 'every', 'both', 'few', 'more', 'most', 
        'other', 'another', 'some', 'any', 'same', 'now', 'than', 
        'through', 'over', 'under', 'into', 'onto', 'before', 
        'after', 'during', 'between', 'against', 'without', 
        'within', 'among', 'about', 'above', 'below', 'toward', 
        'across', 'along', 'upon', 'like', 'but', 'for', 'nor', 
        'yet', 'so', 'either', 'neither', 'if', 'whether', 
        'although', 'while', 'because', 'since', 'until', 
        'unless', 'while', 'whereas', 'despite', 'although', 
        'though', 'although', 'even', 'if', 'but', 'still', 
        'yet', 'so', 'then', 'then', 'and', 'also', 'as', 
        'thus', 'hence', 'therefore', 'while', 'whether'
    ])

    # Concatenate the list into a single string
    combined_text = ' '.join(translated_text_list)

    # Tokenize the text
    tokens = word_tokenize(combined_text)

    # Convert to lowercase and filter out non-alphanumeric tokens and custom stop words
    filtered_tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in custom_stop_words]

    # Count frequency of each token
    token_counts = Counter(filtered_tokens)

    # Get the most common tokens
    most_common_tokens = token_counts.most_common(num_tokens)

    # Extract just the tokens from the list of tuples
    token_list = [token for token, count in most_common_tokens]

    return token_list