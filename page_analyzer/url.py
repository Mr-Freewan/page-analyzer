from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from page_analyzer.database import get_url_by_field


def normalize(url: str) -> str:
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def validate(url: str) -> dict:
    validation_result = {
        'url': url,
        'error': None
    }

    if len(url) == 0:
        validation_result['error'] = 'zero_len'
    elif len(url) > 255:
        validation_result['error'] = 'too_long'
    elif not validators.url(url):
        validation_result['error'] = 'wrong'
    else:
        normalized_url = normalize(url)
        validation_result['url'] = normalized_url
        if get_url_by_field('name', normalized_url):
            validation_result['error'] = 'exists'

    return validation_result


def get_ceo_data(url: str) -> dict:
    checking_result = {}
    response = requests.get(url)

    if response.status_code != 200:
        raise RequestException

    checking_result['status_code'] = response.status_code

    soup = BeautifulSoup(response.text, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    checking_result['h1'] = h1_tag.text.strip() if h1_tag else ''
    checking_result['title'] = title_tag.text.strip() if title_tag else ''
    checking_result['description'] = description_tag['content'].strip() \
        if description_tag else ''

    return checking_result
