#!/usr/bin/env python

import sys

assert sys.version >= '2.5', "Requires Python v2.5 or above."
from distutils.core import setup
from setuptools import find_packages

setup(
    name="django-impersonation",
    version="1.0",
    author="Ignacio Alvarez",
    author_email="ignacioalvarez92@gmail.com",
    url="https://github.com/nachoaIvarez/django-impersonation",
    description="An app to add a 'Log in as this user' button in the Django"
                "user admin page.",
    long_description="A short Django app that adds a button in the Django"
                     "user admin page. When a superuser clicks the button, "
                     "they are instantly logged in as that user.",
    license="BSD",
    keywords="django, login, as, impersonate, user, impersonation, loginas",
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
)
