import os
from setuptools import setup, find_packages

# Get the absolute path to the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Read the README file for the long description
readme_path = os.path.join(base_dir, "README.md")

if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "A custom Django ImageField that automatically converts images to WebP format."

setup(
    name='webp_imagefield',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'Pillow>=8.0.0'
    ],
    include_package_data=True,
    description='A custom Django ImageField that automatically converts images to WebP format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mehdi Shoqeyb',
    author_email='mehdi.shoqeyb@gmail.com',
    url='https://github.com/mehdi-shoqeyb/webp-image-field',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',  # Update as your project matures
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
