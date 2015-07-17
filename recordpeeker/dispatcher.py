import json
import re
import os
import time
from collections import defaultdict

from libmproxy.protocol.http import decoded

from recordpeeker import json_decode

def dump_json(data):
    return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

class Dispatcher(object):
    def __init__(self, host):
        self._host = host
        self._handlers = defaultdict(list)
        self._ignore = []
        self._wants_flow = []

    def register(self, path, function, flow=False):
        """
        Registers a function to call when a certain path is requested.
        The function should take one argument, a dictionary that contains
        response data.
        """
        self._handlers[path].append(function)
        if flow:
            self._wants_flow.append(function)

    def unregister(self, path, function):
        "Unregisters a previously-registered function."
        if function in self._handlers[path]:
            self._handlers[path].remove(function)

    def ignore(self, path, exact=False):
        """Ignores a path."""
        if exact:
            path = "^{0}$".format(re.escape(path))
        else:
            path = re.escape(path)
        self._ignore.append(re.compile(path))

    def should_ignore(self, path):
        for ignore in self._ignore:
            if ignore.search(path):
                return True
        return False

    def get_handlers(self, path):
        for mypath, handlers in self._handlers.iteritems():
            if mypath in path:
                return handlers
        return []

    def handle(self, flow, args):
        if not flow.request.pretty_host(hostheader=True).endswith(self._host):
            return
        if args.verbosity >= 1:
            data_path = os.getcwd() + "/data_dump/data_dump" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
            test_file = open(data_path, 'w')
            print >> test_file, "//" + str(flow.request.path)
            # print >> test_file, json.dumps(data, indent=4, sort_keys=True)
            test_file.close()

            # print flow.request.path
        if self.should_ignore(flow.request.path):
            return
        with decoded(flow.response):
            handlers = self.get_handlers(flow.request.path)
            if handlers:
                data = json_decode(flow.response.content)
                if args.verbosity >= 2:
                    test_file = open(data_path, 'w')
                    print >> test_file, json.dumps(data, indent=4, sort_keys=True)
                    test_file.close()
                    # print dump_json(data)
                for func in handlers:
                    if func in self._wants_flow:
                        func(data, flow)
                    else:
                        func(data)
            else:
                if args.verbosity >= 3:
                    data = json_decode(flow.response.content)
                    test_file = open(data_path, 'w')
                    print >> test_file, json.dumps(data, indent=4, sort_keys=True)
                    test_file.close()
                    # print dump_json(data)

