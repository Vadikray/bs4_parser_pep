import re
import collections
import logging

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests import RequestException
from urllib.parse import urljoin

from constants import (BASE_DIR, MAIN_DOC_URL, MAIN_PEP_URL,
                       EXPECTED_STATUS, WHATSNEW, DOWNLOAD_HTML, DOWNLOAD)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag
from exceptions import ContentExclusion


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, WHATSNEW)
    soup = get_soup(session, whats_new_url)
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]

    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, "lxml")
        results.append((version_link,
                        find_tag(soup, "h1").text,
                        find_tag(soup, "dl").text.replace("\n", " "))
                       )
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")

    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise ContentExclusion("Ничего не нашлось")

    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"

    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, DOWNLOAD_HTML)
    soup = get_soup(session, downloads_url)
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag,
        "a",
        {"href": re.compile(r".+pdf-a4\.zip$")}
    )
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / DOWNLOAD
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)

    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    section_tag = find_tag(soup, "section", {"id": "numerical-index"})
    tr_tags = section_tag.find_all("tr")
    total_by_status = collections.defaultdict(int)

    for tr_tag in tqdm(tr_tags[1:], desc="Подсчет статусов PEP"):
        td_tag = find_tag(tr_tag, "td")
        preview_status = td_tag.text[1:]
        href = find_tag(tr_tag, "a")["href"]
        pep_link = urljoin(MAIN_PEP_URL, href)
        soup = get_soup(session, pep_link)
        dl_tag = find_tag(soup, "dl")
        for tag in dl_tag:
            if tag.name == "dt" and tag.text == "Status:":
                pep_status = tag.find_next_sibling().text
        total_by_status[pep_status] += 1
        status_preview = EXPECTED_STATUS[preview_status]
        if pep_status not in status_preview:
            logging.info(
                f"Несовпадающие статусы у PEP: "
                f'"{pep_link}".'
                f"Статус в карточке: {pep_status}, "
                f"ожидаемые статусы: {status_preview}."
            )
    total = 0
    results = [("Статус", "Количество")]
    for key, value in total_by_status.items():
        results.append((key, value))
        total += value
    results.append(("Всего PEP", total))

    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def get_soup(session, url):
    try:
        response = get_response(session, url)
        if response is None:
            return
    except RequestException:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )
    soup = BeautifulSoup(response.text, features="lxml")

    return soup


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
