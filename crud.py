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

def create_book(title, author, genre, description, image_url, available, owner):
    book = Book(title=title,
        author=author,
        genre=genre,
        description=description,
        image_url=image_url,
        available=available,
        owner=owner)

    db.session.add(book)
    db.sesion.commit()

    return book

if __name__ == '__main__':
    from server import app
    connect_to_db(app)