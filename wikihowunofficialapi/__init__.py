"""
wikiHowUnofficialAPI

API to extract data from wikiHow.
"""

__version__ = '0.1.0'
__author__ = 'Aniket Sharma, Ashok Arora'
__credits__ = 'Aniket Sharma & Ashok Arora'

from bs4 import BeautifulSoup
import urllib.request
from wikihowunofficialapi.exceptions import *
from datetime import datetime
import re


class Steps:
    def __init__(self, number, title=None, description=None, picture=None):
        self._number = number
        self._title = title
        self._description = description
        self._picture = picture

    def __repr__(self):
        return '{} - {}'.format(self.number, self.title)

    @property
    def number(self):
        return self._number

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def picture(self):
        return self._picture

    def get(self):
        return {
            'number': self.number,
            'title': self.title,
            'description': self.description,
            'picture': self.picture
        }


class Methods:
    def __init__(self, number, title):
        self._number = number
        self._title = title
        self._steps = []

    def __repr__(self):
        return '{} - {}'.format(self.number, self.title)

    @property
    def number(self):
        return self._number

    @property
    def title(self):
        return self._title

    @property
    def steps(self):
        return self._steps

    def get(self):
        return {
            'number': self.number,
            'title': self.title,
            'steps': self.steps
        }


class Article:
    def __init__(self, url='https://www.wikihow.com/Special:Randomizer', lazy=True):
        self._url = url
        self._title = None
        self._intro = None
        self._summary = None
        self._methods = []
        self._num_votes = None
        self._percent_helpful = None
        self._is_expert = None
        self._last_updated = None
        self._views = None
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
    def summary(self):
        if not self._parsed:
            self._parse()
        return self._summary

    @property
    def methods(self):
        if not self._parsed:
            self._parse()
        return self._methods

    @property
    def n_methods(self):
        return len(self._methods)

    @property
    def num_votes(self):
        if not self._parsed:
            self._parse()
        return self._num_votes

    @property
    def percent_helpful(self):
        if not self._parsed:
            self._parse()
        return self._percent_helpful

    @property
    def is_expert(self):
        if not self._parsed:
            self._parse()
        return self._is_expert

    @property
    def last_updated(self):
        if not self._parsed:
            self._parse()
        return self._last_updated

    @property
    def views(self):
        if not self._parsed:
            self._parse()
        return self._views

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

    def _parse_methods(self, soup):
        self._methods = []
        methods_html = soup.findAll(
            'div', {'class': ['section steps steps_first sticky', 'section steps sticky']})
        if not methods_html:
            raise ParseError
        else:
            count = 0
            for method_html in methods_html:
                span = method_html.find('span', {'class': 'mw-headline'})
                count += 1
                title = span.text
                method = Methods(count, title)
                self._methods.append(method)

                step_html = method_html.findAll('div', {'class': 'step'})

                pic_count = 0
                pictures_list = [None] * len(step_html)
                for list_html in method_html.findAll('ol'):
                    for list in list_html.findAll('li', {'id': re.compile('step.+')}):
                        html = list.find('a', {'class': 'image'})
                        # handling case when there are no images or for when there are videos/gifs instead of images
                        if html != None:
                            html = html.find('img')
                            i = str(html).find('data-src=')
                            pic = str(html)[i:].replace('data-src="', '')
                            pic = pic[:pic.find('"')]
                            pictures_list[pic_count] = pic
                        pic_count += 1

                count_steps = 0
                for html in step_html:
                    # exception handling because not all steps have a summary
                    try:
                        super = html.find('sup')
                        script = html.find('script')
                        if script != None:
                            for script in html.findAll('script'):
                                script.decompose()
                        if super != None:
                            for sup in html.findAll('sup'):
                                sup.decompose()
                        count_steps += 1
                        summary = html.find('b').text

                        for _extra_div in html.find('b').find_all('div'):
                            summary = summary.replace(_extra_div.text, '')
                    except:
                        summary = ''

                    step = Steps(count_steps, summary)
                    ex_step = html
                    for b in ex_step.findAll('b'):
                        b.decompose()
                    step._description = ex_step.text.strip()
                    step._picture = pictures_list[count_steps-1]
                    self._methods[count-1]._steps.append(step)

    def _parse_votes_n_helpful(self, soup):
        num_votes_html = soup.find('div', {'class': 'sp_helpful_rating_count'})
        if num_votes_html:
            if str(num_votes_html) == '<div class="sp_helpful_rating_count"></div>':
                return
            content = str(num_votes_html)
            self._num_votes = int(''.join(
                (content[content.find('>')+1: content.find(' votes')]).split(',')))
            self._percent_helpful = int(content[content.find(
                '- ')+2:content.find('%</div>')])

    def _parse_is_expert(self, soup):
        expert_html = soup.find('div', {'id': 'byline_info'})
        if not expert_html:
            raise ParseError
        else:
            b = expert_html.find('b')
            if b:
                self._is_expert = True
            else:
                self._is_expert = False

    def _parse_last_updated(self, soup):
        update_html = soup.find('div', {'id': 'byline_info'})
        if not update_html:
            raise ParseError
        else:
            span = str(update_html.find('span'))
            date = span[span.find(': ')+2:span.find('</span>')]
            self._last_updated = datetime.strptime(date, '%B %d, %Y')

    def _parse_views(self, soup):
        views_html = soup.find('div', {'class': 'sp_box sp_stats_box'})
        if not views_html:
            raise ParseError
        else:
            div = views_html.findAll('div', {'class': 'sp_text'})
            span = str(div[2].find('span', {'class': 'sp_text_data'}))
            self._views = int(''.join(
                (span[span.find('>')+1: span.find('</span>')]).split(',')))

    def _parse(self):
        try:
            content = urllib.request.urlopen(self._url)
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            self._parse_title(soup)
            self._parse_intro(soup)
            self._parse_methods(soup)
            self._parse_votes_n_helpful(soup)
            self._parse_is_expert(soup)
            self._parse_last_updated(soup)
            self._parse_views(soup)
            self._parsed = True
        except Exception as e:
            raise ParseError

    def get(self):
        return {
            'url': self.url,
            'title': self.title,
            'intro': self.intro,
            'n_methods': self.n_methods,
            'methods': self.methods,
            'summary': self.summary,
            'num_votes': self.num_votes,
            'percent_helpful': self.percent_helpful,
            'is_expert': self.is_expert,
            'last_updated': self.last_updated,
            'views': self.views
        }


class WikiHow:
    lang2url = {
        'en': 'http://www.wikihow.com/',
        'es': 'http://es.wikihow.com/',
        'pt': 'http://pt.wikihow.com/',
        'it': 'http://www.wikihow.it/',
        'fr': 'http://fr.wikihow.com/',
        'ru': 'http://ru.wikihow.com/',
        'de': 'http://de.wikihow.com/',
        'zh': 'http://zh.wikihow.com/',
        'nl': 'http://nl.wikihow.com/',
        'cz': 'http://www.wikihow.cz/',
        'id': 'http://id.wikihow.com/',
        'jp': 'http://www.wikihow.jp/',
        'hi': 'http://hi.wikihow.com/',
        'th': 'http://th.wikihow.com/',
        'ar': 'http://ar.wikihow.com/',
        'ko': 'http://ko.wikihow.com/',
        'tr': 'http://www.wikihow.com.tr/',
        'vn': 'http://www.wikihow.vn/',
    }

    @ staticmethod
    def search(search_term, max_results=-1, lang='en'):
        lang = lang.split('-')[0].lower()
        if lang not in WikiHow.lang2url:
            raise UnsupportedLanguage
        search_url = WikiHow.lang2url[lang] + \
            'wikiHowTo?search=' + search_term.replace(' ', '+')
        content = urllib.request.urlopen(search_url)
        read_content = content.read()
        soup = BeautifulSoup(read_content, 'html.parser').findAll('a', attrs={
            'class': 'result_link'})
        count = 1
        for link in soup:
            url = link.get('href')
            if not url.startswith('http'):
                url = 'http://' + url
            how_to = Article(url)
            try:
                how_to._parse()
            except ParseError:
                continue
            yield how_to
            count += 1
            if 0 < max_results < count:
                return


def random_article(lang='en'):
    url = WikiHow.lang2url[lang] + 'Special:Randomizer'
    return Article(url)


def search_wikihow(query, max_results=10, lang='en'):
    return list(WikiHow.search(query, max_results, lang))


if __name__ == '__main__':
    exit()
