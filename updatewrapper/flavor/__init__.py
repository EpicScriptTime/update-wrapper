import abc
import importlib

from updatewrapper.utils.file import bytes_to_text


def detect_flavor(host):
    returncode, stdout, stderr = host.run('if [ -f /etc/debian_version ]; then echo -n "debian"; elif [ -f /etc/redhat-release ]; then echo -n "redhat"; fi')

    return bytes_to_text(stdout).strip()


def get_flavor_wrapper(host, dist_upgrade):
    flavor = host.flavor if host.flavor in ['debian', 'redhat'] else None

    if flavor is None:
        raise ValueError('Invalid flavor')

    Wrapper = getattr(importlib.import_module('updatewrapper.flavor.' + flavor), flavor.capitalize())

    return Wrapper(host, dist_upgrade=dist_upgrade)


class FlavorBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self, host, **kwargs):
        self.host = host

    @abc.abstractmethod
    def update_cache(self):
        pass

    @abc.abstractmethod
    def check_update(self):
        pass

    @abc.abstractmethod
    def has_update(self, returncode, stdout, stderr):
        pass

    @abc.abstractmethod
    def perform_update(self):
        pass

