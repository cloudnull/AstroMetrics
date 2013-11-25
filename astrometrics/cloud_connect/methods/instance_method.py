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
import astrometrics.cloud_connect.methods as hashes
import astrometrics.cloud_connect.methods.show_method as lookup
import astrometrics.base_utils as utils
import astrometrics.gen_utils as gen_utils
from astrometrics.worker import LOG


class Actions(object):
    """A class collection of all show methods."""

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args

    def start(self):
        for method in hashes.NODEMTD.keys():
            if method in self.args:
                self.magic(action=hashes.NODEMTD.get(method))
                break
        else:
            raise ions.SystemError('No Parse-able Functions were found.')

    def magic(self, action):
        """Return data on an image."""

        function = getattr(self, action)
        function()

    def info_lookup(self, action, arg):
        """Look up Cloud Information."""

        find = lookup.show(conn=self.conn, args=self.args)
        data = find.magic(action=action, arg=arg)
        if len(data) > 1:
            raise ions.SystemError('More than a single return was found when'
                                   ' performing %s lookup.' % action)
        else:
            return data[0]

    def networks(self, specs):
        networks = self.args.get('cloud_networks')
        specs['networks'] = networks.split(',')
        return specs

    def security_groups(self, specs):
        if self.args['cloud_provider'].upper() == 'EC2':
            if self.args.get('security_groups'):
                _sg = self.args.get('security_groups')
                specs['ex_securitygroup'] = _sg
        elif self.args['cloud_provider'].upper() == 'OPENSTACK':
            if self.args.get('security_groups'):
                _sec_groups = self.args.get('security_groups')
                _sgns = ''.join(_sec_groups.split()).split(',')
                try:
                    _asg = self.conn.ex_list_security_groups()
                except Exception as exp:
                    LOG.error(exp)
                    raise ions.SystemError('No Security Groups Available')
                else:
                    specs['ex_security_groups'] = [_sg for _sg in _asg
                                                   if _sg.name in _sgns]
        return specs

    def user_data(self, specs):
        with open(self.args.get('userdata'), 'rb') as user_data:
            specs['ex_userdata'] = user_data.read()
        return specs

    def ssh_access(self, specs):
        """Set an SSH Key for injection in UserData."""

        specs['ex_keyname'] = self.args.get('ssh_keyname')
        specs['ssh_key'] = self.args.get('ssh_keypub')
        specs['ssh_username'] = self.args.get('ssh_username')
        return specs

    def file_injection(self, specs):
        """Path to files that will be used for injection on VM boot."""

        files = self.args.get('inject_files')
        specs['ex_files'] = files
        return specs

    def vm_ssh_deploy(self):
        """Prepare for an SSH deployment Method for any found config."""
        import libcloud.compute.deployment as dep

        def ssh_key_deploy(ssh_key):
            return dep.SSHKeyDeployment(key=ssh_key)

        def script_deploy(script):
            return dep.ScriptDeployment(name=('/tmp/deployment_%s.sh'
                                              % utils.rand_string()),
                                        script=str(script))

        def deployment_type(actions):
            if len(actions) > 1:
                return dep.MultiStepDeployment(actions)
            else:
                return actions[0]

        dep_actions = []
        if self.args.get('ssh_key_pub'):
            with open(self.args.get('ssh_key_pub'), 'rb') as open_key:
                dep_actions.append(
                    ssh_key_deploy(ssh_key=open_key.read())
                )

        if self.args.get('config_script'):
            with open(self.args.get('config_script'), 'rb') as open_script:
                dep_actions.append(
                    script_deploy(script=open_script.read())
                )

        return deployment_type(actions=dep_actions)

    def reboot_instance(self):
        """Reboot a Cloud Instances."""

        instance = self.info_lookup(action='list_instances',
                                    arg=self.args.get('id'))
        self.conn.reboot_instance(instance=instance)

    def destroy_instance(self):
        """Destroy a Cloud Instances."""

        instance = self.info_lookup(action='list_instances',
                                    arg=self.args.get('id'))
        self.conn.destroy_instance(instance=instance)

    def create_instance(self):
        """Build an instance from values in our DB."""

        instance_name = self.args.get('name', utils.rand_string().lower())
        image_id = self.info_lookup(action='list_images',
                                    arg=self.args.get('image'))
        size_id = self.info_lookup(action='list_sizes',
                                   arg=self.args.get('size'))

        specs = {'name': instance_name,
                 'image': image_id,
                 'size': size_id,
                 'max_tries': 15,
                 'timeout': 1200}

        if any(['ssh_keyname' in self.args,
                'ssh_keypub' in self.args,
                'ssh_username' in self.args]):
            self.ssh_access(specs=specs)

        if 'security_group' in self.args:
            self.security_groups(specs=specs)

        if 'userdata' in self.args:
            self.user_data(specs=specs)

        if 'file_injection' in self.args:
            self.file_injection(specs=specs)

        if 'cloud_networks' in self.args:
            self.networks(specs=specs)

        if self.args.get('ssh_deployment') is not None:
            specs['deploy'] = self.vm_ssh_deploy()

        specs = gen_utils.parse_dictionary(dictionary=specs)
        LOG.debug('Here are the specs for the build ==> %s' % specs)
        self.conn.create_instance(**specs)
