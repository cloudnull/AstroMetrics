# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

"""All commands are represented as the following hashes.

:param LISTMTD: List methods and options.
:param SHOWMTD: Show methods and options
:param INSTANCEMTD: Instance Methods and options
"""

LISTMTD = {
    'availability-zones': {
        'cmd': 'ex_list_availability_zones',
        'opt': None
    },
    'images': {
        'cmd': 'list_images',
        'opt': None
    },
    'key-pairs': {
        'cmd': 'ex_list_keypairs',
        'pop_keys': ['public_key'],
        'opt': None
    },
    'locations': {
        'cmd': 'list_locations',
        'opt': None
    },
    'networks': {
        'cmd': 'ex_list_networks',
        'opt': None
    },
    'providers': {
        'cmd': 'list_providers',
        'opt': None
    },
    'instances': {
        'cmd': 'list_nodes',
        'opt': None
    },
    'security-groups': {
        'cmd': 'ex_list_security_groups',
        'opt': None
    },
    'sizes': {
        'cmd': 'list_sizes',
        'opt': None
    },
    'volumes': {
        'cmd': 'list_volumes',
        'opt': None
    },
    'volume-snapshots': {
        'cmd': 'list_volume_snapshots',
        'opt': {
            '--vol': {
                'required': True,
                'help': 'List snapshots by Volume ID',
                'default': None
            }
        }
    }
}

SHOWMTD = {
    'availability-zone': {
        'cmd': 'ex_list_availability_zones',
        'opt': None
    },
    'image': {
        'cmd': 'list_images',
        'opt': None
    },
    'location': {
        'cmd': 'list_locations',
        'opt': {
            '--id': {
                'required': True,
                'help': 'Location ID',
                'default': None
            }
        }
    },
    'instance': {
        'cmd': 'list_nodes',
        'opt': {
            '--id': {
                'required': True,
                'help': 'Instance ID',
                'default': None
            }
        }
    },
    'security-group': {
        'cmd': 'ex_list_security_groups',
        'opt': {
            '--id': {
                'required': False,
                'help': 'Security group name',
                'default': None
            },
            '--name': {
                'required': False,
                'help': 'Security group id',
                'default': None
            }
        }
    },
    'size': {
        'cmd': 'list_sizes',
        'opt': {
            '--id': {
                'required': False,
                'help': 'Show Size information',
                'default': None
            }
        }
    },
    'volume': {
        'cmd': 'list_volumes',
        'opt': {
            '--id': {
                'required': False,
                'help': 'Show volume information',
                'default': None
            }
        }
    }
}

INSTANCEMTD = {
    'create': {
        'cmd': 'create_node',
        'opt': None
    },
    'reboot': {
        'cmd': 'reboot_node',
        'opt': None
    },
    'destroy': {
        'cmd': 'destroy_node',
        'opt': None
    }
}
