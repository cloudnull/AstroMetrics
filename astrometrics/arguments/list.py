# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


def list_args(subparser):
    """Set the arguments being used when beginning the attack.

    :param subparser: adds arguments to the begin method.
    """

    lister = subparser.add_parser('list',
                                  help='Listing information from the Cloud'
                                       ' Provider')
    lister.set_defaults(list=True)
    lister.add_argument('--filter',
                        metavar='[NAME]',
                        default=[],
                        action='append',
                        help='Filter Lists by key words')

    group = lister.add_mutually_exclusive_group()
    group.add_argument('--availability-zones',
                       action='store_true',
                       default=None,
                       help='List all available availability zones')
    group.add_argument('--images',
                       action='store_true',
                       default=None,
                       help='List all available Images')
    group.add_argument('--key-pairs',
                       action='store_true',
                       default=None,
                       help='List all available key pairs')
    group.add_argument('--locations',
                       action='store_true',
                       default=None,
                       help='List all available Locations')
    group.add_argument('--instances',
                       action='store_true',
                       default=None,
                       help='List all available instances')
    group.add_argument('--providers',
                       action='store_true',
                       default=None,
                       help='List all available Providers')
    group.add_argument('--security-groups',
                       action='store_true',
                       default=None,
                       help='List all available security groups')
    group.add_argument('--sizes',
                       action='store_true',
                       default=None,
                       help='List all available Sizes')
    group.add_argument('--volumes',
                       action='store_true',
                       default=None,
                       help='List all available volumes')


def show_args(subparser):
    """Set the arguments being used when beginning the attack.

    :param subparser: adds arguments to the begin method.
    """

    show = subparser.add_parser('show',
                                help='Show information from the Cloud'
                                     ' Provider on a resource')
    show.set_defaults(show=True)

    group = show.add_mutually_exclusive_group()
    group.add_argument('--availability-zones',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on an availability zone')
    group.add_argument('--image',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on an Image')
    group.add_argument('--location',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on a Location')
    group.add_argument('--instance',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on an instance')
    group.add_argument('--security-group',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on a security group')
    group.add_argument('--size',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on a Size')
    group.add_argument('--volume',
                       metavar='[ID_NUM]',
                       default=None,
                       help='Show information on a volume')
