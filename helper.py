""" Helper functions"""

from model import (db, User, Book, connect_to_db)
# import json
# import os

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()

def get_user_phone(user_id):
    """ Look up user phone for twilio text"""

    user =  User.query.get(user_id)
    return user.phone



def get_all_book_data():
    """returns data for all books in database"""

    books = Book.query.all()
    json_books = []
    for book in books:
        book_dict = {}
        book_dict['title'] = book.title
        book_dict['author'] = book.author
        book_dict['image_url'] = book.image_url
        json_books.append(book_dict)

    return json_books



def search_database(search_words, param):
    """Quesry database for book search and return data"""

    if param == 'title':
        book_list = search_title(search_words)
    elif param == 'author':
        book_list = search_author(search_words)
    elif param == 'genre':
        book_list = search_genre(search_words)

    if len(book_list) > 0:
        return jsonify_book_list_data(book_list)
    else:
        return"""'No books match your search request. 
Please check your spelling or try fewer search words."""



def search_title(search_words):
    """Query database based on title column"""

    return  (Book.query.options(db.joinedload('user'))
            .filter(Book.title.ilike(f'%{search_words}%'))
            .all())



def search_author(search_words):
    """Query database based on author column"""

    return (Book.query.options(db.joinedload('user'))
            .filter(Book.author.ilike(f'%{search_words}%'))
            .all())



def search_genre(search_words):
    """Query database based on genre column"""
    
    return (Book.query.options(db.joinedload('user'))
            .filter(Book.genre.ilike(f'%{search_words}%'))
            .all())



def search_all(search_words):
    """Query Database from all columns"""
    pass



def jsonify_book_list_data(book_list):
    """return json list of database query for front end render"""

    json_book_list = []
    for book in book_list:
        book_data = {'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'image_url': book.image_url,
                'owner_name': book.user.fname,
                'owner_id': book.owner,
                'owner_phone': book.user.phone,
        }
        json_book_list.append(book_data)

    return json_book_list



def get_length_of_phone(phone):
    """check length of phone number for validity
        Type(int) is already coded into html input"""
    
    if len(phone) == 10:
        return True
    else:
        return False



def check_img_ext(filename):
    """Check that file upload is an allowable image filetype"""

    if not '.' in filename:
        return False

    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_IMG_EXT']:
        return True
    else:
        return False



if __name__ == '__main__':
    from server import app
    connect_to_db(app)