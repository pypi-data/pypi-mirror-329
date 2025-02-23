"""
In this file we handle Tiktok url and we parse
them to obtain basic information and check if
they are valid ones or not.

We have two different types of valid urls:
- Long: 'https://www.tiktok.com/@ahorayasabesque/video/7327001175616703777?\_t=8jqq93LWqsC&\_r=1'
- Short: 'https://vm.tiktok.com/ZGeSJ6YRA'
"""
from yta_general_utils.programming.regular_expressions import GeneralRegularExpression
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.web.tiktok.dataclasses import TiktokUrl

import requests


class TiktokUrlParser:
    """
    Class to simplify the way we parse Tiktok
    videos urls.
    """

    @staticmethod
    def is_valid(url: str):
        """
        Check if the provided Tiktok video 'url' is
        valid or not. A valid Tiktok url can be a 
        short url or a long url.
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return _is_short_tiktok_url(url) or _is_long_tiktok_url(url)
    
    @staticmethod
    def parse(
        url: str
    ) -> TiktokUrl:
        """
        Parse the provided 'url' and return a TiktokUrl
        dataclass instance containing the author username,
        the video id and the long-format url, or raises
        an Exception if the given 'url' is not valid.
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')

        if not TiktokUrlParser.is_valid(url):
            raise Exception('The provided "url" is not a valid tiktok video url.')
        
        url = _clean(url)
        if not _is_long_tiktok_url(url):
            url = _short_tiktok_url_to_long_tiktok_url(url)

        aux = url.split('/')

        return TiktokUrl(
            username = aux[len(aux) - 3],
            video_id = aux[len(aux) - 1],
            url = url
        )
    
def _is_short_tiktok_url(url: str):
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    return GeneralRegularExpression.TIKTOK_SHORT_VIDEO_URL.parse(url)

def _is_long_tiktok_url(url: str):
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    return GeneralRegularExpression.TIKTOK_LONG_VIDEO_URL.parse(url)

def _short_tiktok_url_to_long_tiktok_url(url: str):
    """
    Transforms the provided short tiktok 'url' to 
    the long format and returns it.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    if not _is_short_tiktok_url(url):
        raise Exception('No "url" provided is not a short tiktok url.')

    return requests.get(url).url

def _clean(url: str):
    """
    Removes any additional parameter that is after a
    question mark sign.
    """
    if not PythonValidator.is_string(url):
        raise Exception('The provided "url" parameter is not a string.')
    
    url = url.split('?')[0] if '?' in url else url

    return url