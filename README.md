# <img src="https://github.com/LaRenaiocco/community-library/blob/master/static/assets/community-library-navbar.png" alt="Community Library">
Community Library was inspired by many things! My love of books and libraries, missing the library during the pandemic, and social media groups like the "Buy Nothing" communities.  I thought wouldn't it be great to be able to see what books other people in your community own and are willing to lend out, instead of having to buy books or wait for libraries to re-open.
I designed this project with the desire to figure out how to build an image repository on Cloudinary and learn how to interact with it. 

## About the Developer
Before attending Hackbright Academy, LaRena spent most of her adult life clowning around in the circus (yes, you read that right).  She studied Theatre in college and then honed her circus and clowning skills at the San Francisco Clown Conservatory.  LaRena spent 8 years touring full time in the US, Mexico and Japan with Ringling Bros. and Barnum & Bailey as well as Kinoshita Circus. Despite her passion for travel, being on the road 52 weeks a year can wear out even the most seasoned traveller.  Looking to live in one place and ready for the next step in her career, coupled with massive amounts of time in the current pandemic, LaRena discovered a love for software development and has enjoyed putting her previously unused math and logic skills to good use and learning to code.
<!-- ## Deployment
 http://adventure-awaits.fun/ -->

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future Features](#future)
* [Installation](#installation)
* [License](#license)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* Jinja2
* PostgresQL
* SQLAlchemy ORM
* JavaScript
* jQuery
* HTML
* CSS
* Bootstrap
* Cloudinary
* Twilio

## <a name="features"></a>Features

#### Landing Page
The landing page provides basic information about my project as well as the ability to login or sign up for a new account.
Passwords are encrypted using the Passlib library on Python.

#### User Profile Page
After a user has created an account and logged in they will be redirected to their profile page.  Here the user can see all of their books and add and delete books to their library.  Once a new book form is submitted, the server side will add the photo to Cloudinary as well as to the database.

#### Book Search
A user does not need to be logged in to see the books available, but will need to log in before they can request to borrow a book. Users can search by title, author, genre or all (which includes the previous 3 as well as the description). Queries on the server side will return all relevant data, and the client side will dynamically render the data to the page.

## <a name="future"></a>The Future of Community Library
There are lots of new features planned for additional sprints:
* Use a geolocating API to only show books within a certain distance of the user OR
* Have regions/groups that users can join or create in their own community
* Allow editing of profile information (including email, password)
* Allow editing of book data (updating genres, description, etc)
* Adding settings for availability of books
* Improving the contact of a book owner
* Working with React on the front end
* And much more...


## <a name="installation"></a>Installation
To run Community Library on your own machine:

Install PostgresQL (Mac OSX)

Clone or fork this repo:
```
https://github.com/LaRenaiocco/community-library
```

Create and activate a virtual environment inside your Community Library directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Twilio API](https://www.twilio.com/try-twilio/)

Sign up to use the [Cloudinary API](https://cloudinary.com/)

Save your API keys in a file called <kbd>secrets.sh</kbd> using the following format and make sure to include your phone number as a string prefixed with "+1" so that you can interact with your new Twilio account.

```
export CLOUD_NAME="YOUR_CLOUDINARY_CLOUD_NAME"
export CLOUDINARY_KEY="YOUR_CLOUDINARY_KEY"
export CLOUDINARY_SECRET="YOUR_CLOUDINARY_SECRET"
export TWILIO_ACCOUNT_SID="YOUR_TWILIO_ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="YOUR_TWILIO_AUTH_TOKEN"
export TWILIO_PHONE="YOUR_TWILIO_PHONE"
export YOUR_PHONE_NUMBER="YOUR_PHONE_NUMBER"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb library
python3 model.py
```

Seed the database with the sample users and books if you wish:

```
python3 seed_database.py
```

Run the app:

```
python3 server.py
```

You can now navigate to 'localhost:5000/' to access Community Library.

## <a name="license"></a>License
The MIT License (MIT) Copyright (c) 2016 Agne Klimaite

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.