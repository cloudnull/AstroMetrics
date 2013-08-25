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


def auth_args(parser):
    """Set the arguments being used when for authentication."""

    authgroup = parser.add_argument_group('Authentication',
                                          ' Authentication against'
                                          ' the Cloud API')
    # Base Authentication Argument Set
    authgroup.add_argument('-u',
                           '--cloud-user',
                           metavar='[USERNAME]',
                           help='Defaults to env[CLOUD_USERNAME]',
                           default=os.environ.get('CLOUD_USERNAME', None))
    authgroup.add_argument('-t',
                           '--cloud-tenant',
                           metavar='[USERNAME]',
                           help='Defaults to env[CLOUD_TENANT]',
                           default=os.environ.get('CLOUD_TENANT', None))
    authgroup.add_argument('-a',
                           '--cloud-apikey',
                           metavar='[APIKEY]',
                           help='Defaults to env[CLOUD_APIKEY]',
                           default=os.environ.get('CLOUD_APIKEY', None))
    authgroup.add_argument('-p',
                           '--cloud-password',
                           metavar='[PASSWORD]',
                           help='Defaults to env[CLOUD_PASSWORD]',
                           default=os.environ.get('CLOUD_PASSWORD', None))
    authgroup.add_argument('-r',
                           '--cloud-region',
                           metavar='[REGION]',
                           help='Defaults to env[CLOUD_REGION]',
                           default=os.environ.get('CLOUD_REGION', None))
    authgroup.add_argument('--cloud-provider',
                           metavar='[PROVIDER]',
                           help='Defaults to env[CLOUD_PROVIDER]',
                           default=os.environ.get('CLOUD_PROVIDER', None))
    authgroup.add_argument('--cloud-authurl',
                           metavar='[AUTH_URL]',
                           help='Defaults to env[CLOUD_AUTHURL]',
                           default=os.environ.get('CLOUD_AUTHURL', None))
    authgroup.add_argument('--cloud-version',
                           metavar='[VERSION_NUM]',
                           default=os.getenv('CLOUD_VERSION', None),
                           help='env[OS_VERSION]')
