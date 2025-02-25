#!/usr/bin/env python

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-nogarbage',
    version='1.0.1',
    author='Matt Vollrath',
    author_email='tactii@gmail.com',
    maintainer='Matt Vollrath',
    maintainer_email='tactii@gmail.com',
    license='MIT',
    url='https://github.com/mvollrath/pytest-nogarbage',
    description='Ensure a test produces no garbage',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    py_modules=['pytest_nogarbage'],
    python_requires='>=3.7',
    install_requires=['pytest>=4.6.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'nogarbage = pytest_nogarbage',
        ],
    },
)
