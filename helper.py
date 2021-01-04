""" Helper functions"""

from model import (db, User, Book, connect_to_db)
# import json
# import os

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()

def get_length_of_phone(phone):
    
    if len(phone) == 10:
        return True
    else:
        return False


if __name__ == '__main__':
    from server import app
    connect_to_db(app)