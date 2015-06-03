"""
,--.   ,--.,------.,------.,--.   ,--.,--.  ,--.,------.
|  |   |  ||  .---'|  .---'|  |   |  ||  ,'.|  ||  .---'
|  |   |  ||  `--, |  `--, |  |   |  ||  |' '  ||  `--,
|  '--.|  ||  |`   |  `---.|  '--.|  ||  | `   ||  `---.
`-----'`--'`--'    `------'`-----'`--'`--'  `--'`------'

Lifeline is there to help when you can't access your favorite package managers.

NOTE: Relies on npm for node, gem for Ruby, and pip for Python


Usage:
  lifeline (list)
  lifeline [FRAMEWORK...] [--preview]
  lifeline (-h | --help)
  lifeline --clean
  lifeline --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --preview     Show packages to download
"""

import os
import sys

from docopt import docopt
from subprocess import Popen

__version__ = '0.0.1'
_ROOT = os.path.abspath(os.path.dirname(__file__))
_LIFELINE_DIR_ = os.path.abspath(os.path.join(os.path.abspath(os.sep), '.lifeline'))
_FRAMEWORKS_DIR = 'packages'

INSTALL_COMMANDS = {
    'node': 'npm',
    'ruby': 'gem',
    'python': 'pip'
}

def _find_or_create_lifeline():
    if not os.path.exists(_LIFELINE_DIR_):
        os.makedirs(_LIFELINE_DIR_)

def _get_frameworks():
    frameworks = []
    for _root, _sub_folders, files in os.walk(_FRAMEWORKS_DIR):
        frameworks += files
    return sorted(frameworks)

def _parse_package_file(framework):
  _framework_file = os.path.join(_ROOT, _FRAMEWORKS_DIR, framework)
  with open(_framework_file) as f:
    lines = f.read().splitlines()
  return sorted(lines)

def _handle_preview(frameworks):
    errors = []
    packages = {}

    for framework in frameworks:
        try:
            packages[framework] = _parse_package_file(framework)
        except IOError:
            errors.append(framework)

    if packages:
        for framework in packages:
            print (framework) + ': ' + ', '.join(packages[framework])

    if errors:
        verb = '\nare' if (len(errors) > 1) else '\nis'

        print('\n'.join(errors) + verb + ' not yet supported. Feel free to submit a pull request at http://www.github.com/samuelcouch/lifeline to fix that!')


def _handle_install(frameworks):
    _find_or_create_lifeline()

    errors = []

    for framework in frameworks:
        try:
            packages = _parse_package_file(framework)
        except IOError:
            errors.append(framework)

    if errors:
        verb = '\nare' if (len(errors) > 1) else '\nis'

        print('\n'.join(errors) + verb + ' not yet supported. Feel free to submit a pull request at http://www.github.com/samuelcouch/lifeline to fix that!')

def main():
    args = docopt(__doc__, version=__version__)

    if args['list']:
        print ' '.join(_get_frameworks())
    elif args['FRAMEWORK']:
        if args['--preview']:
            _handle_preview(args['FRAMEWORK'])
        else:
            _handle_install(args['FRAMEWORK'])
    else:
        print __doc__

if __name__ == "__main__":
    main()
