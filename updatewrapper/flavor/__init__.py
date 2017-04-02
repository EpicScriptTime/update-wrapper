import abc
import importlib


def get_flavor_wrapper(host):
    flavor = host.flavor if host.flavor in ['debian', 'redhat'] else None

    if flavor is None:
        raise ValueError('Invalid flavor')

    Wrapper = getattr(importlib.import_module('updatewrapper.flavor.' + flavor), flavor.capitalize())

    return Wrapper(host)


class FlavorBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self, host):
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

