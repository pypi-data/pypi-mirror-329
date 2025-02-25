# 🌐 WebP Image Field

[![PyPI version](https://badge.fury.io/py/webp-image-field.svg)](https://badge.fury.io/py/webp-image-field)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django Version](https://img.shields.io/badge/Django-%3E%3D3.0-blue.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-%3E%3D3.6-blue.svg)](https://www.python.org/)

**WebP Image Field** is a Django package that provides a custom ImageField which automatically converts uploaded images to the WebP format. This helps optimize image loading times on the web, as WebP images are often significantly smaller than JPEG or PNG files.

## ✨ Features

- 🚀 **Automatic Conversion**: Seamlessly converts images to WebP during upload.
- 🔧 **Customizable Quality**: Adjust WebP quality to balance between size and image fidelity.
- 🔌 **Easy Integration**: Drop-in replacement for Django's ImageField.

## 📋 Requirements

Before using WebP Image Field, ensure you have the following dependencies installed:

- **Python**: >= 3.6
- **Django**: >= 3.0
- **Pillow**: >= 8.0.0

## 🛠 Installation

Install the package using pip:

bash
pip install webp-image-field


## 🚀 How to Use
1. Add to Your Django Project
First, make sure that webp-image-field is installed in your environment .

2. Update Your Models if you have been using ImageField
Replace Django’s built-in ImageField with WebPImageField in your models.
if you have been migrated you don't have to make new migrations.

Here’s a basic example:

bash
from django.db import models
from webp_image_field import WebPImageField

class MyModel(models.Model):
    image = WebPImageField(upload_to='images/', quality=85)

    def __str__(self):
        return f"Image: {self.image.url}"

        
upload_to: Specifies the directory within your MEDIA_ROOT where the images will be saved.

quality: Sets the quality of the WebP images (default is 90). You can adjust this value to balance between image quality and file size.
