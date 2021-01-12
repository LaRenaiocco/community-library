""" CRUD functions for Community Library database """

from model import (db, User, Book, connect_to_db)
from passlib.hash import argon2

def create_user(email, password, fname, lname, phone):
    """Create and return a new user."""

    user = User(email=email, 
        password=argon2.hash(password), 
        fname=fname, 
        lname=lname,
        phone=phone)

    db.session.add(user)
    db.session.commit()

    return user

def create_book(title, author, genre, description, image_url, owner, available=True,):
    book = Book(title=title,
        author=author,
        genre=genre,
        description=description,
        image_url=image_url,
        owner=owner,
        available=available)

    db.session.add(book)
    db.session.commit()
    print(f'crud.create_book {book}')

    return book

def delete_book(book_id):

    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    return 

if __name__ == '__main__':
    from server import app
    connect_to_db(app)