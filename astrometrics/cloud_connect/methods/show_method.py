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
    """A class collection of all show methods."""

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args
        self.method = None

    def start(self):
        """Run the show method."""

        method = self.args.get('method')
        method = ''.join(method.split('show-'))

        self.method = hashes.SHOWMTD.get(method)
        utils.print_virt_table(
            data=self.show_parser(
                data=self.magic(
                    action=self.method['cmd']
                )
            )
        )

    def show_parser(self, data):
        """Parse and return Data into more usable Data."""

        show_data = data[0]
        print show_data
        if 'pop_keys' in self.method:
            for keys in self.method['pop_keys']:
                show_data.pop(keys)

        if 'extra' in show_data:
            _extra = show_data.pop('extra')
            show_data.update(_extra)
            if 'metadata' in show_data:
                _metadata = show_data.pop('metadata')
                show_data.update(_metadata)

        if 'public_ips' in show_data:
            show_data['public_ips'] = ', '.join(show_data.get('public_ips'))

        if 'private_ips' in show_data:
            show_data['private_ips'] = ', '.join(show_data.get('private_ips'))

        if 'rules' in show_data:
            rules = show_data.pop('rules')
            for sec_rules in rules:
                rules_dict = sec_rules.__dict__
                rule_id = sec_rules.id
                new_rules = dict(('%s_ruleId_%s' % (key, rule_id), value)
                                 for key, value in rules_dict.items()
                                 if not key.startswith('driver'))
                show_data.update(new_rules)

        if 'driver' in show_data:
            show_data.pop('driver')

        LOG.debug(show_data)
        return utils.parse_dictionary(dictionary=show_data)

    def magic(self, action):
        """Return data on an image."""

        def string_type(raw_list, num=0):
            return_list = []
            for fct in raw_list:
                num += 1
                if fct == self.args.get('id'):
                    return_list.append(
                        {'number': num, 'name': fct}
                    )
            return return_list

        def dict_type(raw_list):
            return [fct for fct in raw_list
                    if 'id' in fct and fct['id'] == self.args.get('id')]

        def function_type(raw_list):
            def attr_check(obj):
                attr_test = [isinstance(obj, basestring), isinstance(obj, int)]
                if not any(attr_test):
                    return False
                else:
                    return True

            return_list = [_fct.__dict__ for _fct in raw_list
                           if _fct.__dict__['id'] == self.args.get('id')]
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
