import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List


def get_links() -> List[str]:
    """
    Creates a list of page links.
    :return: List of links
    """
    links = ['http://quotes.toscrape.com']  # String is the first page.

    for i in range(2, 11):  # i is the page number between 'page 2' and 'page 10'
        links.append('http://quotes.toscrape.com/page/' + str(i) + '/')

    return links


def quotes(page_string: BeautifulSoup.string) -> List[BeautifulSoup]:
    """
    Selects the specific part of giving page where the quotes in.
    :param page_string: The string of all page.
    :return: List of contents in 'html' format.
    """
    soup = BeautifulSoup(page_string, 'html.parser')
    quotes_content = soup.select('div.container div.row div.col-md-8 div.quote')

    return quotes_content


class Locators:
    """
    The container of needed locators.
    """
    QUOTE_LOCATOR = 'span.text'
    AUTHOR_LOCATOR = 'span small.author'
    TAGS_LOCATOR = 'div.tags a'


class QuotesScrapers:
    """
    The container of needed actions.
    """
    def __init__(self, content: BeautifulSoup.string):
        self.content = content

    @property
    def quote(self) -> str:
        """
        Method that selects the qoute from giving content and returns it.
        :return: The quote itself.
        """
        quote_line = self.content.select_one(Locators.QUOTE_LOCATOR)
        quote = quote_line.string

        return quote

    @property
    def author(self) -> str:
        """
        Method that selects the author name of the quote from giving content and returns it.
        :return: The author name.
        """
        author_line = self.content.select_one(Locators.AUTHOR_LOCATOR)
        author = author_line.string

        return author

    @property
    def tags(self) -> List[str]:
        """
        Method that selects the tags of the quote from giving content and returns them.
        :return: List of tags.
        """
        tags_lines = self.content.select(Locators.TAGS_LOCATOR)
        tags = [tag.string for tag in tags_lines]
        return tags


def scrap() -> List[Dict]:
    """
    The main scraper function that scraps the data from all pages and returns them in a list.
    :return:
    """
    scraped = []  # A list to append contents.
    links = get_links()

    for link in links:  # A loop for all pages in the links list.
        page = requests.get(link)
        page_string = page.content
        contents = quotes(page_string)

        for content in contents:  # A loop for all contents in a page.
            quote = QuotesScrapers(content).quote[1:-1]  # The quote value has double quotes.
            author = QuotesScrapers(content).author  # So using indexing for .json file.
            tags = QuotesScrapers(content).tags

            line = {'quote': quote, 'author': author, 'tags': tags}
            scraped.append(line)

    return scraped


def save_to_json(scraped: List[Dict]) -> None:
    """
    Saves the giving list to main '.json' file.
    :param scraped: The list of scraped contents.
    :return: None
    """
    with open("quotes.json", "w") as quotes_file:
        json.dump(scraped, quotes_file)


save_to_json(scrap())  # It starts and ends here!
