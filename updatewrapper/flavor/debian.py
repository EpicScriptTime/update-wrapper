from ansible.module_utils._text import to_bytes

from updatewrapper.flavor import FlavorBase


class Debian(FlavorBase):
    def __init__(self, host, dist_upgrade=False, **kwargs):
        self.command = 'dist-upgrade' if dist_upgrade else 'upgrade'

        super().__init__(host)

    def update_cache(self):
        return self.host.run('DEBIAN_FRONTEND=noninteractive apt-get update')

    def check_update(self):
        return self.host.run('DEBIAN_FRONTEND=noninteractive apt-get --show-upgraded --assume-no ' + self.command)

    def has_update(self, returncode, stdout, stderr):
        return to_bytes('The following packages will be upgraded') in stdout

    def perform_update(self):
        return self.host.run('DEBIAN_FRONTEND=noninteractive apt-get --show-upgraded --assume-yes ' + self.command)
