""" Script to seed our database with objects."""

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
