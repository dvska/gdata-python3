#
# Copyright 2009 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Data model for parsing and generating XML for the Google Apps Marketplace Licensing API."""

# __author__ = 'Alexandre Vivien <alex@simplecode.fr>'

import atom.core
import gdata.data

LICENSES_NAMESPACE = 'http://www.w3.org/2005/Atom'
LICENSES_TEMPLATE = '{%s}%%s' % LICENSES_NAMESPACE


class Enabled(atom.core.XmlElement):
    """ """

    _qname = LICENSES_TEMPLATE % 'enabled'


class Id(atom.core.XmlElement):
    """ """

    _qname = LICENSES_TEMPLATE % 'id'


class CustomerId(atom.core.XmlElement):
    """ """

    _qname = LICENSES_TEMPLATE % 'customerid'


class DomainName(atom.core.XmlElement):
    """ """

    _qname = LICENSES_TEMPLATE % 'domainname'


class InstallerEmail(atom.core.XmlElement):
    """  """

    _qname = LICENSES_TEMPLATE % 'installeremail'


class TosAcceptanceTime(atom.core.XmlElement):
    """  """

    _qname = LICENSES_TEMPLATE % 'tosacceptancetime'


class LastChangeTime(atom.core.XmlElement):
    """  """

    _qname = LICENSES_TEMPLATE % 'lastchangetime'


class ProductConfigId(atom.core.XmlElement):
    """  """

    _qname = LICENSES_TEMPLATE % 'productconfigid'


class State(atom.core.XmlElement):
    """  """

    _qname = LICENSES_TEMPLATE % 'state'


class Entity(atom.core.XmlElement):
    """ The entity representing the License. """

    _qname = LICENSES_TEMPLATE % 'entity'

    enabled = Enabled
    id = Id
    customer_id = CustomerId
    domain_name = DomainName
    installer_email = InstallerEmail
    tos_acceptance_time = TosAcceptanceTime
    last_change_time = LastChangeTime
    product_config_id = ProductConfigId
    state = State


class Content(atom.data.Content):
    entity = Entity


class LicenseEntry(gdata.data.GDEntry):
    """ Represents a LicenseEntry object. """

    content = Content


class LicenseFeed(gdata.data.GDFeed):
    """ Represents a feed of LicenseEntry objects. """

    # Override entry so that this feed knows how to type its list of entries.
    entry = [LicenseEntry]
