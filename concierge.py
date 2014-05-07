#!/usr/bin/env python2

import os
import sys
import subprocess
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

file_name = __file__
file_dir = os.path.dirname(os.path.realpath(file_name))

class Concierge:
    def __init__(self, config_file):
        config = configparser.SafeConfigParser()
        config.read(config_file)
        repo_section = 'repos'
        self.repos = config.get(repo_section, 'repos').split(',')
        self.setup_order = config.get(repo_section, 'setup_order').split(',')
        self.run_repos = config.get(repo_section, 'run_repos').split(',')

        git_section = 'git'
        self.protocol = config.get(git_section, 'protocol')
        self.remote = config.get(git_section, 'remote')
        self.organization = config.get(git_section, 'organization')


commands = {
}


def usage():
    print('Usage %s ini_file [%s]' % (file_name, '|'.join(commands.keys())))
    sys.exit(1)


def main(argv):
    if len(argv) < 3:
        usage()
    try:
        command = commands[argv[2]]
    except KeyError:
        print("Unknown command %s" % (argv[2],))
        usage()
    concierge = Concierge(argv[1])
    getattr(concierge, command)()

if __name__ == '__main__':
    main(sys.argv)
