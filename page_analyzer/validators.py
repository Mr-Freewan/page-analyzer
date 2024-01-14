from urllib.parse import urlparse

import validators
from page_analyzer.database import get_url_by_name


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def validate_url(url):
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
        normalized_url = normalize_url(url)
        validation_result['url'] = normalized_url
        if get_url_by_name(normalized_url):
            validation_result['error'] = 'exists'

    print(validation_result)
    return validation_result
