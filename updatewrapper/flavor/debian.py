from ansible.module_utils._text import to_bytes

from updatewrapper.flavor import FlavorBase


class Debian(FlavorBase):
    def update_cache(self):
        return self.host.run('apt-get update')

    def check_update(self):
        return self.host.run('apt-get --show-upgraded --assume-no upgrade')

    def has_update(self, returncode, stdout, stderr):
        return to_bytes('The following packages will be upgraded') in stdout

    def perform_update(self):
        return self.host.run('apt-get --show-upgraded --assume-yes upgrade')
