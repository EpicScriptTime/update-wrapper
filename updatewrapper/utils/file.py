import datetime
import os
import yaml

from ansible.module_utils._text import to_text

from updatewrapper.host import Host


CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.update-wrapper.yml')


def convert_console_output(string):
    before = string.split('\n')
    after = []

    for line in before:
        while True:
            # after removing CR, we may end up with an empty line
            if not line:
                break

            # if a CR is found at the end of the line, strip it
            if line.endswith('\r'):
                line = line.rstrip('\r')
                continue  # they may be more than one CR, so we start over again

            # while we're at it, strip all trailing whitespace
            line = line.rstrip()

            # find the position of the character after the last CR
            pos = line.rfind('\r') + 1

            # if a CR was found, slice the string
            if pos > 0:
                line = line[pos:]

            # all clear, we can keep the line
            after.append(line)

            break

    return '\n'.join(after)


def get_config_file():
    return CONFIG_FILE


def get_current_date():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_hosts(file):
    hosts = []

    with open(file) as stream:
        cfg = yaml.load(stream)

    if 'hosts' in cfg and isinstance(cfg['hosts'], dict):
        for name, data in cfg['hosts'].items():
            data['name'] = name

            host = Host(**data)
            hosts.append(host)

    return hosts


def get_logfile(name, path):
    return os.path.join(path, '{0}-update-{1}.log'.format(name, get_current_date()))


def save_output(file, data):
    encoding_errors = 'surrogate_then_replace'

    if isinstance(data, bytes):
        output = to_text(data, errors=encoding_errors)
    elif not isinstance(data, str):
        output = to_text(b''.join(data.readlines()), errors=encoding_errors)
    else:
        output = data

    output = convert_console_output(output)

    with open(file, 'a') as stream:
        stream.write(output)
