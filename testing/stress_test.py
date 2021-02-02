""" Stress Testing to ensure there are no errors generate while parsing """


from tqdm import tqdm
import wikihowpy as wha

try:
    num = 500
    for i in tqdm(range(num)):
        ra = wha.random_article()
        ra.url

    print('Testing Passed')

except:
    print('Testing Failed')
