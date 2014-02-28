"""
usage: sl search [<args>...] [options]

@TODO Add usage here
"""
# :copyright: (c) 2013, SoftLayer Technologies, Inc. All rights reserved.
# :license: BSD, see LICENSE for more details.
# SoftLayer/CLI/modules

from textwrap import TextWrapper
from SoftLayer import SearchManager
from SoftLayer.utils import (
    console_input, getSimpleType, getApiType)
from SoftLayer.CLI import (
    CLIRunnable, Table)
from SoftLayer.CLI.helpers import (
    CLIAbort, NestedDict, blank)

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
          simple_types = args.get('--types').split(',')
          types = [getApiType(x) for x in simple_types]

        if query == None:
            query = '*'

        results = searchService.search(query, types)

        if results:
            results_table = Table([
                'Id', 'Type', 'Name'
            ])
            results_table.align['Name'] = 'l'

            wrapper = TextWrapper(width=self.default_column_width, expand_tabs=False)

            for result in results:
                result = NestedDict(result)

                identifier = result['resource'].get('id') or blank()
                resource_type = getSimpleType(result['resourceType'])
                name = blank()
                if resource_type == 'hardware':
                    name = result['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'cci':
                    name = result['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'ticket':
                    name = result['resource'].get('title')
                elif resource_type == 'ip_address':
                    name = result['resource'].get('ipAddress')
                elif resource_type == 'vlan':
                    name = '.'.join([
                        result['resource'].get('primaryRouter').get('hostname'),
                        result['resource'].get('vlanNumber')
                    ])
                elif resource_type == 'loadbalancer':
                    name = result['resource'].get('name')
                elif resource_type == 'firewall':
                    name = result['resource'].get('fullyQualifiedDomainName')

                if (name and name != 'NULL') or not args.get('--raw'):
                    name = wrapper.wrap(name)

                results_table.add_row([
                    identifier,
                    resource_type,
                    name
                ])

            return results_table

        raise CLIAbort("No objects found matching: %s" % query)

