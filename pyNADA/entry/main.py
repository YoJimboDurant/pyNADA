import argparse

import pyNADA.entry.plugin

def main():
    parser = argparse.ArgumentParser()
    pyNADA.entry.plugin.load_plugins(parser)

    args = parser.parse_args()
    args.subcommand(args)
