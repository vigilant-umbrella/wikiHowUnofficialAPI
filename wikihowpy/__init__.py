"""
wikihowpy

API to extract data from wikiHow.
"""

__version__ = '0.1.0'
__author__ = 'mlcpp'
__credits__ = 'Aniket Sharma & Ashok Arora'

from bs4 import BeautifulSoup
import urllib.request
from pywikihow.exceptions import *


class Article:
    def __init__(self, url='https://www.wikihow.com/Special:Randomizer', lazy=True):
        self._url = url
        self._title = None
        self._parsed = False
        if not lazy:
            self._parse()

    def __repr__(self):
        return self.title

    @property
    def url(self):
        if not self._parsed:
            self._parse()
        return self._url

    @property
    def title(self):
        if not self._parsed:
            self._parse()
        return self._title

    def _parse_title(self, soup):
        html = soup.findAll(
            'h1', {'class': ['title_lg', 'title_md', 'title_sm']})[0]
        if not html.find('a'):
            raise ParseError
        else:
            self._url = html.find('a').get('href')
            if not self._url.startswith('http'):
                self._url = 'http://' + self._url
            self._title = self._url.split('/')[-1].replace('-', ' ')

    def _parse(self):
        try:
            content = urllib.request.urlopen(self._url)
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            self._parse_title(soup)
            self._parsed = True
        except Exception as e:
            raise ParseError

    def get(self):
        return {
            'url': self._url,
            'title': self.title,
            'intro': self._intro,
            'n_steps': self.n_steps,
            'steps': self.steps,
            'summary': self.summary
        }


def random_article(lang='en'):
    return Article()


if __name__ == '__main__':
    exit()
