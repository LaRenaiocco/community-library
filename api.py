import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

CLOUD_NAME = os.environ['CLOUD_NAME']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']

cloudinary.config(cloud_name = CLOUD_NAME,
            api_key = CLOUDINARY_KEY,
            api_secret = CLOUDINARY_SECRET
            )

def cloudinary_upload_image(image_data):
    """Uploads user image to Cloudinary API"""
    if image_data:
        response = cloudinary.uploader.upload(image_data)
        image_url = response['secure_url']

    return image_url