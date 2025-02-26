# usage

 documents = {
     "doc1": "Python is Awesome.",
     "doc2": "Python is Perfect",
     "doc3": "Cpp is great."
 }

inverted_index = create_inverted_index(documents)
print_inverted_index(inverted_index)
print(search(inverted_index, "python"))
