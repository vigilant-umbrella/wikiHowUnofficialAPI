from wikihowpy import *

max_results = 1
how_tos = search_wikihow("sleep", max_results)
print(how_tos[0])

# Search and print all articles for a given query
for how_to in WikiHow.search("sleep"):
    print(how_to)
