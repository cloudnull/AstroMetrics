# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import argparse
import ConfigParser
import inspect
import os

from astrometrics.arguments import arguments
from astrometrics import gen_utils
from astrometrics import info


def set_parser():
    """Set the default Parser."""

    home = os.getenv('HOME')
    config_file_name = '%s/.astro' % home

    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument(
        '-C',
        '--config-file',
        metavar='',
        type=str,
        default=os.getenv('CLOUD_CONFIG', config_file_name),
        help=('Path to a Configuration file. This is an optional argument used'
              ' to specify Anything you may want in your environment. '
              'The file is in INI format. Default: "%(default)s"')
    )

    conf_parser.add_argument(
        '-E',
        '--environment',
        metavar='',
        type=str,
        default=None,
        help='Name of Environment Section in your "config-file"'
    )

    args = argparse.ArgumentParser(
        parents=[conf_parser],
        usage='%(prog)s',
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=28
        ),
        description=info.__description__,
        epilog=info.__copyright__)

    subparser = args.add_subparsers(
        title='Positional Arguments',
        metavar=''
    )

    return conf_parser, args, subparser


def args_setup():
    """Set and return all Parsed all Arguments.

    :return parser:
    """

    # Load all of the optional Arguments
    conf_parser, parser, subparser = set_parser()

    functions = inspect.getmembers(arguments, inspect.isfunction)
    for path_arg in [parg for parg in functions]:
        name, function = path_arg
        if name.endswith('subargs'):
            function(subparser)
        elif name.endswith('optargs'):
            function(parser)

    # Get Default ARGS from file if used
    args, remaining_argv = conf_parser.parse_known_args()

    _args = vars(args)

    sysconfig = _args.get('config_file')

    if sysconfig is not None and os.path.exists(sysconfig):
        if _args.get('environment') is not None:
            config = ConfigParser.SafeConfigParser()
            config.read([sysconfig])
            section = _args.get('environment')
            if section in config.sections():
                default = dict(config.items(section))
            else:
                raise SystemExit(
                    'Section "%s" was not found in config file "%s"'
                    % (section, sysconfig)
                )

            # If key is None, rip it out.
            for key, value in default.iteritems():
                if value.upper() == 'TRUE' or value.lower() == 'true':
                    default[key] = True
                elif value.upper() == 'FALSE' or value.lower() == 'false':
                    default[key] = False
                elif value.upper() == 'NONE' or value.lower() == 'none':
                    default[key] = None

            # Set the known defaults if file is used.
            parser.set_defaults(**default)

    # Parse the Arguments.
    return parser


def get_help():
    """Get Argument help.

    :returns parser.print_help(): returns help information.
    """

    return args_setup().print_help()


def get_args():
    """Parse all arguments to run the application.

    :returns vars(parser.parse_args()): args as a dictionary
    """

    return gen_utils.parse_dictionary(
        dictionary=vars(
            args_setup().parse_args()
        )
    )
