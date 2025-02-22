from setuptools import setup, find_packages
from os import path


working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='json_to_df',
    version='0.0.1',
    url='https://github.com/SourinKarmakar/json_to_df',
    author='Sourin Karmakar',
    author_email='sourinkarmakar@gmail.com',
    description='Package to convert nested JSON to dataframes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)
