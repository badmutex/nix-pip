from traits.api import HasTraits, File, Instance

import os.path
import shelve

from nixpip.util import default_config_dir

import logging
logger = logging.getLogger(__name__)


class Store(HasTraits):

    path = File
    _shelf = Instance(shelve.Shelf)

    def __init__(self, path=None):

        self.path = path or os.path.join(default_config_dir(), 'store.dat')
        self._shelf = shelve.open(self.path)


    def close(self):
        logger.debug('Closing store %s', self.path)
        self._shelf.close()

    def sync(self):
        self._shelf.sync()

    def get(self, name, version, default=None):
        logger.debug('Getting %s==%s from store', name, version)
        return self._shelf.get('%s==%s' % (name, version), default)

    def set(self, name, version, pkg):
        logger.debug('Adding %s==%s to store', name, version)
        self._shelf['%s==%s' % (name, version)] = pkg
        self.sync()
