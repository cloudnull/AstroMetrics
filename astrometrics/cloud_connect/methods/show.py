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
from astrometrics.cloud_connect.methods import LISTMTD
import astrometrics.utils as utils
from astrometrics.worker import LOG


class show(object):
    """A class collection of all show methods."""

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args

    def start(self):
        """Run the show method."""

        for method in LISTMTD.keys():
            if method in self.args:
                data = self.magic(action=LISTMTD.get(method), arg=method)
                break
        else:
            raise ions.SystemError('No Parse-able Functions were found.')

        utils.print_virt_table(data=self.show_parser(data=data))

    def show_parser(self, data):
        """Parse and return Data into more usable Data."""

        _data = data[0].__dict__
        if 'extra' in _data:
            _extra = _data.pop('extra')
            _data.update(_extra)
            if 'metadata' in _data:
                _metadata = _data.pop('metadata')
                _data.update(_metadata)
        if 'public_ips' in _data:
            _data['public_ips'] = ', '.join(_data.get('public_ips'))
        if 'private_ips' in _data:
            _data['private_ips'] = ', '.join(_data.get('private_ips'))
        if 'rules' in _data:
            rules = _data.pop('rules')
            for sec_rules in rules:
                rules_dict = sec_rules.__dict__
                rule_id = sec_rules.id
                new_rules = dict(('%s_ruleId_%s' % (key, rule_id), value)
                                 for key, value in rules_dict.items()
                                 if not key.startswith('driver'))
                _data.update(new_rules)
        if 'driver' in _data:
            _data.pop('driver')
        LOG.debug(_data)
        return utils.parse_dictionary(dictionary=_data)

    def magic(self, action, arg):
        """Return data on an image."""

        function = getattr(self.conn, action)
        show_act = function()

        if all([isinstance(fct, str) for fct in show_act]):
            return [(('id', type(fct)), ('name', fct)) for fct in show_act
                    if str(self.args.get(arg)) == fct]
        if all([isinstance(fct, dict) for fct in show_act]):
            return [fct.items() for fct in show_act
                    if str(self.args.get(arg)) in fct.values()]
        else:
            data = [_im for _im in show_act
                    if str(_im.id) == str(self.args.get(arg, arg))]
            if not data:
                raise ions.SystemError('%s not found' % arg)
            else:
                return data
