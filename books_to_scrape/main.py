from books.books import get_books
from parsers.book_parsers import BookParser
from database import save_to_database


id = 0
for book_link in get_books():  # Gets the list of all 1000 books.
    # Gets informations from each book using parsers.
    title = BookParser(book_link).title
    price = BookParser(book_link).price
    star_rating = BookParser(book_link).star_rating
    thumbnail = BookParser(book_link).thumbnail
    tag = BookParser(book_link).tag
    stock = BookParser(book_link).stock

    # Saves all informations into book dictionary.
    book = {'id': id, 'title': title, 'price': price, 'star_rating': star_rating, 'thumbnail': thumbnail, 'tag': tag, 'stock': stock}
    id += 1

    try:  # Skips the book if there is a database exception.
        save_to_database(book)  # Save the book dictionary into database.

    except Exception:
        continue
