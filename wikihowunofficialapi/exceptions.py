class ParseError(RuntimeError):
    """ Error parsing wikiHow page"""


class UnsupportedLanguage(ValueError):
    """ Unsupported lang, see https://www.wikihow.com/wikiHow:Language-Projects"""
