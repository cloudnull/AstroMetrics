# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
LOG = None
QUEUE = None
DEQUE = None


def load_constants(log_method):
    """Setup In Memory Persistent Logging.

    :param log_method: Set method for logging
    """

    import astrometrics.utils as utils

    global LOG, QUEUE, DEQUE
    LOG = log_method
    QUEUE = utils.basic_queue()
    DEQUE = utils.basic_deque()


def start_work(set_args):
    """Begin Work.

    :param set_args: Arguments that have been parsed for in application use.
    """

    import pkgutil

    from astrometrics.cloud_connect import methods as cks
    import astrometrics.utils as utils

    def get_method(name):
        """Import what is required to run the System."""

        to_import = '%s.%s' % (cks.__name__, name)
        return __import__(to_import, fromlist="None")

    def get_actions(module):
        """Get all available actions from an imported method."""

        classes = [c for c in module.__dict__.values() if isinstance(c, type)]
        return [c for c in classes if issubclass(c, tuple(classes))]

    def run_action(actions):
        """Run the action."""

        for action in actions:
            if set_args.get(action.__name__) is not None:
                action(conn=conn, args=set_args).start()
                break

    def get_options(connection):
        """Show all Driver Options for a Provider."""

        testing = [(('command', method), ('documentation', method.__class__))
                   for method in dir(connection) if not method.startswith('_')]
        utils.print_horiz_table(data=testing)

    # Set an Open Connection
    conn = utils.ret_conn(args=set_args)

    # Testing Code
    if set_args.get('show_opts'):
        get_options(connection=conn)
    else:
        for mod, name, package in pkgutil.iter_modules(cks.__path__):
            if set_args.get(name) is not None:
                method = get_method(name=name)
                actions = get_actions(module=method)
                run_action(actions=actions)
                break
