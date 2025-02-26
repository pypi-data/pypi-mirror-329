"""
inverted_index.py

A simple library for creating and searching inverted indexes with stopword removal.
"""

import re
import pprint


STOPWORDS = {
   'a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an',
   'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 
   'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn',
    "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't",
    'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven',
    "haven't", 'having', 'he', "he'd", "he'll", 'her', 'here', 'hers', 'herself',
    "he's", 'him', 'himself', 'his', 'how', 'i', "i'd", 'if', "i'll", "i'm", 'in',
    'into', 'is', 'isn', "isn't", 'it', "it'd", "it'll", "it's", 'its', 'itself',
    "i've", 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most',
    'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not',
    'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours',
    'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she',
    "she'd", "she'll", "she's", 'should', 'shouldn', "shouldn't", "should've", 'so',
    'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them',
    'themselves', 'then', 'there', 'these', 'they', "they'd", "they'll", "they're", 
    "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 
    'very', 'was', 'wasn', "wasn't", 'we', "we'd", "we'll", "we're", 'were', 'weren', 
    "weren't", "we've", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 
    'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", 
    'your', "you're", 'yours', 'yourself', 'yourselves', "you've"
}

def create_inverted_index(documents, stopwords=STOPWORDS):
    """
    Creates an inverted index from a dictionary of documents, optionally removing stopwords.

    Args:
        documents: A dictionary where keys are document IDs and values are document text.
        stopwords: A set of words to exclude from the index (default: STOPWORDS).

    Returns:
        An inverted index (dictionary) where keys are terms and values are lists of document IDs.
    """
    inverted_index = {}
    for doc_id, text in documents.items():
        words = re.findall(r'\w+', text.lower())
        for word in words:
            if word not in stopwords:  # Check if the word is a stopword
                if word not in inverted_index:
                    inverted_index[word] = []
                if doc_id not in inverted_index[word]:
                    inverted_index[word].append(doc_id)
    return inverted_index

def search(inverted_index, query, stopwords=STOPWORDS):
    """
    Searches the inverted index for the given query, optionally removing stopwords.

    Args:
        inverted_index: The inverted index.
        query: The search query (string).
        stopwords: A set of words to exclude from the search query (default: STOPWORDS).

    Returns:
        A list of document IDs that match the query.
    """
    query_words = [word for word in re.findall(r'\w+', query.lower()) if word not in stopwords]
    result_docs = set()
    if len(query_words) > 0:
        first_word = query_words[0]
        if first_word in inverted_index:
            result_docs.update(inverted_index[first_word])
            for word in query_words[1:]:
                if word in inverted_index:
                    result_docs = result_docs.intersection(set(inverted_index[word]))
                else:
                    return []
        else:
            return []
    return list(result_docs)

def print_inverted_index(inverted_index):
    """
    Prints an inverted index in a readable, vertical format.

    Args:
        inverted_index: The inverted index dictionary.
    """
    pprint.pprint(inverted_index)
