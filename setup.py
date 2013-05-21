# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='django-cadoshop',
    version='0.1.0',
    description='Cado Shop',
    author='Frank Wawrzak (CadoSolutions)',
    author_email='frank.wawrzak@cadosolutions.com',
    url='https://github.com/fsw/django-cadoshop',
    download_url='git://github.com/fsw/django-cadoshop.git',
    packages=['cadoshop'],
    install_requires=[
		'plata',
        'xlwt',
    ],
)
