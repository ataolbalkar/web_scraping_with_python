from typing import List

"""
The site has 1000 books in 50 pages.
This package returns list of all 50 pages.
"""


def get_pages() -> List[str]:
    """
    :return: List of pages.
    """
    page_link = 'https://books.toscrape.com/catalogue/page-'

    pages = [page_link + str(i) + '.html' for i in range(1, 51)]

    return pages
