""" Helper functions for Community Library app"""
from model import (db, User, Book, connect_to_db)

"""Search Queries"""

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_user_phone(user_id):
    """Look up user phone for twilio text"""

    user =  User.query.get(user_id)
    return user.phone


def get_user_books(user_id):
    """Look up all books owned by a user"""

    books = Book.query.filter(Book.owner == user_id).all()
    if len(books) > 0:
        json_books = jsonify_user_book_data(books)
        return json_books
    else:
        return "User has no books"


def check_user_matches_book_owner(book_id, user_id):
    """Make sure logged in user matches book owner"""

    book = Book.query.get(book_id)
    if user_id == book.owner:
        return True
    else:
        return False


def get_all_book_data():
    """Get data for all books in database"""

    books = Book.query.all()
    json_books = jsonify_book_search_data(books)

    return json_books


def search_database(search_words, param):
    """Query database based on search parameters and return data"""

    if param == 'title':
        book_list = search_title(search_words)
    elif param == 'author':
        book_list = search_author(search_words)
    elif param == 'genre':
        book_list = search_genre(search_words)
    else:
        book_list = search_all(search_words)

    if len(book_list) > 0:
        return jsonify_book_search_data(book_list)
    else:
        return"""No books match your search request. 
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

    return (Book.query.filter( (Book.title.ilike(f'%{search_words}%')) 
        | (Book.author.ilike(f'%{search_words}%')) 
        | (Book.genre.ilike(f'%{search_words}%')) 
        | (Book.description.ilike(f'%{search_words}%')) ).all())


def jsonify_book_search_data(book_list):
    """return json list of database query for front-end"""

    json_book_list = []
    for book in book_list:
        book_data = {'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'genre': book.genre,
                'image_url': book.image_url,
                'owner_name': book.user.fname,
                'owner_id': book.owner,
        }
        json_book_list.append(book_data)

    return json_book_list


def jsonify_user_book_data(book_list):
    """Return json list of books owned by 1 user"""

    json_book_list = []
    for book in book_list:
        book_data = {'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'image_url': book.image_url,
                'genre': book.genre,
                'description': book.description
        }
        json_book_list.append(book_data)

    return json_book_list


def jsonify_new_book(book):
    """return json object of newly uploaded book"""

    book_data = {'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'image_url': book.image_url,
                'genre': book.genre,
                'description': book.description
    }
    return book_data


"""Prepare data for API's and Database"""

def get_length_of_phone(phone):
    """check length of phone number for validity
        Type(int) is already coded into html input"""
    
    if len(phone) == 10:
        return True
    else:
        return False


def check_img_ext(filename):
    """Check that file upload is an allowable image filetype"""

    allowed_image_ext = ['PNG', 'JPG', 'JPEG', 'GIF']

    if not '.' in filename:
        return False

    ext = filename.split('.')[-1]

    if ext.upper() in allowed_image_ext:
        return True 
    else:
        return False


def create_public_id_for_image(book_id):
    """Creates public id from url for cloudinary delete"""

    book = Book.query.get(book_id)
    url = book.image_url
    filename = url.split('/')[-1]
    public_id = filename.split('.')[0]

    return public_id


def prepare_data_for_text(book_id, user_id):
    """prepare necessary data for twilio text message"""
    
    user = User.query.get(user_id)
    user_phone = user.phone
    user_name = user.fname
    book = (Book.query.options(db.joinedload('user'))
            .filter(Book.book_id == book_id).first())
    book_title = book.title
    owner_phone = book.user.phone

    return {'user_name': user_name,
            'user_phone': user_phone,
            'book_title': book_title,
            'owner_phone': owner_phone
            }



if __name__ == '__main__':
    from server import app
    connect_to_db(app)