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

    node = subparser.add_parser('node',
                                help='Interactions with Cloud Nodes')
    node.set_defaults(node=True)
    node.add_argument('-I', '--image',
                      default=None,
                      metavar="[ID_NUMBER]",
                      help='Image ID')
    node.add_argument('-N', '--name',
                      default=None,
                      metavar="[NAME]",
                      help='Name Convention')
    node.add_argument('-S', '--size',
                      default=None,
                      metavar="[ID_NUMBER]",
                      help='Size ID')
    node.add_argument('-CN', '--cloud-networks',
                      default=None,
                      metavar="[ID_NUM]",
                      help='Attach an Instance to a Cloud Network')
    node.add_argument('-IF', '--inject-file',
                      default=[],
                      action='append',
                      metavar="[local-file:remote-location]",
                      help='Inject a file on Boot')
    node.add_argument('-U', '--userdata',
                      default=None,
                      metavar="[Local-File]",
                      help='Run Local File on Node Boot')
    node.add_argument('-T', '--id',
                      default=None,
                      metavar="[ID_NUMBER]",
                      help='Specify a Node ID')

    group = node.add_mutually_exclusive_group()
    group.add_argument('--create',
                       action='store_true',
                       default=None,
                       help='Create a Node.')
    group.add_argument('--reboot',
                       action='store_true',
                       default=None,
                       help='Reboot Node.')
    group.add_argument('--destroy',
                       action='store_true',
                       default=None,
                       help='Destroy a Node.')

    # group.add_argument('--deploy-node',
    #                    default=None,
    #                    help='Deploy a Node.')
