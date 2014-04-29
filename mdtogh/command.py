"""\
mdtogh.command
-------------------

Implements the command-line interface for md to github.


Usage:
  mdtogh [options] [<path>] ...
  mdtogh -h | --help
  mdtogh --version

Where:
  <path> is a file or a directory to render, [default: '.']

Options:
  --templates=<path>       path of templates, it should contains all three files: content.html, toc.html, index.html
  --cache_path=<path>      path to store style file cache, default to current directory
  --system_css             using system wide css.
  --css                    when NOT set, css contents are generate into html
  --abscss                 link css with absolute path, use only with --css is set 
  --gfm                    Use GitHub-Flavored Markdown, e.g. comments or issues
  --context=<repo>         The repository context, only taken into account with --gfm
  --user=<username>        GitHub username for API authentication
  --pass=<password>        GitHub password for API authentication
  --toc                    Generate table of contents
  --toc_depth=<n>          Max toc depth, default to 2
  --toc_file=<file>        You can specific a file to be toc(Just incase you have one)
  --book=<book.json>       Generate toc with book info, only used when --toc is set
  --offline                Use offline renderer
  --encoding=<utf-8>       encode for file, use only when --offline is set
  --refresh                clear cached styles & refetch them
  --file_reg=<reg_exp>     when path is a directory, using reg_exp to get file, this reg_exp must obey python's rules
                           if not set, mdtogh will get all files end with .md or .markdown, Notice: this is case-insensitive.
  --timeout=<time>         timeout for request github in second. [default: 20]

Notice:
	Due to limitation by github, the rate of anonymous access to github api is limit to 60 in an hour.
	If you need to generate more than that, please set --user & --pass.
	Also, --user & --pass are sended via https.
"""

import sys
from docopt import docopt
from .transform import transform
from . import __version__
import jinja2

usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])

#TODO:
#add custom title support
#add recursive support
#add custom template support

def main(argv=None):
    """Entry point of this application"""
    if argv is None:
        argv = sys.argv[1:]
        version = 'mdtogh ' + __version__

        args = docopt(usage, argv=argv, version=version)
        #json.dump(args, sys.stdout)

    try:
        transform(args['<path>'], args['--cache_path'], args['--system_css'], args['--css'], args['--abscss'], 
                args['--gfm'], args['--user'],args['--pass'], 
                args['--toc'], args['--toc_depth'], args['--toc_file'], args['--book'], 
                args['--offline'], args['--encoding'], args['--refresh'], args['--file_reg'], args['--templates'], args['--timeout'])
        return 0
    except ValueError as e:
      print "Error: ", e
      return 1
    except RuntimeError as e:
       print "Error: ", e
       return 1
    except jinja2.TemplateNotFound as e:
        print "Template not found ", e, "...Invalid templates path given or template miss."
    except jinja2.TemplateSyntaxError as e:
        print "Syntax Error in template ", e.args[3] if len(e.args) > 3 else '', " line "+e.args[1] if len(e.args) > 1 else '', ": ", e.args[0]
    except jinja2.TemplateError as e:
        print "jinja2 Error: ", e
    except Exception as e:
        print "Error: ", e.args
        return 1


if __name__ == '__main__':
    main()
