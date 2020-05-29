import os

############################################################################
# Flask-Login
############################################################################
SECRET_KEY = b'9cd9ea3d9fbcab99e896c6a28f348cf4986c98700f6d9f9f371810f4e3f7de6c9d'
############################################################################
# System
############################################################################
SYSTEM_MODE = "DEV"
ROOT_DIR = os.getcwd() + "/"
############################################################################
# Image Formate
############################################################################
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
IMAGE_FORMATS = {
    "news": {
        "main_image": {
            "width": "1920",
            "height": "0",
            "max_files": 1,
            "max_size": 30  # 30 MB
        },
        "teaser_image": {
            "width": "480",
            "height": "480",
            "max_files": 1,
            "max_size": 30  # 30 MB
        },
        "meta_image": {
            "width": "1920",
            "height": "0",
            "max_files": 1,
            "max_size": 30  # 30 MB
        }
    },
    "pages": {
        "slider_images": {
            "width": "1920",
            "height": "0",
            "max_files": 6,
            "max_size": 30  # 30 MB
        },
        "head_image": {
            "width": "1920",
            "height": "0",
            "max_files": 1,
            "max_size": 30  # 30 MB
        },
        "teaser_image": {
            "width": "480",
            "height": "480",
            "max_files": 1,
            "max_size": 30  # 30 MB
        },
        "meta_image": {
            "width": "1920",
            "height": "0",
            "max_files": 1,
            "max_size": 30  # 30 MB
        }
    }
}
