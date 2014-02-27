"""
usage: sl search [<args>...] [options]

@TODO Add usage here
"""
# :copyright: (c) 2013, SoftLayer Technologies, Inc. All rights reserved.
# :license: BSD, see LICENSE for more details.
# SoftLayer/CLI/modules

from os import linesep
import os.path
from textwrap import TextWrapper

from SoftLayer import SearchManager
from SoftLayer.utils import console_input
from SoftLayer.CLI import (
    CLIRunnable, Table, listing,
    FormattedItem)
from SoftLayer.CLI.helpers import (
    CLIAbort, ArgumentError, NestedDict, blank)

class Search(CLIRunnable):
    """
usage: 
sl search [--types=TYPES] [options]
sl search [--query=QUERY] [--types=TYPES] [options]

Filters:
  -Q --query=QUERY      The search string or query to use, must be within quotes. 
  --types=TYPES         Object types to search for, comma seperated.

Search SoftLayer API object data using plain language DSL. The primary objective 
is to make it easier to find something. If you just use 'sl search' it will prompt 
you for a search string to use to search against all available data types.  
"""
    action = None
    search_prompt = '\n Search String: '
    default_column_width = 60

    def execute(self, args):
        searchService = SearchManager(self.client)

        query = None
        if args.get('--query'):
            query = args.get('--query')
        else:
            query = console_input(self.search_prompt)

        types = None
        if args.get('--types'):
          types = args.get('--types').split(',')

        if query == None:
            query = '*'

        results = searchService.search(query, types)

        type_mapping = searchService.getTypeMapping()
        reversed_type_mapping = dict((longer,short) for short,longer in type_mapping.iteritems())

        if results:
            results_table = Table([
                'Id', 'Object Type', 'Name'
            ])

            wrapper = TextWrapper(width=self.default_column_width)

            for result in results:
                searchContainerResult = NestedDict(result)

                identifier = searchContainerResult['resource'].get('id') or blank()
                resource_type = blank()
                name = blank()

                if searchContainerResult['resourceType'] in reversed_type_mapping.keys():
                    resource_type = reversed_type_mapping[searchContainerResult['resourceType']]

                if resource_type == 'SoftLayer_Hardware':
                    name = searchContainerResult['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'SoftLayer_Virtual_Guest':
                    name = searchContainerResult['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'SoftLayer_Ticket':
                    name = searchContainerResult['resource'].get('title')
                elif resource_type == 'SoftLayer_Network_Subnet_IpAddress':
                    name = searchContainerResult['resource'].get('ipAddress')
                elif resource_type == 'SoftLayer_Network_Vlan':
                    name = '.'.join([
                        searchContainerResult['resource'].get('primaryRouter').get('hostname'),
                        searchContainerResult['resource'].get('vlanNumber')
                    ])
                elif resource_type == 'SoftLayer_Network_Application_Delivery_Controller':
                    name = searchContainerResult['resource'].get('name')
                elif resource_type == 'SoftLayer_Network_Vlan_Firewall':
                    name = searchContainerResult['resource'].get('fullyQualifiedDomainName')

                results_table.add_row([
                    identifier,
                    resource_type,
                    wrapper.wrap(name)
                ])

            return results_table

        raise CLIAbort("No objects found matching: %s" % query)

