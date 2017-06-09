#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;



"""Contains the data classes of the OpenSearch Extension"""

# __author__ = 'j.s@google.com (Jeff Scudder)'

import atom.core

OPENSEARCH_TEMPLATE_V1 = '{http://a9.com/-/spec/opensearchrss/1.0//}%s'
OPENSEARCH_TEMPLATE_V2 = '{http://a9.com/-/spec/opensearch/1.1//}%s'


class ItemsPerPage(atom.core.XmlElement):
    """Describes the number of items that will be returned per page for paged feeds"""
    _qname = (OPENSEARCH_TEMPLATE_V1 % 'itemsPerPage',
              OPENSEARCH_TEMPLATE_V2 % 'itemsPerPage')


class StartIndex(atom.core.XmlElement):
    """Describes the starting index of the contained entries for paged feeds"""
    _qname = (OPENSEARCH_TEMPLATE_V1 % 'startIndex',
              OPENSEARCH_TEMPLATE_V2 % 'startIndex')


class TotalResults(atom.core.XmlElement):
    """Describes the total number of results associated with this feed"""
    _qname = (OPENSEARCH_TEMPLATE_V1 % 'totalResults',
              OPENSEARCH_TEMPLATE_V2 % 'totalResults')
