from selenium import webdriver
from selenium.webdriver.support.ui import Select
import sqlite3
import time


class Locators:
    AUTHOR_DROPDOWN = 'select#author'
    TAG_DROPDOWN = 'select#tag'
    SEARCH_BUTTON = 'input[name="submit_button"]'

    QUOTE_LOCATOR = 'span.content'
    AUTHOR_LOCATOR = 'span.author'
    TAG_LOCATOR = 'span.tag'


class QuotesScraper:
    def __init__(self, browser):
        self.browser = browser

    @property
    def author_dropdown(self):
        """
        Accesses to the Author dropdown.
        :return: Select object.
        """
        element = self.browser.find_element_by_css_selector(Locators.AUTHOR_DROPDOWN)

        return Select(element)

    @property
    def tag_dropdown(self):
        """
        Accesses to the Tag dropdown.
        :return: Select object.
        """
        element = self.browser.find_element_by_css_selector(Locators.TAG_DROPDOWN)

        return Select(element)

    @property
    def author_list(self):
        """
        Creates a list of all authors in the site.
        :return: Author list.
        """
        author_list = [option.text.strip() for option in self.author_dropdown.options[1:]]

        return author_list

    @property
    def tag_list(self):
        """
        Creates a list of tags when author specified.
        :return: List of accessible tags.
        """
        tag_list = [option.text.strip() for option in self.tag_dropdown.options[1:]]

        return tag_list

    @property
    def search_button(self):
        """
        :return: Search button to click.
        """
        return self.browser.find_element_by_css_selector(Locators.SEARCH_BUTTON)

    def select_author(self, author):
        """
        Selects the author from author dropdown.
        :param author:
        :return:
        """
        self.author_dropdown.select_by_visible_text(author)

    def select_tag(self, tag):
        """
        Selects the tag from tag dropdown.
        :param tag:
        :return:
        """
        self.tag_dropdown.select_by_visible_text(tag)

    def scrape(self):
        """
        Scraping method to scrape quotes information.
        :return: Quotes, author names, quote tags.
        """
        quote = self.browser.find_elements_by_css_selector(Locators.QUOTE_LOCATOR)
        author = self.browser.find_elements_by_css_selector(Locators.AUTHOR_LOCATOR)
        tag = self.browser.find_elements_by_css_selector(Locators.TAG_LOCATOR)

        return quote, author, tag

    def save_to_database(self, id, quote, author, tag):
        """
        Database interaction.
        """
        connection = sqlite3.connect('quotes.db')
        with connection:
            cursor = connection.cursor()

            cursor.execute('CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, quote TEXT, author TEXT, tag TEXT)')
            cursor.execute('INSERT INTO quotes VALUES(?, ?, ?, ?)', (id, quote, author, tag))

    def main(self):
        """
        Main function to interact with site and scrape it.
        :return:
        """
        id = 0  # Id number to specify quotes in database.
        for author in self.author_list:
            self.select_author(author)  # Selects the author dropdown.

            for tag in self.tag_list:
                self.select_tag(tag)  # Selects the tag dropdown.
                self.search_button.click()  # Clicks the button.
                time.sleep(1)  # Waits 1 sec to avoid conflicts.

                quote, author, tag = self.scrape()  # Scrapes all quotes on the page.

                # Saves the values inside list variables:
                for index in range(0, len(quote)):
                    self.save_to_database(id, quote[index].text, author[index].text, tag[index].text)
                    id += 1


chrome = webdriver.Chrome(executable_path="c:/chromedriver/chromedriver.exe")
chrome.get('http://quotes.toscrape.com/search.aspx')
QuotesScraper(chrome).main()
