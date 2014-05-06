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


def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output

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

    def clone_all(self):
        for repo in self.repos:
            full_repo_description = get_full_repo_description(
                self.protocol, self.remote, self.organization, repo)
            output = check_output(['git', 'clone', full_repo_description])
            print(repo)
            print(output)


def get_full_repo_description(protocol, remote, organization, repo):
    protocol_info = {
        'git': ('@', ':'),
        'https': ('://', '/'),
    }
    try:
        protocol_delimiter, repo_delimiter = protocol_info[protocol]
    except KeyError:
        raise Exception('Unknown protocol: %s, must be one of %s' % (
            protocol, ' '.join(protocol_info.keys())))
    return protocol + protocol_delimiter + remote + repo_delimiter + organization + '/' + repo


commands = {
    'clone': 'clone_all',
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
