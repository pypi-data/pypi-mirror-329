# coding: utf-8
from __future__ import print_function, unicode_literals
import sys
import codecs
from setuptools import setup, find_packages
from exafs_neo._version import __version__, __author__, __email__


def long_description():
    with codecs.open('README.md', 'rb') as readme:
        if not sys.version_info < (3, 0, 0):
            return readme.read().decode('utf-8')


setup(
    name='exafs_neo',
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__email__,
    keywords=['exafs_neo', 'AI', 'analysis'],
    description='exafs_neo AI analysis using GA',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/laumiulun/EXAFS_Neo',
    download_url='https://github.com/laumiulun/EXAFS_Neo/tarball/master',
    package_data={"gui": ["media/*"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'xraylarch',
        'attrs',
        'matplotlib',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'exafs_neo = exafs_neo.input_arg:main',
            'exafs_neo_gui = exafs_neo.gui.XAFS_GUI:main',
        ]
    },
    license='GPLv3',
)
