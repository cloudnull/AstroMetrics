# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


def node_args(subparser):
    """Set the arguments being used when beginning the attack.

    :param subparser: adds arguments to the begin method.
    """

    volume = subparser.add_parser('volume',
                                  help='Interactions with Cloud Volumes')
    volume.set_defaults(volume=True)

    group = volume.add_mutually_exclusive_group()
    group.add_argument('--create-volume',
                       default=None,
                       metavar="[ID_NUMBER]",
                       help='Create a Volume.')
    group.add_argument('--create-volume-snapshot',
                       default=None,
                       metavar="[ID_NUMBER]",
                       help='Create a Volume Snapshot.')
    group.add_argument('--destroy-volume',
                       default=None,
                       metavar="[ID_NUMBER]",
                       help='Destroy a Volume.')
    group.add_argument('--destroy-volume-snapshot',
                       default=None,
                       metavar="[ID_NUMBER]",
                       help='Destroy a Volume Snapshot.')
    group.add_argument('--detach-volume',
                       default=None,
                       metavar="[ID_NUMBER]",
                       help='Detach a Volume from a Node.')
