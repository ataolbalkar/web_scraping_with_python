from typing import List
from pages.pages import get_pages
from parsers.page_parser import parse_page
from locators.page_locators import PageLocators


def get_books() -> List[str]:
    """
    Parses the links of all book in all 50 pages.
    :return: List of book links.
    """
    book_links = []
    locator = PageLocators.BOOK_LOCATOR

    for page in get_pages():
        for book in parse_page(page):
            book_content = book.select_one(locator)
            book_link = 'http://books.toscrape.com/catalogue/' + book_content.attrs['href']

            book_links.append(book_link)

    return book_links
