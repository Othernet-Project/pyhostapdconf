import os
from setuptools import setup, find_packages

import hostapdconf as pkg


def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = pkg.__version__

setup(
    name='pyhostapdconf',
    description='Library for working with hostapd configuation files',
    version=VERSION,
    author='Outernet Inc',
    author_email='apps@outernet.is',
    license='GPLv3',
    url='https://github.com/Outernet-Project/confloader',
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: System :: Hardware',
        'Topic :: Utilities',
    ]
)
