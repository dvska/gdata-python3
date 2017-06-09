#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;


"""Contains the data classes of the Google Access Control List (ACL) Extension"""

# __author__ = 'j.s@google.com (Jeff Scudder)'

import atom.data
import gdata.opensearch.data

GACL_TEMPLATE = '{http://schemas.google.com/acl/2007}%s'


class AclRole(atom.core.XmlElement):
    """Describes the role of an entry in an access control list."""
    _qname = GACL_TEMPLATE % 'role'
    value = 'value'


class AclAdditionalRole(atom.core.XmlElement):
    """Describes an additionalRole element."""
    _qname = GACL_TEMPLATE % 'additionalRole'
    value = 'value'


class AclScope(atom.core.XmlElement):
    """Describes the scope of an entry in an access control list."""
    _qname = GACL_TEMPLATE % 'scope'
    type = 'type'
    value = 'value'


class AclWithKey(atom.core.XmlElement):
    """Describes a key that can be used to access a document."""
    _qname = GACL_TEMPLATE % 'withKey'
    key = 'key'
    role = AclRole
    additional_role = AclAdditionalRole


class AclEntry(gdata.data.GDEntry):
    """Describes an entry in a feed of an access control list (ACL)."""
    scope = AclScope
    role = AclRole
    with_key = AclWithKey
    additional_role = AclAdditionalRole


class AclFeed(gdata.data.GDFeed):
    """Describes a feed of an access control list (ACL)."""
    entry = [AclEntry]
