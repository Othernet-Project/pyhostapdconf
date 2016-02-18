import os
from setuptools import setup, find_packages

import hostapdconf as pkg


def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = pkg.__version__

setup(
    name='pyhostapdconf',
    version=VERSION,
    license='GPLv3',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: System :: Hardware',
        'Topic :: Utilities',
    ]
)
