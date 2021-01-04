"""Data models for Community Library"""

from flask_sqlalchemy import SQLAlchemy

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
    available = db.Column(db.Boolean)
    owner = db.Column(db.Integer,
            db.ForeignKey('users.user_id'))

    user = db.relationship('User', backref='book')

    def __repr__(self):
        return f'<Book Object - book_id: {self.book_id}, title: {self.title} owner: {self.owner}>'

if __name__ == '__main__':
    from server import app
    connect_to_db(app)