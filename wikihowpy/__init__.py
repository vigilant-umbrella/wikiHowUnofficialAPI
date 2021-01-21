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


class Steps:
    def __init__(self, number, summary=None, description=None, picture=None):
        self._number = number
        self._summary = summary
        self._description = description
        self._picture = picture

    def __repr__(self, view_description=False):
        return '{} - {}'.format(self.number, self.summary)

    @property
    def number(self):
        return self._number

    @property
    def summary(self):
        return self._summary

    @property
    def description(self):
        return self._description

    @property
    def picture(self):
        return self._picture


class Article:
    def __init__(self, url='https://www.wikihow.com/Special:Randomizer', lazy=True):
        self._url = url
        self._title = None
        self._intro = None
        self._steps = []
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

    @property
    def intro(self):
        if not self._parsed:
            self._parse()
        return self._intro

    @property
    def steps(self):
        if not self._parsed:
            self._parse()
        return self._steps

    @property
    def summary(self):
        summary = self.title + '\n'
        for step in self.steps:
            summary += '{n} - '.format(n=step.number) + step.summary + '\n'
        return summary

    @property
    def n_steps(self):
        return len(self._steps)

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

    def _parse_intro(self, soup):
        intro_html = soup.find('div', {'class': 'mf-section-0'})
        if not intro_html:
            raise ParseError
        else:
            super = intro_html.find('sup')
            if super != None:
                for sup in intro_html.findAll('sup'):
                    sup.decompose()
                    intro = intro_html.text
                    self._intro = intro.strip()
            else:
                intro = intro_html.text
                self._intro = intro.strip()

    def _parse_steps(self, soup):
        self._steps = []
        step_html = soup.findAll('div', {'class': 'step'})
        count = 0
        for html in step_html:
            super = html.find('sup')
            script = html.find('script')
            if script != None:
                for script in html.findAll('script'):
                    script.decompose()
            if super != None:
                for sup in html.findAll('sup'):
                    sup.decompose()
            count += 1
            summary = html.find('b').text

            for _extra_div in html.find('b').find_all('div'):
                summary = summary.replace(_extra_div.text, '')

            step = Steps(count, summary)
            ex_step = html
            for b in ex_step.findAll('b'):
                b.decompose()
            step._description = ex_step.text.strip()
            self._steps.append(step)

    def _parse_pictures(self, soup):
        count = 0
        for html in soup.findAll('a', {'class': 'image'}):
            html = html.find('img')
            i = str(html).find('data-src=')
            pic = str(html)[i:].replace('data-src="', '')
            pic = pic[:pic.find('"')]
            self._steps[count]._picture = pic
            count += 1

    def _parse(self):
        try:
            content = urllib.request.urlopen(self._url)
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            self._parse_title(soup)
            self._parse_intro(soup)
            self._parse_steps(soup)
            self._parse_pictures(soup)
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


def random_article():
    return Article()


if __name__ == '__main__':
    exit()
