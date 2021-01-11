"""Server for Community Library app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
from passlib.hash import argon2
import json
from model import connect_to_db
import os
import api
import crud
import helper

FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.jinja_env.undefined = StrictUndefined
app.config['ALLOWED_IMG_EXT'] = ['PNG', 'JPG', 'JPEG', 'GIF']


@app.route('/')
def homepage():
    """ Show Homepage."""

    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login_user():
    """ Login user """

    email = request.form['email']
    incoming_password = request.form['password']
    user = helper.get_user_by_email(email)
    if user == None:
        flash('No account with this email exists. Please try again.')
        return redirect ('/')
    else: 
        if argon2.verify(incoming_password, user.password):
            session['EMAIL'] = user.email
            session['NAME'] = user.fname 
            session['ID'] = user.user_id
            return redirect (f'profile/{user.fname}')  
        else:
            flash('Incorrect Password. Please try again.')
            return redirect ('/') 

@app.route('/logout')
def logout_user():
    """Clear session and logout user"""

    session.clear()
    return redirect('/')

@app.route('/create-user', methods=['POST'])
def create_user():
    """Create new user account"""
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    user = helper.get_user_by_email(email)

    if len(phone) != 10:
        flash('Phone numbers must be 10 digits long')
        return redirect ('/')
    phone = '+1' + phone
    print(phone)

    if user != None:
        flash('This email is already associated with an account. Please log in.')
        return redirect ('/')
    else:
        crud.create_user(email, password, fname, lname, phone)
        flash('Your account has been created.  Please log in.')
        return redirect ('/')



@app.route('/profile')
def reroute_to_profile():
    """obtain username to reroute to profile"""
    if session.get('ID') is None:
        flash('You must be logged in to view your profile')
        return redirect ('/')
    
    fname = session.get('NAME')
    return redirect (f'profile/{fname}')

@app.route('/profile/<fname>')
def render_profile(fname):
    """Show user profile"""

    return render_template('profile.html', fname=fname)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Upload image to Cloudinary and database"""

    if request.files:
        image = request.files['file']
        allowed_filetype = helper.check_img_ext(image)

        if allowed_filetype == True:
            image_url = api.cloudinary_upload_image(image)
            print('image_uploaded')
        else:
            return jsonify('Please make sure your image file is a .png, .jpg, .jpeg or .gif')
    
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genres')
        description = request.form.get('description')

        # if request.form['available'] == 'yes':
        #     available = True
        # else:
        #     available = False
        available = True
        owner = session['ID']

        crud.create_book(title, author, genre, description, image_url, owner, available)

    return jsonify('Your book has been uploaded')

@app.route('/search')
def render_search_page():

    return render_template('search.html')

@app.route('/books/browse-all')
def return_all_books():
    """Return all books to front-end"""

    return jsonify(helper.get_all_book_data())

@app.route('/books/search-books', methods = ['POST'])
def return_search_results():
    search_words = request.form.get('search')
    param = request.form.get('param')
    result = helper.search_database(search_words, param)
    # if type(result) == str:
    #     flash(result)
    #     return redirect ('/search')
    # else: 
    return jsonify(result)

@app.route('/books/borrow-book')
def send_book_request_text():
    """Send text request to book owner to facilitate borrow"""

    if session.get('ID') is None:
        return jsonify('You must be logged in to borrow a book')

    user_id = session['ID']
    user_name = session['NAME']
    user_phone = helper.get_user_phone


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
