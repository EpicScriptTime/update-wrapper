import getpass

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_bytes
from ansible.playbook.play_context import PlayContext
from ansible.plugins import PluginLoader

from updatewrapper.command import exec_command

connection_loader = PluginLoader(
    'Connection',
    'updatewrapper.connection.ssh',
    C.DEFAULT_CONNECTION_PLUGIN_PATH,
    'connection_plugins',
    aliases={'paramiko': 'paramiko_ssh'},
    required_base_class='ConnectionBase',
)


class Host:
    def __init__(self, name='localhost', addr='localhost', port='22', user='root', sudo=False, sudo_pass=False, flavor='debian'):
        self.name = addr if name is 'localhost' else name
        self.addr = name if addr is 'localhost' else addr
        self.port = port
        self.user = user
        self.sudo = sudo or sudo_pass
        self.sudo_pass = sudo_pass
        self.flavor = flavor

        self._passwords = None

    def run(self, cmd):
        return exec_command(self, cmd)

    def ask_passwords(self):
        if self.sudo_pass:
            (sshpass, becomepass) = self._ask_passwords()
            self._passwords = {'conn_pass': sshpass, 'become_pass': becomepass}
            print()

    @staticmethod
    def _ask_passwords():
        sshpass = None
        becomepass = None

        try:
            becomepass = getpass.getpass(prompt='SUDO password: ')
            if becomepass:
                becomepass = to_bytes(becomepass)
        except EOFError:
            pass

        return sshpass, becomepass

    def get_play_context(self):
        play_context = PlayContext(play=None, options=None, passwords=self._passwords)

        play_context.remote_addr = self.addr
        play_context.port = self.port
        play_context.remote_user = self.user

        play_context.ssh_executable = 'ssh'
        play_context.timeout = 10
        play_context.connection = 'ssh'

        play_context.become = self.sudo
        play_context.become_method = 'sudo'
        play_context.become_user = 'root'

        return play_context

    @staticmethod
    def get_connection(play_context):
        conn_type = play_context.connection
        new_stdin = None

        connection = connection_loader.get(conn_type, play_context, new_stdin)

        if not connection:
            raise AnsibleError("the connection plugin '%s' was not found" % conn_type)

        return connection
