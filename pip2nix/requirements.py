from traits.api import HasTraits, Trait, List, Str

import package
from util import shelve_open

from itertools import imap

import hashlib
import re

import logging
logger = logging.getLogger(__name__)


class Requirements(HasTraits):

    _requirements = List(Str)
    _digest = Trait(hashlib.sha256())
    _graph = Trait(package.Graph)

    @classmethod
    def from_iter(cls, names):
        pkg_regex = r'^([a-zA-Z0-9=-_.]+)'
        regex = re.compile(pkg_regex)
        logger.debug('Package regex: %s', pkg_regex)

        this = cls()
        for line in imap(str.strip, names):

            # skip emtpy lines
            if not line:
                continue

            # skip -e and other flags, which are not supported
            if line.startswith('-'):
                logger.warn('Skipping unsupported requirement definition: %s', line)
                continue

            m = regex.match(line)
            if not m:
                logger.warn('Skipping unmatched requirement %s', line)
                continue

            pkg = m.group()
            this.add(pkg)

        logger.debug('Created requirements %s', this._requirements)
        return this

    @classmethod
    def from_file(cls, path):
        logger.debug('Loading python requirements from %s', path)
        with open(path) as fd:
            return cls.from_iter(fd)

    @property
    def digest(self):
        return self._digest.hexdigest()

    @property
    def graph(self):
        if not self._graph:
            logger.critical('Requirements `build_graph()` not called. This is a bug')

        return self._graph

    @property
    def packages(self):
        return self.graph.nodes()

    def add(self, name):
        logger.debug('Adding package %s', name)

        if self._graph:
            logger.debug('Clearing precomputed graph due to addition of %s', name)
            self._graph = None

        self._requirements.append(name)
        self._digest.update(name)

    def build_graph(self, buildInputs=None):
        if self._graph:
            logger.debug('Using cached graph')
            return

        logger.debug('No cached graph found, computing it')
        self._graph = package.Graph.from_names(self._requirements, buildInputs=buildInputs)

    def graphviz(self, *args, **kwargs):
        "Call the underlying graph's `graphviz(*args, **kwargs)` method"
        return self.graph.graphviz(*args, **kwargs)

    def merge(self, other):
        logger.debug('Merging requiremnts sets')
        logger.debug('\t%s', self._requirements)
        logger.debug('\t%s', other._requirements)

        new = self.__class__.from_iter(self._requirements)
        for r in other._requirements:
            new.add(r)
        return new

    def persist(self, filename):
        logger.debug('Persisting to %s using %s', filename, self.digest)
        with shelve_open(filename) as shelf:
            shelf[self.digest] = (self._requirements, self._graph)

    def unpersist(self, filename):
        logger.debug('Loading from %s using %s', filename, self.digest)
        with shelve_open(filename) as shelf:
            if self.digest in shelf:
                logger.debug('Using cached values')
                (reqs, graph) = shelf[self.digest]
                self._requirements = reqs
                self._graph = graph
            else:
                logger.debug('No values found in persistent cache')
