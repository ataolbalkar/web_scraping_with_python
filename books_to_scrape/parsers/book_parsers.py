import requests
from bs4 import BeautifulSoup
from locators.book_locators import BookLocators


class BookParser:
    """
    The parser class for parsing book information.
    """
    def __init__(self, book_link: str):
        self.link_list = book_link

        content = requests.get(book_link).content
        self.soup = BeautifulSoup(content, 'html.parser')

    @property
    def title(self) -> str:
        """
        Parses the title of the book.
        :return: Title
        """
        locator = BookLocators.TITLE_LOCATOR

        title = self.soup.select_one(locator).string

        return str(title)

    @property
    def price(self) -> float:
        """
        Parses the price of the book.
        :return: Price
        """
        locator = BookLocators.PRICE_LOCATOR

        price_str = self.soup.select_one(locator).string
        price = float(price_str[1:])  # Deletes the '£' currency and turns str price to float format.

        return price

    @property
    def star_rating(self) -> int:
        """
        Parses the star rating of the book.
        :return: Star rating
        """
        locator = BookLocators.STAR_RATING_LOCATOR

        content = self.soup.select_one(locator)
        # List is in format of ['star-rating', '(Number of stars)']. Comprehension is for get rid of it:
        star_rating_list = [i for i in content.attrs.get('class', []) if i != 'star-rating']

        if star_rating_list[0] == 'One':
            star_rating = 1
        elif star_rating_list[0] == 'Two':
            star_rating = 2
        elif star_rating_list[0] == 'Three':
            star_rating = 3
        elif star_rating_list[0] == 'Four':
            star_rating = 4
        elif star_rating_list[0] == 'Five':
            star_rating = 5
        else:
            star_rating = 0

        return star_rating

    @property
    def thumbnail(self) -> str:
        """
        Parses the thumbnail link of the book.
        :return: Thumbnail link.
        """
        locator = BookLocators.THUMBNAIL_LOCATOR

        content = self.soup.select_one(locator)

        src = content.attrs['src']
        link = src.strip("../")  # Removes the '../' string.
        thumbnail = 'http://books.toscrape.com/' + link  # Makes it a proper link.

        return str(thumbnail)

    @property
    def tag(self) -> str:
        """
        Parses the tag of the book.
        :return: Tag
        """
        locator = BookLocators.TAG_LOCATOR

        content = self.soup.select(locator)

        tag = content[-1].string

        return str(tag)

    @property
    def stock(self) -> int:
        """
        Parses the number of books in the stock.
        :return: Stock.
        """
        locator = BookLocators.STOCK_LOCATOR

        content = self.soup.select(locator)
        stock_string = content[-2].string

        if stock_string[0:8] != 'In stock':
            return 0

        # Operations to get only the number:
        stock_string = stock_string.strip('In stock (')
        stock_string = stock_string.strip(' avaible)')
        stock = int(stock_string)

        return stock
