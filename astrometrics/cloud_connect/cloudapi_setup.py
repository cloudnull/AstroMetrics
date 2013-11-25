# =============================================================================
# Copyright [2013] [kevin]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import logging

import libcloud.compute.providers as providers
from libcloud import security

import astrometrics as ions
import astrometrics.gen_utils as utils


LOG = logging.getLogger('cloud-setup')


def cloud_keys(args):
    """Figure out the Authentication Key Type.

    :param args:
    """

    if args.get('password'):
        user_key = args.get('password')
        key_type = 'password'
    elif args.get('apikey'):
        user_key = args.get('apikey')
        key_type = 'api_key'
    else:
        raise ions.SystemError('No Password/Key provided in Command')
    return user_key, key_type


def api_conn(args):
    """Authenticates a user with the Cloud System .

    :param args:

    If authentication is successful, then the system will allow the user
    to deploy through the application to the types.Provider.
    """

    security.CA_CERTS_PATH.append('dist/cacert.pem')

    user_key, key_type = cloud_keys(args)
    _provider = args.get('provider', 'dummy')

    if _provider in providers.DRIVERS:
        driver = providers.get_driver(args.get('provider'))
    else:
        raise ions.SystemError('No Provider Type Found.')

    try:
        if _provider.upper() in ['RACKSPACE', 'OPENSTACK']:
            region = args.get('region', 'RegionOne').lower()

            if key_type is 'api_key':
                auth_type = '2.0_apikey'
            else:
                auth_type = '2.0_password'

            specs = {'ex_force_auth_url': args.get('authurl'),
                     'ex_force_auth_version': auth_type,
                     'ex_tenant_name': args.get('tenant')}

            if _provider.upper() == 'RACKSPACE':
                if region == 'regionone':
                    raise ions.SystemError('No Region Specified')
                else:
                    specs.update({'ex_force_service_region': region,
                                  'datacenter': region,
                                  'region': region})
        else:
            specs = {'ex_force_auth_url': args.get('authurl'),
                     'ex_force_auth_version': args.get('api_version')}

    except Exception as exp:
        LOG.info(exp)
        raise ions.SystemError('System has halted on specified Request.\n'
                               'ERROR: %s' % exp)
    else:
        specs = utils.parse_dictionary(dictionary=specs)
        LOG.info(specs)
        LOG.debug(specs)
        return driver(
            args.get('username'), user_key, **specs
        )
