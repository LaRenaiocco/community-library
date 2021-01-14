"""Back End Tests"""
#run code in terminal: 
# python3 -m unittest test.py 

from unittest import TestCase
from flask import session
from model import (connect_to_db, db, example_data, User, Book)
from server import app
import helper
import crud
import api

class FlaskTestsBasic(TestCase):
    """Flask route path tests (no db)"""

    def setUp(self):
        """To do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage"""

        result = self.client.get('/')
        self.assertIn(b'a fullstack project by LaRena Iocco', result.data)
    
    def test_profile_no_login(self):
        """Test that profile redirects to homepage if no login"""

        result = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'a fullstack project by LaRena Iocco', result.data)

    def test_search_page(self):
        """Test that search page renders"""
        result = self.client.get('/search')
        self.assertIn(b'Browse All Books', result.data)


class CrudAndHelperTests(TestCase):
    """Crud and Helper function tests (with db)"""

    def setUp(self):
        """To do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///apptestdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """To do at end of every test"""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_create_user(self):
        """Tests creation of user in database"""

        u = crud.create_user(email='Claire@claire.com', 
                            password='test', 
                            fname='Claire', 
                            lname='Cramer', 
                            phone='1234567890')
        self.assertIsNotNone(u.user_id)

    def test_create_book(self):
        """Tests creation of user in database"""

        b = crud.create_book(title='Tipping the Velvet', 
                            author='Sarah Waters', 
                            genre='fiction, historical fiction, LGBT', 
                            description=None, 
                            image_url='https://res.cloudinary.com/rosieslibrary/image/upload/v1609811721/Books/tipping_the_velvet_kmsojp.jpg',
                            owner=1,
                            available=True)
        self.assertIsNotNone(b.book_id)

    def test_delete_book(self):
        """Tests deleting of book from database"""

        book_id = 1
        crud.delete_book(book_id)
        self.assertFalse(Book.query.get(book_id))


if __name__ == '__main__':
    unittest.main()