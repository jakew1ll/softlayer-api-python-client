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
usage: sl search [--query=QUERY_STRING]
                   [options]

@TODO Add documented options out here


Search SoftLayer API objects
"""
    action = None

    @staticmethod
    def execute(client, args):
        searchService = SearchManager(client)

        query = args.get('--query')
        data = {}

        results = searchService.search(query)

        print str(results)

        t = Table([
            'id', 'datacenter', 'host',
            'cores', 'memory', 'primary_ip',
            'backend_ip', 'active_transaction',
        ])

        return t


class GetSearchTypes(CLIRunnable):
    """
usage: sl search types
                   [options]

@TODO Add documented options out here


Get SoftLayer API object types that are available 
for search.
"""
    action = 'types'

    @staticmethod
    def execute(client, args):
        searchService = SearchManager(client)

        query = args.get('--query')
        data = {}

        results = searchService.search(query)

        print str(results)

        t = Table([
            'id', 'datacenter', 'host',
            'cores', 'memory', 'primary_ip',
            'backend_ip', 'active_transaction',
        ])

        return t