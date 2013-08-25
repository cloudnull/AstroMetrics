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
    node.add_argument('--image',
                      default=None,
                      metavar="[ID_NUMBER]",
                      help='Image ID')
    node.add_argument('--name',
                      default=None,
                      metavar="[NAME]",
                      help='Name Convention')
    node.add_argument('--size',
                      default=None,
                      metavar="[ID_NUMBER]",
                      help='Size ID')
    node.add_argument('--cloud-networks',
                      default=None,
                      metavar="[ID_NUM]",
                      help='Attach an Instance to a Cloud Network')
    node.add_argument('--inject-file',
                      default=[],
                      action='append',
                      metavar="[local-file:remote-location]",
                      help='Inject a file on Boot')
    node.add_argument('--userdata',
                      default=None,
                      metavar="[Local-File]",
                      help='Run Local File on Node Boot')

    group = node.add_mutually_exclusive_group()
    group.add_argument('--create-node',
                       action='store_true',
                       default=None,
                       help='Create a Node.')

    # group.add_argument('--reboot-node',
    #                    default=None,
    #                    help='Reboot Node.')
    # group.add_argument('--destroy-node',
    #                    default=None,
    #                    help='Destroy a Node.')
    # group.add_argument('--deploy-node',
    #                    default=None,
    #                    help='Deploy a Node.')
