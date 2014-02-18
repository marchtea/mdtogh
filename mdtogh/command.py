"""\
mdtog.command
-------------------

Implements the command-line interface for md to github.


Usage:
  mdtogh [options] <path>
  mdtogh -h | --help
  mdtogh --version

Where:
  <path> is a file or a directory to render, default to .

Options:
  --gfm             Use GitHub-Flavored Markdown, e.g. comments or issues
  --context=<repo>  The repository context, only taken into account with --gfm
  --user=<username> GitHub username for API authentication
  --pass=<password> GitHub password for API authentication
  --toc             Generate table of contents
  --offline         Use offline renderer
"""
__version__ = '0.0.1'

import sys
from docopt import docopt
import json 

usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])

def main(argv=None):
    """Entry point of this application"""
    if argv is None:
        argv = sys.argv[1:]
    version = 'mdtogh ' + __version__

    args = docopt(usage, argv=argv, version=version)

    print json.dump(args)
    

if __name__ == '__main__':
	main()
