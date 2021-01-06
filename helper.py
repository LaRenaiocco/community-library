""" Helper functions"""

from model import (db, User, Book, connect_to_db)
# import json
# import os

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()

def get_all_book_data():

    books = Book.query.all()
    json_books = []
    for book in books:
        book_dict = {}
        book_dict['title'] = book.title
        book_dict['author'] = book.author
        book_dict['image_url'] = book.image_url
        json_books.append(book_dict)

    return json_books

def get_length_of_phone(phone):
    
    if len(phone) == 10:
        return True
    else:
        return False


if __name__ == '__main__':
    from server import app
    connect_to_db(app)