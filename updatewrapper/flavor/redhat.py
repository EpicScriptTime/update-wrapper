from updatewrapper.flavor import FlavorBase


class Redhat(FlavorBase):
    def update_cache(self):
        return self.host.run('yum clean expire-cache')

    def check_update(self):
        return self.host.run('yum check-update')

    def has_update(self, returncode, stdout, stderr):
        return returncode == 100

    def perform_update(self):
        return self.host.run('yum --assumeyes update')
