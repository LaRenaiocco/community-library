import cloudinary
import cloudinary.uploader
import cloudinary.api
from twilio.rest import Client
import os

CLOUD_NAME = os.environ['CLOUD_NAME']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE = os.environ['TWILIO_PHONE']

#  CLOUDINARY
cloudinary.config(cloud_name = CLOUD_NAME,
            api_key = CLOUDINARY_KEY,
            api_secret = CLOUDINARY_SECRET
            )

def cloudinary_upload_image(image_data):
    """Uploads user image to Cloudinary API"""
    if image_data:
        response = cloudinary.uploader.upload(image_data)
        print(response)
        image_url = response['secure_url']

    return image_url

def cloudinary_delete_image(public_id):
    """Removes user image from Cloudinary API"""

    response = cloudinary.uploader.destroy(public_id)
    result = response['result']
    return result


# TWILIO
def borrow_book_text(recipient_phone, requestor_phone, book_title, requestor_name):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
                        body=f'Hello from the Community Library!\n{requestor_name} would like to borrow {book_title}.\n You can reach them at {requestor_phone}.',
                        from_=TWILIO_PHONE,
                        to=recipient_phone
                    )

    print(message.sid)