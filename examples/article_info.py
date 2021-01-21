from wikihowpy import *

article = Article("https://www.wikihow.com/Train-a-Dog")
info = article.get()

print(info['url'])
print(info['title'])
print(info['intro'])
print(info['n_steps'])
print(info['steps'])
print(info['summary'])

first_step = info['steps'][0]
print(first_step)
print(first_step.description)
print(first_step.summary)
print(first_step.picture)
