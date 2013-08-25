# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import astrometrics as ions
import astrometrics.utils as utils
from astrometrics.worker import LOG
from astrometrics.cloud_connect.methods import LISTMTD


class list(object):
    """A class collection of all list methods."""

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args

    def start(self):
        """Run the list method."""

        for method in LISTMTD.keys():
            if method in self.args:
                if method in ['instances', 'providers']:
                    function = getattr(self, method)
                    self.parse_data(data=function())
                    break
                else:
                    self.parse_data(
                        data=self.magic(action=LISTMTD.get(method))
                    )
                    break
        else:
            raise ions.SystemError('No Parseable Functions were found.')

    def parse_data(self, data):
        """Parse the data that has been returned by the Cloud API."""

        if not data:
            print('\nNo Data was returned for this search\n')
        elif self.args.get('filter'):
            data_set = [dict(item) for item in data]
            LOG.debug(data_set)
            filtered = [obj.items() for obj in data_set
                        for term in self.args.get('filter')
                        if term.upper() in obj.get('name').upper()]
            if filtered:
                utils.print_horiz_table(data=filtered)
            else:
                print('\nNothing Found When Filtering. '
                      'Review your Filter and Try Again\n')
        else:
            utils.print_horiz_table(data=data)

    def magic(self, action):
        """Parse and return Data into more usable Data."""

        function = getattr(self.conn, action)
        action = function()
        if all([isinstance(fct, str) for fct in action]):
            return [(('id', type(fct)), ('name', fct)) for fct in action]
        if all([isinstance(fct, dict) for fct in action]):
            return [fct.items() for fct in action]
        else:
            return [(('id', fct.id), ('name', fct.name)) for fct in action]

    def instances(self):
        """Return a list of tuples for all nodes."""

        def form(info):
            ips = utils.ret_ipv4(data=info)
            if len(ips) > 1:
                return ', '.join([ips[0], '(...)'])
            else:
                return ', '.join(ips)

        return [(('id', node.id),
                 ('name', node.name),
                 ('public_ips', form(info=node.public_ips)),
                 ('private_ips', form(info=node.private_ips)),
                 ('state', node.state)) for node in self.conn.list_nodes()]

    def providers(self):
        """Return a list of tuples for all providers."""

        import libcloud.compute.providers as providers
        return [(('name', _prov), ('value', _type[1]))
                for _prov, _type in providers.DRIVERS.items()]
