# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import prettytable


def print_horiz_table(data):
    """Print a horizontal pretty table from data."""

    base_data = [dict(d) for d in data]
    all_keys = []

    for keys in base_data:
        for key in keys.keys():
            if key not in all_keys:
                all_keys.append(key)

    for data in base_data:
        for key in all_keys:
            if key not in data.keys():
                data[key] = None

    table = prettytable.PrettyTable(all_keys)
    for info in base_data:
        table.add_row(info.values())
    for tbl in table.align.keys():
        table.align[tbl] = 'l'
    print(table)


def print_virt_table(data):
    """Print a virtical pretty table from data."""

    table = prettytable.PrettyTable()
    table.add_column('Keys', data.keys())
    table.add_column('Values', data.values())
    for tbl in table.align.keys():
        table.align[tbl] = 'l'
    print(table)


def parse_dictionary(dictionary):
    """Parse all keys in a dictionary for Values that are None.

    :param default_args: all parsed arguments
    :returns dict: all arguments which are not None.
    """

    return dict([(key, value) for key, value in dictionary.iteritems()
                 if value is not None])


def list_pop(data, pat):
    """Remove an index from a list and return the list.

    :param data: list
    :param pat: pattern to index and pop
    """

    index = data.index(pat)
    return data.pop(index)


def ret_ipv4(data):
    """Validate and return IPv4 addresses."""

    for ipa in data:
        for octet in ipa.strip().split('.'):
            if not octet.isdigit():
                list_pop(data=data, pat=ipa)
            else:
                if not int(octet) < 256:
                    list_pop(data=data, pat=ipa)
    return data