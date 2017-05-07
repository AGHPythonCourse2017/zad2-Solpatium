#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy',
    'timeout-decorator'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='complexity_determinant',
    version='0.1',
    description="Complexity determinant",
    long_description=readme + '\n\n' + history,
    author="Jakub Ptak",
    author_email='solpatium003@gmail.com',
    url='https://github.com/solpatium/complexity_determinant',
    packages=[
        'complexity_determinant',
    ],
    package_dir={'complexity_determinant':
                 'complexity_determinant'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='complexity_determinant',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
