from invert_index import create_inverted_index, print_inverted_index, search

documents = {
    "doc1": "Python is Awesome.",
    "doc2": "Python is Perfect",
    "doc3": "Cpp is great."
}

inverted_index = create_inverted_index(documents)

print_inverted_index(inverted_index)

print(search(inverted_index, "python"))