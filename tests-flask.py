"""Flask Route Tests"""
#run code in terminal: 
# python3 -m unittest tests-flask.py 

from unittest import TestCase
from flask import session
from model import (connect_to_db, db, example_data, User, Book)
from server import app
import helper
import crud
import api

class FlaskTestsBasic(TestCase):
    """Flask route tests (no db)"""

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

    def test_borrow_book_fail(self):
        """Tests that book borrow will fail if no user is logged in"""

        result = self.client.post('/books/borrow-book',
                                    data={'book': 1})
        self.assertIn(b'You must be logged in', result.data)



class FlaskTestsDatabase(TestCase):
    """Flask route Tests (with db)"""

    def setUp(self):
        """To do before every test."""

        self.client = app.test_client()
        app.config['SECRET_KEY'] = 'key'
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///apptestdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as s:
                s['ID'] = 1
                s['NAME'] = 'Alex'
                s['EMAIL'] = 'Alex@alex.com'

        #Mock functions for API calls
        def _mock_check_hashed_password(password, hashed_password):
            """Mocks boolean return of hashed password check"""

            if password == 'test':
                return True
            else:
                return False

        helper.check_hashed_password = _mock_check_hashed_password

        def _mock_cloudinary_image_upload(image_data):
            """Mocks Cloudinary API upload call"""

            return 'fake url'

        api.cloudinary_upload_image = _mock_cloudinary_image_upload

        def _mock_cloudinary_image_delete(image_data):
            """Mocks Cloudinary API delete call"""

            return 'image deleted'

        api.cloudinary_delete_image = _mock_cloudinary_image_delete

        def _mock_borrow_book_text(data):
            """Mocks Twilio text call"""

            return None 
        
        api.borrow_book_text = _mock_borrow_book_text

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login"""

        bad_email = self.client.post('/login', 
                                    data={'email': 'Wrong@wrong.com', 
                                        'password': 'wrong'},
                                    follow_redirects=True)
        bad_password = self.client.post('/login',
                                    data={'email': 'Alex@alex.com', 
                                        'password': 'wrong'},
                                    follow_redirects=True)
        correct = self.client.post('/login', 
                                    data={'email': 'Alex@alex.com', 
                                        'password': 'test'},
                                    follow_redirects=True)
        self.assertIn(b'No account with this email exists', bad_email.data)
        self.assertIn(b'Incorrect Password', bad_password.data)
        self.assertIn(b'Add a book to your Library', correct.data)

    def test_logout(self):
        """Test logout"""

        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'a fullstack project by LaRena Iocco', result.data)

    def test_create_user(self):
        """Test create user route"""

        bad_phone = self.client.post('/create-user',
                                    data={'email': 'Test@test.com',
                                        'password': 'test',
                                        'fname': 'Testy',
                                        'lname': 'McTester',
                                        'phone': '111'},
                                    follow_redirects=True)
        dup_email = self.client.post('/create-user',
                                    data={'email': 'Alex@alex.com',
                                        'password': 'test',
                                        'fname': 'Testy',
                                        'lname': 'McTester',
                                        'phone': '1234567890'},
                                    follow_redirects=True)
        new = self.client.post('/create-user',
                                    data={'email': 'Test@test.com',
                                        'password': 'test',
                                        'fname': 'Testy',
                                        'lname': 'McTester',
                                        'phone': '1234567890'},
                                    follow_redirects=True)
        self.assertIn(b'Phone numbers must be 10 digits long', bad_phone.data)
        self.assertIn(b'This email is already associated with an account', dup_email.data)
        self.assertIn(b'Your account has been created', new.data)

    def test_profile(self):
        """Test profile re-route"""

        result = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Add a book to your Library', result.data)

    def test_profile_user(self):
        """Test profile route with user name"""

        result = self.client.get('/profile/Alex')
        self.assertIn(b"Alex's Profile", result.data)

    def test_delete_book_route(self):
        """Test delete book route with DB delete and mock cloudinary delete"""

        good = self.client.post('/delete-book',
                                    data={'book': 1})
        bad = self.client.post('/delete-book',
                                    data={'book': 2})
        self.assertIn(b'Book Deleted', good.data)
        self.assertIn(b'You are not authorized', bad.data)

    def test_borrow_book_success(self):
        """Test borrow book route with mock Twilio call"""

        result = self.client.post('/books/borrow-book',
                                data={'book': 2})
        self.assertIn(b'A borrow request has been sent', result.data)

    # NOT WORKING  DON'T KNOW HOW TO MOCK THE IMAGE FILE
    # def test_upload_image(self):
    #     """Test image upload route"""

    #     good_file = self.client.post('/upload-image',
    #                                 data={'files': 'static/assets/favicon-32x32.png',
    #                                         'title': 'Test Book',
    #                                         'author': 'Test Author',
    #                                         'genre': 'test genre',
    #                                         'description': 'test description'})
    #     self.assertIn(b'title', good_file.data)


if __name__ == '__main__':
    unittest.main()