""" Script to seed our database with objects."""
import os
import json
import crud
import model
import server

# For development purposes only with Twilio
YOUR_PHONE_NUMBER = os.environ['YOUR_PHONE_NUMBER']

os.system('dropdb library')
os.system('createdb library')

model.connect_to_db(server.app)
model.db.create_all()

# Create users
crud.create_user('test@test.com', 'test', 'Testy', 'McTest', YOUR_PHONE_NUMBER)
crud.create_user('Alex@alex.com', 'test', 'Alex', 'Arbour', YOUR_PHONE_NUMBER)
crud.create_user('Bobby@bobby.com', 'test', 'Bobby', 'Bobbington', YOUR_PHONE_NUMBER)
crud.create_user('Claire@claire.com', 'test', 'Claire', 'Carson', YOUR_PHONE_NUMBER)
crud.create_user('Dawna@dawna.com', 'test', 'Dawna', 'Darcy', YOUR_PHONE_NUMBER)
crud.create_user('Eunice@eunice.com', 'test', 'Eunice', 'Ellis', YOUR_PHONE_NUMBER)
crud.create_user('Flo@flo.com', 'test', 'Flo', 'Florence', YOUR_PHONE_NUMBER)
crud.create_user('Grace@grace.com', 'test', 'Grace', 'Graceful', YOUR_PHONE_NUMBER)
crud.create_user('Hildy@hildy.com', 'test', 'Hildy', 'Hinter', YOUR_PHONE_NUMBER)
crud.create_user('Jamie@jamie.com', 'test', 'Jamie', 'Jameson', YOUR_PHONE_NUMBER)
crud.create_user('Kat@kat.com', 'test', 'Kat', 'King', YOUR_PHONE_NUMBER)

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
