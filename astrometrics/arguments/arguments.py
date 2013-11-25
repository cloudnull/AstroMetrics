# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import os

from astrometrics import info
import astrometrics.cloud_connect.methods as hashes


def add_arg_method(parser, name, opts, prefix, help_info, add_filter=False):
    action = '%s-%s' % (prefix, name.replace('_', '-'))
    obj = parser.add_parser(action, help=help_info)
    obj.set_defaults(method=action)
    if opts['opt']:
        for key, value in opts['opt'].items():
            obj.add_argument(key,
                             metavar='',
                             required=value['required'],
                             default=value['default'],
                             help=value['help'])

    if add_filter is True:
        obj.add_argument('--filter',
                         metavar='',
                         default=[],
                         action='append',
                         help='Filter Lists by key words')


def list_subargs(subparser):
    """Set the arguments being used when beginning the attack.

    :param subparser: adds arguments to the begin method.
    """

    for key, value in hashes.LISTMTD.items():
        add_arg_method(
            parser=subparser,
            name=key,
            opts=value,
            prefix='list',
            help_info='List all %s' % key,
            add_filter=True
        )


def show_subargs(subparser):
    """Set the arguments being used when beginning the attack.

    :param subparser: adds arguments to the begin method.
    """

    for key, value in hashes.SHOWMTD.items():
        add_arg_method(
            parser=subparser,
            name=key,
            opts=value,
            prefix='show',
            help_info='Show information on a %s' % key,
        )


def node_subargs(subparser):
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


def volume_subargs(subparser):
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


def auth_optargs(parser):
    """Set the arguments being used when for authentication.

    :param parser:
    """

    authgroup = parser.add_argument_group('Authentication',
                                          ' Authentication against'
                                          ' the Cloud API')
    # Base Authentication Argument Set
    authgroup.add_argument('-u',
                           '--username',
                           metavar='',
                           help='Defaults to env[CLOUD_USERNAME]',
                           default=os.environ.get('CLOUD_USERNAME', None))
    authgroup.add_argument('-t',
                           '--tenant',
                           metavar='',
                           help='Defaults to env[CLOUD_TENANT]',
                           default=os.environ.get('CLOUD_TENANT', None))

    exc_group = authgroup.add_mutually_exclusive_group()
    exc_group.add_argument('-a',
                           '--apikey',
                           metavar='',
                           help='Defaults to env[CLOUD_APIKEY]',
                           default=os.environ.get('CLOUD_APIKEY', None))
    exc_group.add_argument('-p',
                           '--password',
                           metavar='',
                           help='Defaults to env[CLOUD_PASSWORD]',
                           default=os.environ.get('CLOUD_PASSWORD', None))
    authgroup.add_argument('-r',
                           '--region',
                           metavar='',
                           help='Defaults to env[CLOUD_REGION]',
                           default=os.environ.get('CLOUD_REGION', None))
    authgroup.add_argument('--provider',
                           metavar='',
                           help='Defaults to env[CLOUD_PROVIDER]',
                           default=os.environ.get('CLOUD_PROVIDER', None))
    authgroup.add_argument('--authurl',
                           metavar='',
                           help='Defaults to env[CLOUD_AUTHURL]',
                           default=os.environ.get('CLOUD_AUTHURL', None))
    authgroup.add_argument('--api-version',
                           metavar='',
                           default=os.getenv('CLOUD_VERSION', None),
                           help='env[CLOUD_VERSION]')


def default_optargs(parser):
    """Add in Default Arguments to the parser.

    :param parser:
    """

    parser.add_argument('--log-level',
                        choices=['warn', 'info', 'error', 'critical', 'debug'],
                        default='info',
                        help='Set the Log Level')
    parser.add_argument('--version',
                        '-V',
                        action='version',
                        version=info.VINFO)


