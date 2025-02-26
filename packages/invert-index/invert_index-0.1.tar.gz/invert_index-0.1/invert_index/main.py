"""
inverted_index.py

A simple library for creating and searching inverted indexes.
"""

import re
import pprint

def create_inverted_index(documents):
    """
    Creates an inverted index from a dictionary of documents.

    Args:
        documents: A dictionary where keys are document IDs and values are document text.

    Returns:
        An inverted index (dictionary) where keys are terms and values are lists of document IDs.
    """
    inverted_index = {}
    for doc_id, text in documents.items():
        words = re.findall(r'\w+', text.lower())
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = []
            if doc_id not in inverted_index[word]:
                inverted_index[word].append(doc_id)
    return inverted_index

def search(inverted_index, query):
    """
    Searches the inverted index for the given query.

    Args:
        inverted_index: The inverted index.
        query: The search query (string).

    Returns:
        A list of document IDs that match the query.
    """
    query_words = re.findall(r'\w+', query.lower())
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
