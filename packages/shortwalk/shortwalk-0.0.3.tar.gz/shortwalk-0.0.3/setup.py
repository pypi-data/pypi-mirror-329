import os
from setuptools import setup, find_packages

readme_path = os.path.join(os.path.dirname(__file__), 'readme.md')
try:
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    packages = find_packages(),
    name = 'shortwalk',
    version='0.0.3',
    author="Stanislav Doronin",
    author_email="mugisbrows@gmail.com",
    url='https://github.com/mugiseyebrows/shortwalk',
    description='os.walk with maxdepth option',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = []
)