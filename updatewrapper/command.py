from ansible import constants as C
from ansible.compat.six.moves import shlex_quote


def exec_command(host, cmd):
    play_context = host.get_play_context()
    connection = host.get_connection(play_context)

    in_data = None
    sudoable = True
    executable = None

    allow_same_user = C.BECOME_ALLOW_SAME_USER
    same_user = play_context.become_user == play_context.remote_user

    if sudoable and play_context.become and (allow_same_user or not same_user):
        cmd = play_context.make_become_cmd(cmd, executable=executable)

    if connection.allow_executable:
        if executable is None:
            executable = play_context.executable
            # mitigation for SSH race which can drop stdout (https://github.com/ansible/ansible/issues/13876)
            # only applied for the default executable to avoid interfering with the raw action
            cmd = connection._shell.append_command(cmd, 'sleep 0')
        if executable:
            cmd = executable + ' -c ' + shlex_quote(cmd)

    returncode, stdout, stderr = connection.exec_command(cmd, in_data=in_data, sudoable=sudoable)

    print()  # Required for spacing

    return returncode, stdout, stderr
