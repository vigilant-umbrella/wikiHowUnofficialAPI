from wikihowpy import *

article = Article('https://www.wikihow.com/Train-a-Dog')
info = article.get()


print(info['url'])
print(info['title'])
print(info['intro'])
# print(info['summary'])
print(info['n_methods'])
print(info['methods'])
print(info['num_votes'])
print(info['percent_helpful'])
print(info['is_expert'])
print(info['last_updated'])
print(info['views'])

first_method = article.methods[0]
first_step = first_method.steps[0]
print(first_step)
print(first_step.title)
print(first_step.description)
print(first_step.picture)
