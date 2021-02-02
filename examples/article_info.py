import wikihowunofficialapi as wha

# Some edge cases -
# Expert article with no votes: https://www.wikihow.com/Photograph-the-Sun
# Article with gifs in place of images: https://www.wikihow.com/Clean-a-Solder-Iron

article = wha.Article('https://www.wikihow.com/Train-a-Dog')


print(article.url)
print(article.title)
print(article.intro)
# print(article.summary)
print(article.n_methods)
print(article.methods)
print(article.num_votes)
print(article.percent_helpful)
print(article.is_expert)
print(article.last_updated)
print(article.views)

first_method = article.methods[0]
first_step = first_method.steps[0]
print(first_step)
print(first_step.title)
print(first_step.description)
print(first_step.picture)
