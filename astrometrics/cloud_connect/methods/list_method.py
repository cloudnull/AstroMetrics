# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import astrometrics.cloud_connect.methods as hashes
import astrometrics.gen_utils as utils
from astrometrics.worker import LOG


class Actions(object):
    """A class collection of all list methods."""

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args
        self.method = None

    def start(self):
        """Run the list method."""

        method = self.args.get('method')
        method = ''.join(method.split('list-'))
        self.method = hashes.LISTMTD.get(method)

        if hasattr(self, method):
            function = getattr(self, method)
            self.parse_data(data=function())
        else:
            self.parse_data(
                data=self.magic(
                    action=self.method['cmd']
                )
            )

    def parse_data(self, data):
        """Parse the data that has been returned by the Cloud API."""

        data = [dict(item) for item in data]
        if 'pop_keys' in self.method:
            for key in self.method['pop_keys']:
                for item in data:
                    if key in item:
                        item.pop(key)

        if not data:
            print('\nNo Data was returned for this search\n')
        elif self.args.get('filter'):
            filtered = [obj.items() for obj in data
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

        def string_type(raw_list):
            return_list = []
            num = 0
            for _fct in raw_list:
                num += 1
                return_list.append(
                    (('number', num), ('name', _fct))
                )
            return return_list

        def dict_type(raw_list):
            return [fct.items() for fct in raw_list]

        def function_type(raw_list):
            def attr_check(obj):
                attr_test = [isinstance(obj, basestring), isinstance(obj, int)]
                if not any(attr_test):
                    return False
                else:
                    return True

            return_list = []
            for _fct in raw_list:
                items = _fct.__dict__.items()
                return_list.append(
                    [(key, value) for key, value in items
                     if attr_check(obj=value)]
                )
            return return_list

        function = getattr(self.conn, action)
        run = function()
        if run:
            if isinstance(run[0], str):
                return string_type(raw_list=run)
            elif isinstance(run[0], dict):
                return dict_type(raw_list=run)
            else:
                return function_type(raw_list=run)

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
