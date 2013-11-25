# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import pkgutil

from astrometrics.cloud_connect import methods as cks
import astrometrics.base_utils as base_utils
import astrometrics.gen_utils as gen_utils


LOG = None
QUEUE = None
DEQUE = None


def load_constants(log_method):
    """Setup In Memory Persistent Logging.

    :param log_method: Set method for logging
    """

    global LOG, QUEUE, DEQUE
    LOG = log_method
    QUEUE = base_utils.basic_queue()
    DEQUE = base_utils.basic_deque()


def start_work(set_args):
    """Begin Work.

    :param set_args: Arguments that have been parsed for in application use.
    """

    def get_method(name):
        """Import what is required to run the System."""

        to_import = '%s.%s' % (cks.__name__, name)
        return __import__(to_import, fromlist="None")

    #def get_options(connection):
    #    """Show all Driver Options for a Provider."""
    #
    #    testing = [(('command', method), ('documentation', method.__class__))
    #               for method in dir(connection) if not method.startswith('_')]
    #    gen_utils.print_horiz_table(data=testing)

    # Set an Open Connection
    conn = base_utils.ret_conn(args=set_args)

    action = set_args.get('method')
    action = action.replace('-', '_')

    for mod, name, package in pkgutil.iter_modules(cks.__path__):
        action_arg = action.split('_')
        if name.startswith(action_arg[0]):
            imported_module = get_method(name=name)
            run_action = imported_module.Actions(conn=conn, args=set_args)
            run_action.start()
            break
    else:
        raise SystemExit('No Method Found to peroform action "%s"' % action)
