#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License 2.0;



# This module is used for version 2 of the Google Data APIs.


"""Provides a base class to represent property elements in feeds.

This module is used for version 2 of the Google Data APIs. The primary class
in this module is AppsProperty.
"""

# __author__ = 'Vic Fryzel <vicfryzel@google.com>'

import atom.core
import gdata.apps


class AppsProperty(atom.core.XmlElement):
    """Represents an <apps:property> element in a feed."""
    _qname = gdata.apps.APPS_TEMPLATE % 'property'
    name = 'name'
    value = 'value'
