import requests
from bs4 import BeautifulSoup
from locators.page_locators import PageLocators


def parse_page(page_link: str):
    """
    Parses book contents from giving link.
    :param page_link: Link of page
    :return: List of book content
    """
    page = requests.get(page_link)
    page_content = page.content

    locator = PageLocators.PAGE_LOCATOR

    soup = BeautifulSoup(page_content, 'html.parser')
    books = soup.select(locator)

    return books
