import wikihowunofficialapi as wha

search_text = 'тест'  # 'test' in russian
max_results = 1
how_tos = wha.search_wikihow(search_text, max_results, lang='ru')
print(how_tos[0])

# Search and print all articles for a given query
for how_to in wha.WikiHow.search(search_text, lang='ru'):
    print(how_to)
