"""
usage: sl search [<args>...] [options]

@TODO Add usage here
"""
# :copyright: (c) 2013, SoftLayer Technologies, Inc. All rights reserved.
# :license: BSD, see LICENSE for more details.
# SoftLayer/CLI/modules

from os import linesep
import os.path

from SoftLayer import SearchManager
from SoftLayer.utils import console_input
from SoftLayer.CLI import (
    CLIRunnable, Table, listing,
    FormattedItem)
from SoftLayer.CLI.helpers import (
    CLIAbort, ArgumentError, SequentialOutput, NestedDict, blank)

class Search(CLIRunnable):
    """
usage: sl search [--query=QUERY] [--types=TYPES] [options]

Filters:
  -Q --query=QUERY      The search string or query to use. If this is not used a prompt will take the query input.
  --types=TYPES         Object types to search for, comma seperated.

Search SoftLayer API objects
"""
    action = None
    search_prompt = '\n Search String: '

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

        return_value = None

        if results:
            return_value = Table([
                'Id', 'Resource Type', 'Name', 'Score'
            ])

            for result in results:
                searchContainerResult = NestedDict(result)

                identifier = searchContainerResult['resource'].get('id') or blank()
                resource_type = searchContainerResult['resourceType'] or blank()
                score = searchContainerResult['relevanceScore'] or blank()
                name = blank()

                if resource_type == 'SoftLayer_Hardware':
                    name = searchContainerResult['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'SoftLayer_Virtual_Guest':
                    name = searchContainerResult['resource'].get('fullyQualifiedDomainName')
                elif resource_type == 'SoftLayer_Ticket':
                    name = searchContainerResult['resource'].get('title')

                return_value.add_row([
                    identifier,
                    resource_type,
                    name,
                    score
                ])

        return return_value

