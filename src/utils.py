import logging

from requests import RequestException
from exceptions import ParserFindTagException


def get_response(session, url, utf="utf-8"):
    try:
        response = session.get(url)
        response.encoding = utf

        return response
    except RequestException:
        raise RequestException


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))

    if searched_tag is None:
        error_msg = f"Не найден тег {tag} {attrs}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)

    return searched_tag
