# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import sys

from astrometrics import arguments
from astrometrics.logger import logger
from astrometrics.worker import load_constants as const
from astrometrics.worker import start_work as start


def executable():
    """Look for flags, these are all of the available start options."""

    if len(sys.argv) == 1:
        arguments.get_help()
        sys.exit('\nGive me something to do and I will do it\n')
    else:
        # Parse the Arguments that have been provided
        args = arguments.get_args()

        # Load The System Logger
        log = logger.load_in(log_level=args.get('log_level', 'info'))
        log.debug('Used Arguments %s', args)
        const(log_method=log)

        # Begin Work
        start(set_args=args)


if __name__ == '__main__':
    executable()
