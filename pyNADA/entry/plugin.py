import pkg_resources
ENTRY_POINT = 'pyNADA.cmdline'

class Plugin(object):
    def registerSubparser(self, parent):
        raise NotImplementedError()

def load_plugins(argparser):
    subparsers = argparser.add_subparsers()

    for entrypoint in pkg_resources.iter_entry_points(ENTRY_POINT):
        plugin_class = entrypoint.load(require=False)
        plugin_class.registerSubparser(subparsers)

