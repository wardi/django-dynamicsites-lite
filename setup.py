import os
import sys
from distutils.core import setup

version = __import__('dynamicsites').get_version()

setup(
    name='dynamicsites',
    version=version,
    description="Host multiple sites from a single django project",
    long_description="""Expands the standard django.contrib.sites package to allow for:
    Sites identified dynamically from the request via middleware
    No need for multiple virtual hosts at the webserver level
    301 Redirects to canonical hostnames
    Allows for a site to support multiple subdomains
    Allows for a site to be an independent subdomain of another site
    A site may have its own urls.py and templates
    A single site may accept requests from multiple hostnames
    Allows for environment hostname mappings to use non-production hostnames (for use in dev, staging, test, etc. environments)""",
    author='UYSRC',
    author_email='mtrier@gmail.com',
    maintainer='Bas van Oostveen',
    maintainer_email='v.oostveen@gmail.com',
    url='https://bitbucket.org/ladyrassilon/django-dynamicsites',
    license='Free as in Beer',
    platforms=['any'],
    packages=['dynamicsites'],
)