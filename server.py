"""Server for Community Library app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
import os
import api
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ Show Homepage."""

    return render_template('homepage.html')

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.files:
            image = request.files['file']
            print(image)
            image_url = api.cloudinary_upload_image(image)
            print('image_uploaded')
            print(image_url)
    
    return jsonify(image_url)





if __name__ == '__main__':
    # connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
