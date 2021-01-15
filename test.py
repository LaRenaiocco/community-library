"""Back End Tests"""
#run code in terminal: 
# python3 -m unittest test.py 

from unittest import TestCase
from flask import session
from passlib.hash import argon2
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

        crud.delete_book(book_id=1)
        self.assertFalse(Book.query.get(1))

    def test_get_user_by_email(self):
        """Tests get user by email database query"""

        u = helper.get_user_by_email(email='Alex@alex.com')
        self.assertIsNotNone(u.user_id)

    def test_get_user_phone(self):
        """Tests get user phone database query"""

        p = helper.get_user_phone(user_id=1)
        self.assertIsNotNone(p)

    def test_get_user_books_true(self):
        """ Tests get user's books database query with books"""

        books = helper.get_user_books(user_id=1)
        no_books = helper.get_user_books(user_id=2)
        self.assertIsInstance(books, list)
        self.assertIsInstance(no_books, str)

    def test_check_user_matches_book_owner(self):
        """Tests check that current user matches book owner"""

        match = helper.check_user_matches_book_owner(book_id=1, user_id=1)
        no_match = helper.check_user_matches_book_owner(book_id=1, user_id=2)
        self.assertTrue(match)
        self.assertFalse(no_match)

    def test_get_all_book_data(self):
        """ Tests get all book data database query"""

        result = helper.get_all_book_data()
        self.assertIsInstance(result, list)

    def test_search_database(self):
        """Tests database search return type"""

        match = helper.search_database(search_words='Jane', 
                                        param='author')
        no_match = helper.search_database(search_words='J.K. Rowling', 
                                        param='author')
        self.assertIsInstance(match, list)
        self.assertIsInstance(no_match, str)

    def test_search_title(self):
        """Tests database query based on title"""
        
        result = helper.search_title(search_words='Pride and Prejudice')
        book = result[0]
        self.assertIsNotNone(book.user.user_id)

    def test_search_author(self):
        """Tests database query based on author"""
        
        result = helper.search_author(search_words='Jane')
        book = result[0]
        self.assertIsNotNone(book.user.user_id)

    def test_search_genre(self):
        """Tests database query based on genre"""
        
        result = helper.search_genre(search_words='fiction')
        book = result[0]
        self.assertIsNotNone(book.user.user_id)

    def test_search_all(self):
        """Tests database query of all fields"""
        
        result = helper.search_all(search_words='Jane')
        book = result[0]
        self.assertIsNotNone(book.user.user_id)

    def test_jsonify_book_search_data(self):
        """Tests preparing book object data for JSON formatting"""

        book_list = Book.query.all()
        json_list = helper.jsonify_book_search_data(book_list)
        self.assertIn('title', json_list[0])

    def test_jsonify_user_book_data(self):
        """Tests preparing book object data for JSON formatting"""

        book_list = Book.query.all()
        json_list = helper.jsonify_user_book_data(book_list)
        self.assertIn('title', json_list[0])

    def test_jsonify_new_book(self):
        """Tests preparing book object data for JSON formatting"""

        book = Book.query.first()
        json = helper.jsonify_new_book(book)
        self.assertIn('title', json)

class BasicFunctions(TestCase):

    def test_check_img_ext(self):

        bad_file1 = helper.check_img_ext('file')
        bad_file2 = helper.check_img_ext('file.txt')
        good_file = helper.check_img_ext('file.jpeg')
        self.assertFalse(bad_file1)
        self.assertFalse(bad_file2)
        self.assertTrue(good_file)





if __name__ == '__main__':
    unittest.main()