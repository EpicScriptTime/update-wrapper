from ansible.module_utils._text import to_bytes


class Wrapper:
    def __init__(self, host):
        self.host = host
        self.flavor = host.flavor if host.flavor in ['debian', 'redhat'] else None

        if self.flavor is None:
            raise ValueError('Invalid flavor')

    def is_debian(self):
        return self.flavor == 'debian'

    def is_redhat(self):
        return self.flavor == 'redhat'

    def update_cache(self):
        if self.is_debian():
            return self.host.run('apt-get update')
        elif self.is_redhat():
            return self.host.run('yum clean expire-cache')

    def check_update(self):
        if self.is_debian():
            return self.host.run('apt-get --show-upgraded --assume-no upgrade')
        elif self.is_redhat():
            return self.host.run('yum check-update')

    def has_update(self, returncode, stdout, stderr):
        if self.is_debian():
            return to_bytes('The following packages will be upgraded') in stdout
        elif self.is_redhat():
            return returncode == 100

    def perform_update(self):
        if self.is_debian():
            return self.host.run('apt-get --show-upgraded --assume-yes upgrade')
        elif self.is_redhat():
            return self.host.run('yum --assumeyes update')
