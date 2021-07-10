"""
wikiHowUnofficialAPI

API to extract data from wikiHow.
"""

__version__ = '0.1.1'
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
        """Method to return the count of the current method.

        Returns:
            int: The count of the current method
        """
        return self._number

    @property
    def title(self):
        """Method to return the title of a step.

        Returns:
            str: The title of a step
        """
        return self._title

    @property
    def description(self):
        """Method to return the description given in a step.

        Returns:
            str: The description given in a step
        """
        return self._description

    @property
    def picture(self):
        """Method to return the URL of image associated with the step.

        Returns:
            str: The URL of image associated with the step
        """
        return self._picture

    def get(self):
        """Method to return a dictionary of Steps data members.

        Returns:
            dict: A dictionary of Steps data members
        """
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
        """Method to return the count of the current method.

        Returns:
            int: The count of the current method
        """
        return self._number

    @property
    def title(self):
        """Method to return the title of a method.

        Returns:
            str: The title of a method
        """
        return self._title

    @property
    def steps(self):
        """Method to return a list of steps in a method.

        Returns:
            list: A list of steps in a method
        """
        return self._steps

    def get(self):
        """Method to return a dictionary of Method data members.

        Returns:
            dict: A dictionary of Method data members
        """
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
        self._methods = []
        self._num_votes = None
        self._percent_helpful = None
        self._is_expert = None
        self._last_updated = None
        self._views = None
        self._co_authors = None
        self._references = None
        self._summary = None
        self._warnings = []
        self._tips = []

        self._parsed = False
        if not lazy:
            self._parse()

    def __repr__(self):
        return self.title

    @property
    def url(self):
        """Method to return the URL of a wikiHow article.

        Returns:
            str: The wikiHow article URL
        """
        if not self._parsed:
            self._parse()
        return self._url

    @property
    def title(self):
        """Method to return the title of a wikiHow article.

        Returns:
            str: The wikiHow article title
        """
        if not self._parsed:
            self._parse()
        return self._title

    @property
    def intro(self):
        """Method to return the introduction from a wikiHow article.

        Returns:
            str: The wikiHow article introduction
        """
        if not self._parsed:
            self._parse()
        return self._intro

    @property
    def methods(self):
        """Method to return the method titles from a wikiHow article.

        Returns:
            list: A list of method titles
        """
        if not self._parsed:
            self._parse()
        return self._methods

    @property
    def n_methods(self):
        """Method to return the number of methods in a wikiHow article.

        Returns:
            int: The number of methods in a wikiHow article
        """
        return len(self._methods)

    @property
    def num_votes(self):
        """Method to return the number of votes given to a wikiHow article.

        Returns:
            int: The number of votes given to a wikiHow article
        """
        if not self._parsed:
            self._parse()
        return self._num_votes

    @property
    def percent_helpful(self):
        """Method to return the percent of helpful recieved by a wikiHow article.

        Returns:
            int: The percent of helpful recieved by a wikiHow article
        """
        if not self._parsed:
            self._parse()
        return self._percent_helpful

    @property
    def is_expert(self):
        """Method to check if a wikiHow article is written by an expert.

        Returns:
            bool: True if written by an expert, False otherwise.
        """
        if not self._parsed:
            self._parse()
        return self._is_expert

    @property
    def last_updated(self):
        """Method to return the last date when a wikiHow article was updated. (Format: YYYY-MM-DD HH: MM: SS)

        Returns:
            str: The last date when a wikiHow article was updated.
        """
        if not self._parsed:
            self._parse()
        return self._last_updated

    @property
    def views(self):
        """Method to return the number of times a wikiHow article was viewed.

        Returns:
            int: Number of times a wikiHow article was viewed.
        """
        if not self._parsed:
            self._parse()
        return self._views

    @property
    def co_authors(self):
        """Method to return the number of co-authors in a wikiHow article.

        Returns:
            int: Number of co-authors in a wikiHow article.
        """
        if not self._parsed:
            self._parse()
        return self._co_authors

    @property
    def references(self):
        """Method to return the number of references in a wikiHow article.

        Returns:
            int: Number of references in a wikiHow article.
        """
        if not self._parsed:
            self._parse()
        return self._references

    @property
    def summary(self):
        """Method to return the summary of a wikiHow article.

        Returns:
            str: summary of a wikiHow article.
        """
        if not self._parsed:
            self._parse()
        return self._summary

    @property
    def warnings(self):
        """Method to return a list of warnings from a wikiHow article.

        Returns:
            list: Warnings from a wikiHow article.
        """
        if not self._parsed:
            self._parse()
        return self._warnings

    @property
    def tips(self):
        """Method to return a list of tips from a wikiHow article.

        Returns:
            list: Tips from a wikiHow article.
        """
        if not self._parsed:
            self._parse()
        return self._tips

    def _parse_title(self, soup):
        """Method to extract the title of a wikiHow article.
        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
        html = soup.findAll(
            'h1', {'class': ['title_lg', 'title_md', 'title_sm']})[0]
        if not html.find('a'):
            raise ParseError
        else:
            self._title = html.text

    def _parse_intro(self, soup):
        """Method to extract the introduction from a wikiHow article.
        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
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
        """Method to extract the methods from a wikiHow article.
        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
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
        """Method to extract the number of helpful votes and helpful percentage given to a wikiHow article.
        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
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
        """Method to check if a wikiHow article is written by an expert.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
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
        """Method to extract the date of last update of a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
        update_html = soup.find('div', {'id': 'byline_info'})
        if not update_html:
            raise ParseError
        else:
            try:
                span = str(update_html.find('span'))
                date = span[span.find(': ')+2:span.find('</span>')]
                self._last_updated = datetime.strptime(date, '%B %d, %Y')
            except:
                pass

    def _parse_views(self, soup):
        """Method to extract the number of views in a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Raises:
            ParseError: The given article could not be parsed.
        """
        views_html = soup.find('div', {'class': 'sp_box sp_stats_box'})
        if views_html:
            div = views_html.findAll('div', {'class': 'sp_text'})
            span = str(div[2].find('span', {'class': 'sp_text_data'}))
            self._views = int(
                ''.join((span[span.find('>')+1: span.find('</span>')]).split(',')))
        else:
            pass

    def _parse_co_authors(self, soup):
        """Method to extract the number of co-authors in a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Returns:
            None: When no co-authors are found.
        """
        co_authors_html = soup.find('div', {'class': 'sp_box sp_stats_box'})
        if not co_authors_html:
            return None
        else:
            div = co_authors_html.findAll('div', {'class': 'sp_text'})
            span = str(div[0].find('span', {'class': 'sp_text_data'}))
            self._co_authors = int(''.join(
                (span[span.find('>')+1: span.find('</span>')]).split(',')))

    def _parse_references(self, soup):
        """Method to extract the number of references in a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Returns:
            None: When no references are found.
        """
        references_html = soup.findAll('a', {'class': 'external free'})
        count = 0
        if not references_html:
            return None
        else:
            for reference in references_html:
                count += 1
        self._references = count

    def _parse_summary(self, soup):
        """Method to extract summary from a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Returns:
            None: When no summary is found.
        """
        summary_html_div = soup.find('div', {'id': 'summary_wrapper'})
        if not summary_html_div:
            return None
        else:
            summary_html = summary_html_div.find('p', {'id': 'summary_text'})
            summary = summary_html.text[:-35]
            self._summary = summary

    def _parse_warnings(self, soup):
        """Method to extract warnings from a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Returns:
            None: When no warnings are found.
        """
        warnings_html_div = soup.find('div', {'id': 'warnings'})
        if not warnings_html_div:
            return None
        else:
            warnings_html = warnings_html_div.find('ul')
            if warnings_html != None:
                for li in warnings_html.findAll('li'):
                    if not li.find('div'):
                        return None
                    self._warnings.append(li.find('div').text)
            else:
                warnings_html = warnings_html_div.find('p')
                if warnings_html != None:
                    self._warnings.append(warnings_html.text)
                else:
                    return None

    def _parse_tips(self, soup):
        """Method to extract tips from a wikiHow article.

        Args:
            soup(bs4.BeautifulSoup): An instance of BeautifulSoup class for the entire article.

        Returns:
            None: When no tips are found.
        """
        tips_html_div = soup.find('div', {'id': 'tips'})
        if not tips_html_div:
            return None
        else:
            tips_html = tips_html_div.find('ul')
            if tips_html != None:
                for li in tips_html.findAll('li'):
                    if not li.find('div'):
                        return None
                    else:
                        self._tips.append(li.find('div').text)
            else:
                tips_html = tips_html_div.find('p')
                if tips_html != None:
                    self._tips.append(tips_html.text)
                else:
                    return None

    def _parse(self):
        """Method to extract useful information from a given wikiHow article.

        Raises:
            ParseError: The given article could not be parsed.
        """
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
            self._parse_co_authors(soup)
            self._parse_references(soup)
            self._parse_summary(soup)
            self._parse_warnings(soup)
            self._parse_tips(soup)

            self._parsed = True
        except Exception as e:
            raise ParseError

    def get(self):
        """Method to return a dictionary of class members.

        Returns:
            dict: A dictionary of class members.
        """
        return {
            'url': self.url,
            'title': self.title,
            'intro': self.intro,
            'n_methods': self.n_methods,
            'methods': self.methods,
            'num_votes': self.num_votes,
            'percent_helpful': self.percent_helpful,
            'is_expert': self.is_expert,
            'last_updated': self.last_updated,
            'views': self.views,
            'co_authors': self.co_authors,
            'references': self.references,
            'summary': self.summary,
            'warnings': self.warnings,
            'tips': self.tips
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
        'vn': 'http://www.wikihow.vn/'
    }

    @ staticmethod
    def search(search_term, max_results=-1, lang='en'):
        """Method to search for wikiHow articles.

        Args:
            search_term(str): [description]
            max_results(int, optional): Number of results. Defaults to - 1.
            lang(str, optional):  Language of the wikiHow articles. Defaults to 'en'.

        Raises:
            UnsupportedLanguage: There are no wikiHow articles with this language.

        Yields:
            str: One of the search results.
        """
        lang = lang.split('-')[0].lower()
        if lang not in WikiHow.lang2url:
            raise UnsupportedLanguage
        search_url = WikiHow.lang2url[lang] + \
            'wikiHowTo?search='+urllib.parse.quote(search_term)
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
    """Method to return a random wikiHow article.

    Args:
        lang(str, optional): Language of the wikiHow article. Defaults to 'en'.

    Returns:
        str: URL of the article.
    """
    url = WikiHow.lang2url[lang] + 'Special:Randomizer'
    return Article(url)


def search_wikihow(query, max_results=10, lang='en'):
    """Method to search and return a list of wikHow articles.

    Args:
        query(str): Search string
        max_results(int, optional): Number of search results. Defaults to 10.
        lang(str, optional): Language of the wikiHow articles. Defaults to 'en'.

    Returns:
        list: A list containing the names of the Wikhow articles from the search result.
    """
    return list(WikiHow.search(query, max_results, lang))


if __name__ == '__main__':
    """This file can only be loaded as a module."""
    exit()
