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
from SoftLayer.CLI import (
    CLIRunnable, Table, no_going_back, confirm, mb_to_gb, listing,
    FormattedItem)
from SoftLayer.CLI.helpers import (
    CLIAbort, ArgumentError, SequentialOutput, NestedDict, blank, resolve_id)

class Search(CLIRunnable):
    """
usage: sl search [--query=QUERY] [--types=TYPES] [options]

Filters:
  -Q --query=QUERY      Query for search
  --types=TYPES         Object types to search for, comma seperated.

Search SoftLayer API objects
"""
    action = None

    def execute(self, args):
        searchService = SearchManager(self.client)

        query = args.get('--query')
        types = None

        if args.get('--types'):
          types = args.get('--types').split(',')

        results = searchService.search(query, types)

        t = Table([
            'id', 'resource type', 'score',
        ])

        for result in results:
            searchContainerResult = NestedDict(result)
            t.add_row([
                searchContainerResult['resource'].get('id') or searchContainerResult['resource'].get('objectId') or blank(),
                searchContainerResult['resourceType'] or blank(),
                searchContainerResult['relevanceScore'] or blank(),
            ])

        return t

