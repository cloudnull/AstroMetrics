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

from astrometrics.arguments import authentication
from astrometrics.arguments import default
from astrometrics.arguments import list
from astrometrics.arguments import node
from astrometrics.arguments import volume
from astrometrics import info
from astrometrics import utils


def set_parser():
    """Set the default Parser."""

    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description=info.__description__,
        argument_default=None,
        epilog=info.__copyright__
    )

    subparser = parser.add_subparsers(title='Infrastructure Actions',
                                      metavar='<COMMANDS>\n')
    return parser, subparser


def args_setup():
    """Set and return all Parsed all Arguments.

    :return parser:
    """

    parser, subparser = set_parser()

    # Anything that uses the subparser
    node.node_args(subparser=subparser)
    list.list_args(subparser=subparser)
    list.show_args(subparser=subparser)
    volume.node_args(subparser=subparser)

    # Everything else which uses the parser
    authentication.auth_args(parser=parser)
    default.default_args(parser=parser)

    opts = subparser.add_parser('show-opts',
                                help='Show Driver Options, made for testing.')
    opts.set_defaults(show_opts=True)

    return parser


def get_help():
    """Get Argument help.

    :returns parser.print_help(): returns help information.
    """

    parser = args_setup()
    return parser.print_help()


def get_args():
    """Parse all arguments to run the application.

    :returns vars(parser.parse_args()): args as a dictionary
    """

    parser = args_setup()
    return utils.parse_dictionary(dictionary=vars(parser.parse_args()))
