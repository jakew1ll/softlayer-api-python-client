"""
    SoftLayer.search
    ~~~~~~~~~~~~~
    Search Manager/helpers
    SoftLayer/managers/search.py

    :copyright: (c) 2013, SoftLayer Technologies, Inc. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import socket
from time import sleep
from itertools import repeat

from SoftLayer.utils import NestedDict, query_filter, IdentifierMixin

TYPE_DEFAULT_MASKS = {
    'SoftLayer_Hardware': [
        'id',
        'fullyQualifiedDomainName'
    ],
    'SoftLayer_Virtual_Guest': [
        'id',
        'fullyQualifiedDomainName'
    ],
    'SoftLayer_Ticket': [
        'id',
        'title'
    ]
}


class SearchManager(IdentifierMixin, object):

    type_mapping = {
        'hardware': 'SoftLayer_Hardware',
        'cci': 'SoftLayer_Virtual_Guest',
        'ticket': 'SoftLayer_Ticket'
    }

    """ Manage Search """
    def __init__(self, client):
        self.client = client
        self.searchClient = client['Search']

    # @param query string
    # @param types string[]
    def search(self, query, types=None, **kwargs):
        """ Retrieve a list of objects from SoftLayer_Search::search results based on the query.

        :param string query: Query to use for search
        :param list types: List of types to specifically search for, overriding the default of all data types.
        :param dict \*\*kwargs: response-level arguments (limit, offset, etc.)

        """

        # Default object types to search against
        object_types = self.type_mapping.values()
        # Translate short type overrides, if provided
        if types:
            object_types = [
                self.type_mapping.get(t) for t in types if t in self.type_mapping.keys()
            ]

        # Add our object types to the query
        query = '%s _objectType:%s' % (query, ','.join(object_types))

        # Set our default masks for object types we are using
        if 'mask' not in kwargs:
            type_masks = []

            for t in object_types:
                if t in TYPE_DEFAULT_MASKS.keys():
                    type_masks.append("resource(%s)[%s]" % (t , ','.join(TYPE_DEFAULT_MASKS.get(t))))

            # Set the default mask
            kwargs['mask'] = 'mask[%s]' % ','.join(type_masks)

        # print "Query : \n"
        # print query

        results = self.searchClient.search(query, **kwargs)

        return results

    def getTypeMapping(self):
        return self.type_mapping

    # @param translated bool
    def getSearchTypes(self, translated=False, **kwargs):
        return None

    # @param query string
    # @param types string[]
    def getSearchProperties(self, type, **kwargs):
        return None

