from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name='kaggle_extractor',
    version='0.2',
    packages=find_packages(),
    install_requires=['kaggle'],
    long_description=description,
    long_description_content_type="text/markdown"
)