#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;


"""Contains the data classes of the Dublin Core Metadata Initiative (DCMI) Extension"""

# __author__ = 'j.s@google.com (Jeff Scudder)'

import atom.core

DC_TEMPLATE = '{http://purl.org/dc/terms/}%s'


class Creator(atom.core.XmlElement):
    """Entity primarily responsible for making the resource."""
    _qname = DC_TEMPLATE % 'creator'


class Date(atom.core.XmlElement):
    """Point or period of time associated with an event in the lifecycle of the resource."""
    _qname = DC_TEMPLATE % 'date'


class Description(atom.core.XmlElement):
    """Account of the resource."""
    _qname = DC_TEMPLATE % 'description'


class Format(atom.core.XmlElement):
    """File format, physical medium, or dimensions of the resource."""
    _qname = DC_TEMPLATE % 'format'


class Identifier(atom.core.XmlElement):
    """An unambiguous reference to the resource within a given context."""
    _qname = DC_TEMPLATE % 'identifier'


class Language(atom.core.XmlElement):
    """Language of the resource."""
    _qname = DC_TEMPLATE % 'language'


class Publisher(atom.core.XmlElement):
    """Entity responsible for making the resource available."""
    _qname = DC_TEMPLATE % 'publisher'


class Rights(atom.core.XmlElement):
    """Information about rights held in and over the resource."""
    _qname = DC_TEMPLATE % 'rights'


class Subject(atom.core.XmlElement):
    """Topic of the resource."""
    _qname = DC_TEMPLATE % 'subject'


class Title(atom.core.XmlElement):
    """Name given to the resource."""
    _qname = DC_TEMPLATE % 'title'
