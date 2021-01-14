"""Data models for Community Library"""

from flask_sqlalchemy import SQLAlchemy
import os
YOUR_PHONE_NUMBER = os.environ['YOUR_PHONE_NUMBER']

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///library', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """Users for the community library"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
            autoincrement=True,
            primary_key=True)
    email = db.Column(db.String, 
            unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    phone = db.Column(db.String)

    def __repr__(self):
        return f'< User Object - user_id: {self.user_id}, email: {self.email} >'

class Book(db.Model):
    """Books added to the community library"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer,
            autoincrement=True,
            primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre = db.Column(db.String, 
            nullable=True)
    description = db.Column(db.Text,
            nullable=True)
    image_url = db.Column(db.String)
    owner = db.Column(db.Integer,
            db.ForeignKey('users.user_id'))
    available = db.Column(db.Boolean)


    user = db.relationship('User', backref='book')

    def __repr__(self):
        return f'<Book Object - book_id: {self.book_id}, title: {self.title} owner: {self.owner}>'


def example_data():
    """Data for tests"""

    User.query.delete()
    Book.query.delete()


    user1 = User(email='Alex@alex.com', 
				password='test', 
				fname='Alex', 
                lname='Arbour', 
				phone=YOUR_PHONE_NUMBER)
    user2 = User(email='Bobby@bobby.com', 
				password='test', 
				fname='Bobby',
                lname='Bobbington', 
				phone=YOUR_PHONE_NUMBER)
    book1 = Book(title='Pride and Prejudice', 
				author='Jane Austen', 
				genre='fiction, classics',
				description='Regency romantic comedy', 
				image_url="https://res.cloudinary.com/rosieslibrary/image/upload/v1609811718/Books/pride_and_prejudice_bj6ppu.jpg",
				owner=1,
				available=True)


    db.session.add_all([user1, user2, book1])
    db.session.commit()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)