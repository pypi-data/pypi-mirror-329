# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='InfrontConnect',
    version='1.0.17',

    description='Infront Desktop API for Python 3',

    author='Infront ASA',
    author_email='support@infrontfinance.com',
    license='MIT',
    install_requires=['requests', 'pandas', 'backoff'],

    keywords='infront desktop API finance',

    packages=find_packages(),

)
