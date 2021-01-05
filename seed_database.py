""" Script to seed our database with objects."""
import os
import json
import crud
import model
import server

os.system('dropdb library')
os.system('createdb library')

model.connect_to_db(server.app)
model.db.create_all()

# Create users
crud.create_user('test@test.com', 'test', 'Test', 'Test', '+17073182084')
crud.create_user('Alex@alex.com', 'test', 'Alex', 'Arbour', '+17073182084')
crud.create_user('Bobby@bobby.com', 'test', 'Bobby', 'Bobbington', '+17073182084')
crud.create_user('Claire@claire.com', 'test', 'Claire', 'Carson', '+17073182084')
crud.create_user('Dawna@dawna.com', 'test', 'Dawna', 'Darcy', '+17073182084')
crud.create_user('Eunice@eunice.com', 'test', 'Eunice', 'Ellis', '+17073182084')
crud.create_user('Flo@flo.com', 'test', 'Flo', 'Florence', '+17073182084')
crud.create_user('Grace@grace.com', 'test', 'Grace', 'Graceful', '+17073182084')
crud.create_user('Hildy@hildy.com', 'test', 'Hildy', 'Hinter', '+17073182084')
crud.create_user('Jamie@jamie.com', 'test', 'Jamie', 'Jameson', '+17073182084')
crud.create_user('Kat@kat.com', 'test', 'Kat', 'King', '+17073182084')

# Create books

with open('data/books.json') as f:
    book_data = json.loads(f.read())

for book in book_data:
    title = book['title']
    author = book['author']
    genre = book['genre']
    description = book['description']
    image_url = book['image_url']
    owner = int(book['owner'])
    if book['available'] == 'True':
        available = True
    else:
        available = False

    book_object = crud.create_book(title, author, genre, description, image_url, owner, available)
