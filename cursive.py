"""The `cursive` command-line program itself."""

import sys
from optparse import OptionParser
from pkg_resources import iter_entry_points

# Load the command plugins.
COMMANDS = {}
for point in iter_entry_points(group='cursive.commands', name=None):
    COMMANDS[point.name] = point.load()

def verbose_help(option, opt, value, parser):
    """Print verbose help, as from the --help option."""
    parser.print_help()
    print
    print 'Available Commands:'
    print
    name_length = max( len(n) for n in COMMANDS.keys() )
    for name, func in sorted(COMMANDS.items()):
        docline = func.__doc__.split('\n')[0].strip().strip('.')
        print(' {0:{1}} - {2}'.format(name, name_length, docline))
    parser.exit()
    return

def console_script_cursive():
    """Command-line script printing how many words are in a document."""

    parser = OptionParser(
        usage='usage: %prog [options] <command> [options]',
        conflict_handler='resolve',
        description='Welcome to cursive, the suite of tools for authors using Restructured Text!',
        )
    # Override the default --help behavior.  Leave -h alone to show short help.
    parser.add_option('--help',
                      action='callback',
                      callback=verbose_help,
                      help='Show verbose help, including a list of commands.',
                      )
    (options, args) = parser.parse_args()

    if not args or args[0] not in COMMANDS:
        verbose_help(None, None, None, parser)

    command = COMMANDS[args[0]]
    del sys.argv[1]
    command()
