""" Stress Testing to ensure there are no errors generate while parsing """

import random
from tqdm import tqdm
import wikihowunofficialapi as wha
from wikihowunofficialapi import exceptions

try:
    num = 500
    lang = ['en',
            'es',
            'pt',
            'it',
            'fr',
            'ru',
            'de',
            'zh',
            'nl',
            'cz',
            'id',
            'jp',
            'hi',
            'th',
            'ar',
            'ko',
            'tr',
            'vn']
    print('Stress Testing...')
    for _ in tqdm(range(num)):
        ra = wha.random_article(random.choice(lang))
        ra.url
        ra.title
        ra.intro
        ra.n_methods
        ra.methods
        ra.num_votes
        ra.percent_helpful
        ra.is_expert
        ra.last_updated
        ra.views
        ra.co_authors
        ra.references
        ra.summary
        ra.warnings
        ra.tips

    print('Testing Passed')

except exceptions.ParseError:
    print('Testing Failed: ParseError')
    print('Report the error with the way to reproduce it at https://github.com/vigilant-umbrella/wikiHowUnofficialAPI/issues or vigilant.umbrella@gmail.com')
except exceptions.UnsupportedLanguage:
    print('Testing Failed: UnsupportedLanguage')
    print('Report the error with the way to reproduce it at https://github.com/vigilant-umbrella/wikiHowUnofficialAPI/issues or vigilant.umbrella@gmail.com')
except Exception as e:
    print('Testing Failed: ' + str(e))
    print('Report the error with the way to reproduce it at https://github.com/vigilant-umbrella/wikiHowUnofficialAPI/issues or vigilant.umbrella@gmail.com')
