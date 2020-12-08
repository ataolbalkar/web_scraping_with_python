import sqlite3
from typing import Dict


class DatabaseConnection:
    """
    The context manager to use in database connection.
    """
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect('books.db')
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


def save_to_database(book: Dict):
    """
    Saves the book to the database.
    :param book: The dictionary of books informations.
    :return: None
    """
    id = book['id']
    title = book['title']
    price = book['price']
    star_rating = book['star_rating']
    thumbnail = book['thumbnail']
    tag = book['tag']
    stock = book['stock']

    with DatabaseConnection() as connection:
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS books(id int primary key, title text, price real, star_rating integer, thumbnail text, tag text, stock integer)')
        cursor.execute('INSERT INTO books VALUES(?, ?, ?, ?, ?, ?, ?)', (id, title, price, star_rating, thumbnail, tag, stock))
