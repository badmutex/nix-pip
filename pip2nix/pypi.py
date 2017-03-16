from __future__ import print_function

from pip2nix.nixshell import NixShell

from collections import defaultdict
from contextlib import contextmanager
import hashlib
import json
import logging
import os.path
from pipes import quote
import re
import shutil
from subprocess import check_output, check_call
import sys
import tempfile

from munch import munchify
import networkx as nx
import requests
from traits.api import HasTraits, Dict, Str, Enum, Set, This, Trait, Long, ListUnicode, This

import pkg_resources
python_bare = pkg_resources.resource_filename(__name__, 'data/python-bare.nix')

logger = logging.getLogger(__name__)


@contextmanager
def tmpdir():
    d = tempfile.mkdtemp()
    try:
        yield d
    finally:
        shutil.rmtree(d)


@contextmanager
def tmpfile():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        yield path
    finally:
        os.unlink(path)


@contextmanager
def tmpvenv(python='python', venvdir=None, extraPackages=None):

    with tmpdir() as venvdir:
        shell = NixShell(python_bare, packages=extraPackages)
        shell.command(['virtualenv', venvdir])
        pip = os.path.join(venvdir, 'bin', 'pip')
        yield (shell, venvdir, pip)


def is_wheel(filename):
    return filename.endswith('.whl')


def is_archive(filename):
    return filename.endswith('.tar.gz')


def is_universal_wheel(filename):
    name, ext = os.path.splitext(filename)

    if not ext == '.whl':
        return False

    _, python, abi, platform = name.rsplit('-', 3)
    truth = abi == 'none' and platform == 'any'

    logger.debug('Is universal wheel? %s: %s', filename, truth)
    return truth


def select_release(releases):
    groups = defaultdict(list)
    for r in releases:
        groups[r.packagetype].append(r)

    if groups['universal']:
        result = groups['universal']
    elif groups['source']:
        result = groups['source']
    elif groups['binary']:
        raise NotImplementedError('Binary distributions are not supported')
    else:
        raise NotImplementedError('Unknown')

    python_version = 'py{}'.format(sys.version_info.major)

    for release in result:
        if python_version in release.python_version:
            return release

    raise NotImplementedError('Unable to find release for {} in {}'.format(python_version, result))



def empty_venv_packages():
    logger.info('Determining preinstalled packages in a virtualenv')
    with tmpvenv() as (shell, venvdir, pip):
        frozen = freeze([])
        pkgs = set([p.name for p in frozen])
        return pkgs


class FrozenRequirementsSet(object):

    _reqs = Set()
    _preinstalled = Set()

    def __init__(self, frozen_set, preinstalled=None):

        self._reqs = dict([req.name])
        self._preinstalled = preinstalled or set()

        logger.info('Loading requirements from %s', requirements_file)
        with open(requirements_file) as fd:
            reqs = map(lambda s: s.strip().split('=='), fd)
            reqs = [{'name': n, 'version': v} for n, v in reqs]
            reqs = map(dotdict, reqs)
            for req in reqs:
                if req.name in self.preinstalled:
                    continue
                entry = PackageEntry.from_pip_list_json(req)
                entry.requirements = self
                self._reqs[entry.name] = entry
                logger.info('Requires: %s', entry)



    def __iter__(self):
        for k in sorted(self._reqs):
            yield self._reqs[k]

    def __getitem__(self, name):
        return self._reqs[name]

    def names(self):
        return sorted(self._reqs.iterkeys())

    def verify_dependencies(self):
        logger.info('Verifying dependencies')
        for entry in self:
            entry.pip_download()

    def build(self):
        logger.info('Building')
        with tmp_venv(python=self.python) as (venv, pip), tempdir() as cache:
            for entry in self:
                entry.download(preinstalled=self.preinstalled, cache=cache)
                entry.install(preinstalled=self.preinstalled, venv=venv, cache=cache)

    def graph(self):
        logger.info('Building networkx graph')
        G = nx.DiGraph()
        for entry in self:
            entry.graph(G)
        return G


class Package(HasTraits):

    name = Str
    version = Str
    dependencies = Set(This)
    preinstalled = Set(Str)
    buildInputs = Set(Str)
    sha256 = Str(minlength=64, maxlength=64)  # 64 is the length of the sha256 hexdigest

    def __eq__(self, other):
        return \
            self.name == other.name and\
            self.version == other.version

    def __str__(self):
        return '{}=={}'.format(self.name, self.version)

    @property
    def frozen_name(self):
        return str(self)

    def find_requirements(self):
        logger.info('Finding requirements for %s', self)

        frozen = freeze([self.frozen_name],
                        preinstalled=self.preinstalled,
                        extraPackages=self.buildInputs)

        for entry in frozen:
            if entry.name == self.name:
                continue

            pkg = Package(name=entry.name, version=entry.version,
                          preinstalled=self.preinstalled,
                          buildInputs=self.buildInputs)

            self.dependencies.add(pkg)


    def prune_dependencies(self):
        logger.info('Prunning dependencies for %s', self)

        dep_names = set([dep.name for dep in self.dependencies])  # :: {str}
        to_prune  = set()                                         # :: {str}

        logger.debug('%s children: %s', self.name, ' '.join(dep_names))

        for child in self.dependencies:
            child.find_requirements()
            logger.debug('%s grandchildren: %s', self.name, 
                        ' '.join(map(lambda p: p.name, child.dependencies)))

            for grandchild in child.dependencies:
                if grandchild.name in dep_names:
                    to_prune.add(grandchild.name)

        logger.debug('Prunning for %s: %s', self, ' '.join(to_prune))
        pruned = filter(lambda dep: dep.name not in to_prune, self.dependencies)
        self.dependencies = set(pruned)



def freeze(packages, preinstalled=None, extraPackages=None):
    preinstalled = preinstalled or set()

    logger.debug('Freezing packages: %s', ', '.join(packages))
    with tmpvenv(extraPackages=extraPackages) as (shell, venvdir, pip):
        if packages:
            shell([pip, 'install'] + map(quote, packages))

        frozen = shell([pip, 'list', '--format', 'json'])
        frozen_json = json.loads(frozen.strip())
        munched = filter(
            lambda pkg: pkg.name not in preinstalled,
            munchify(frozen_json))
        return munched


def build_graph(open_packages, extraPackages=None):

    preinstalled = empty_venv_packages()
    logger.info('Preinstalled packages: %s', ', '.join(preinstalled))

    frozen = freeze(open_packages, preinstalled=preinstalled)

    packages = [Package(name=p.name, version=p.version,
                        preinstalled=preinstalled, buildInputs=extraPackages)
                for p in frozen]
    logger.info('Processing %s', ' '.join(map(str, packages)))

    for pkg in packages:
        pkg.find_requirements()

    for pkg in packages:
        pkg.prune_dependencies()


    G = nx.DiGraph()
    for pkg in packages:
        G.add_node(pkg.name)

        for dep in pkg.dependencies:
            G.add_edge(pkg.name, dep.name)

    dotfile = '/tmp/test.dot'
    graphviz_type = 'pdf'
    nx.nx_agraph.write_dot(G, dotfile)
    cmd = ['dot', '-Grankdir=LR', '-T%s' % graphviz_type, dotfile]
    data = check_output(cmd)
    with open('/tmp/test.%s' % graphviz_type, 'wb') as fd:
        fd.write(data)



if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    # build_graph(['azure'])
    # build_graph(['shade'], extraPackages=set(['openssl']))
    build_graph(['cloudmesh_client'], extraPackages=set(['openssl libffi']))
