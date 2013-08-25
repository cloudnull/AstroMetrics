# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
from astrometrics import info


def default_args(parser):
    """Add in Default Arguments to the parser.

    :param parser:
    """

    parser.add_argument('--log-level',
                        choices=['warn', 'info', 'error', 'critical', 'debug'],
                        default='info',
                        help='Set the Log Level')
    parser.add_argument('--version',
                        '-V',
                        action='version',
                        version=info.VINFO)
