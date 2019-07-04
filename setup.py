#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;


import sys

from setuptools import setup

required = ['tlslite-ng', 'lxml']

if sys.version_info[:3] < (2, 9, 0):
    raise NotImplemented('Python 3.5+ required, bye-bye')

setup(name='gdata-python3',
      version='3.0.1',
      description='Python client library for Google data APIs',
      long_description="""\
The Google data Python client library makes it easy to interact with
Google services through the Google Data APIs. This library provides data
models and service modules for the the following Google data services:
- Google Calendar data API
- Google Contacts data API
- Google Spreadsheets data API
- Google Document List data APIs
- Google Base data API
- Google Apps Provisioning API
- Google Apps Email Migration API
- Google Apps Email Settings API
- Picasa Web Albums Data API
- Google Code Search Data API
- YouTube Data API
- Google Webmaster Tools Data API
- Blogger Data API
- Google Health API
- Google Book Search API
- Google Analytics API
- Google Finance API
- Google Sites Data API
- Google Content API For Shopping
- Google App Marketplace API
- Google Content API for Shopping
- core Google data API functionality
The core Google data code provides sufficient functionality to use this
library with any Google data API (even if a module hasn't been written for
it yet). For example, this client can be used with the Notebook API. This
library may also be used with any Atom Publishing Protocol service (AtomPub).
""",
      author='Jeffrey Scudder',
      author_email='j.s@google.com',
      license='Apache 2.0',
      url='https://github.com/dvska/gdata-python3',
      packages=[
          'atom',
          'gdata',
          'gdata.acl',
          'gdata.alt',
          'gdata.analytics',
          'gdata.apps',
          'gdata.apps.adminsettings',
          'gdata.apps.audit',
          'gdata.apps.emailsettings',
          'gdata.apps.groups',
          'gdata.apps.migration',
          'gdata.apps.multidomain',
          'gdata.apps.organization',
          'gdata.blogger',
          'gdata.calendar',
          'gdata.calendar_resource',
          'gdata.codesearch',
          'gdata.contacts',
          'gdata.contentforshopping',
          'gdata.docs',
          'gdata.dublincore',
          'gdata.exif',
          'gdata.geo',
          'gdata.media',
          'gdata.oauth',
          'gdata.opensearch',
          'gdata.photos',
          'gdata.projecthosting',
          'gdata.sites',
          'gdata.spreadsheet',
          'gdata.spreadsheets',
          'gdata.webmastertools',
          'gdata.youtube',
      ],
      package_dir={'': 'src'},
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=required
      )
