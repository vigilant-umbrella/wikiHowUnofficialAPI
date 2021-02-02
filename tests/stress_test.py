""" Stress Testing to ensure there are no errors generate while parsing """


import wikihowunofficialapi as wha
from tqdm import tqdm
from wikihowunofficialapi import exceptions

try:
    print('Stress Testing...')
    num = 500
    for _ in tqdm(range(num)):
        ra = wha.random_article()
        ra.url

    print('Testing Passed')

except exceptions.ParseError:
    print('Testing Failed: ParseError')
    print('Report the error with tha way to reproduce it at vigilant.umbrella@gmail.com')
except exceptions.UnsupportedLanguage:
    print('Testing Failed: UnsupportedLanguage')
    print('Report the error with tha way to reproduce it at vigilant.umbrella@gmail.com')
except Exception as e:
    print('Testing Failed: ' + str(e))
    print('Report the error with tha way to reproduce it at vigilant.umbrella@gmail.com')
