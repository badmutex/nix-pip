from __future__ import print_function

import hashlib
import json
import logging
import os.path
from collections import defaultdict
from pipes import quote
from subprocess import check_output

from munch import munchify
import networkx as nx
from traits.api import HasTraits, Trait, Dict, List, Str, Set, This, Bool

from nixpip.util import concat, tmpvenv
from nixpip.store import Store


logger = logging.getLogger(__name__)


# Some have odd version strings which are consistently inconsistently
# reported by pip and pypi.
#
# Notable example is functools32:
#
# - pip freeze reports version as 3.2.3.post2
# - pypi reports version as 3.2.3-2
# - git repository reports tag consistently with pypi (3.2.3-2)
# - one can install functools32 as functools32==3.2.3-2 OR functools32==3.2.3.post2
#
# Since we depend on pypi reporting for later pinning we apply the
# following transformations to the versions reported by pip list/freeze.
#
# - the key is the string in the reported version
# - the value is the replacement
VERSION_TRANSFORMS = {
    '.post': '-'
}


CACHE = dict()                  # package name -> package


def is_cached(pkg):
    global CACHE
    return pkg.name in CACHE


def cache(pkg):
    assert not is_cached(pkg)
    global CACHE
    CACHE[pkg.name] = pkg


def clear_cache():
    global CACHE
    CACHE.clear()


def empty_venv_packages():
    logger.info('Determining preinstalled packages in a virtualenv')
    pkgs = dict()
    with tmpvenv() as (shell, venvdir, pip):
        frozen = freeze([])
        for p in frozen:
            pkgs[p.name] = Package(name=p.name, version=p.version)
        return pkgs



class Package(HasTraits):

    name = Str
    version = Str
    dependencies = Set(This)
    preinstalled = Dict(Str, This)
    buildInputs = Dict(Str, List(Str))
    available = Dict(Str, This)  # :: name -> Package
    frozen = Bool(False)

    def __eq__(self, other):
        return \
            self.name == other.name and\
            self.version == other.version

    def __str__(self):
        return '{}=={}'.format(self.name, self.version)

    @property
    def frozen_name(self):
        return str(self)

    def apply_version_transformations(self, transformations=None):
        tx = transformations or VERSION_TRANSFORMS
        logger.debug('%s applying version transformations %s',
                    self, tx)

        if self.frozen:
            logger.debug('Using stored %s', self)
            return

        ver = self.version
        for old, new in tx.items():
            ver = ver.replace(old, new)

        logger.debug('%s updating version to %s', self.name, ver)
        self.version = ver

        for dep in self.dependencies:
            dep.apply_version_transformations(transformations=tx)

    def find_requirements(self):
        logger.debug('Finding requirements for %s', self)

        if self.frozen:
            logger.debug('Using stored %s', self)
            return

        if is_cached(self):
            logger.debug('Using cached %s', self)
            return

        frozen = freeze([self.frozen_name],
                        preinstalled=self.preinstalled.keys(),
                        buildInputs=self.buildInputs.get(self.name))

        for entry in frozen:
            if entry.name == self.name:
                continue

            pkg = self.available[entry.name]
            self.dependencies.add(pkg)

        logger.debug('\t%s', map(str, sorted(list(self.dependencies))))


    def prune_dependencies(self):
        logger.debug('Prunning dependencies for %s', self)

        if self.frozen:
            logger.debug('Using stored %s', self)
            return

        dep_names = set([dep.name for dep in self.dependencies])  # :: {str}
        to_prune  = set()                                         # :: {str}

        logger.debug('%s children: %s', self.name, ' '.join(dep_names))

        for child in self.dependencies:

            if not is_cached(child):

                child.find_requirements()
                logger.debug('%s grandchildren: %s', self.name, 
                            ' '.join(map(lambda p: p.name, child.dependencies)))

                cache(child)

            else:

                logger.debug('Using cached %s', child)

            for grandchild in child.dependencies:
                if grandchild.name in dep_names:
                    to_prune.add(grandchild.name)

        logger.debug('Prunning for %s: %s', self, ' '.join(to_prune))
        pruned = filter(lambda dep: dep.name not in to_prune, self.dependencies)
        self.dependencies = set(pruned)

    def freeze(self, store):
        self.frozen = True
        store.set(self.name, self.version, self)



def _decode_ascii(obj):

    def as_ascii(x):
        if isinstance(x, unicode):
            return x.encode('ascii')
        else:
            return x

    for k in obj.keys():
        v = obj.pop(k)
        k = as_ascii(k)
        v = as_ascii(v)

        obj[k] = v

    return obj


def freeze(packages, preinstalled=None, buildInputs=None):
    preinstalled = preinstalled or set()
    buildInputs = buildInputs or list()

    logger.debug('Freezing packages: %s with %s', ', '.join(packages), ', '.join(buildInputs))
    with tmpvenv(buildInputs=buildInputs) as (shell, venvdir, pip):
        if packages:
            shell([pip, 'install'] + map(quote, packages))

        frozen = shell([pip, 'list', '--format', 'json'])
        frozen_json = json.loads(frozen.strip(), object_hook=_decode_ascii)
        for pkg in frozen_json:
            pkg['name'] = pkg['name'].lower()
        munched = filter(
            lambda pkg: pkg.name not in preinstalled,
            munchify(frozen_json))
        return munched


class Graph(HasTraits):

    digraph = Trait(nx.DiGraph)
    sha256 = Str(minlength=64, maxlength=64)

    def __getattr__(self, name):
        return getattr(self.digraph, name)

    @classmethod
    def from_names(cls, names, buildInputs=None, store=None):
        store = store or Store()
        names = sorted(set(names))
        buildInputs = buildInputs or defaultdict(list)

        logger.info('Building dependencygraph for %s with buildInputs %s',
                    ' '.join(names), buildInputs)

        preinstalled = empty_venv_packages()
        logger.info('Preinstalled packages: %s', ', '.join(preinstalled))

        frozen = freeze(names, preinstalled=preinstalled, buildInputs=concat(buildInputs.values()))

        packages = []
        for p in frozen:
            pkg = store.get(p.name, p.version) or \
                  Package(name=p.name, version=p.version,
                          preinstalled=preinstalled,
                          buildInputs=buildInputs)
            packages.append(pkg)

        for p in packages:
            p.available = dict((p.name, p) for p in packages)
        logger.info('Processing %s', ' '.join(map(str, packages)))

        logger.info('Finding requirements')
        for pkg in packages:
            logger.info('\t%s', pkg.name)
            pkg.find_requirements()

        clear_cache()

        logger.info('Computing transitive dependencies')
        for pkg in packages:
            logger.info('\t%s', pkg.name)
            pkg.prune_dependencies()

        logger.info('Applying version transformations')
        for pkg in packages:
            logger.info('\t%s', pkg.name)
            pkg.apply_version_transformations()

        logger.info('Saving packages to store')
        for pkg in packages:
            logger.info('\t%s', pkg.name)
            pkg.freeze(store)

        G = nx.DiGraph()
        digest = hashlib.sha256()
        for pkg in packages:
            G.add_node(pkg)

            for dep in pkg.dependencies:
                G.add_edge(pkg, dep)

            digest.update(str(pkg))

        return cls(digraph=G, sha256=digest.hexdigest())

    def graphviz(self, filename):
        logger.info('Creating graphviz depiction in %s', filename)

        outprefix, ext = os.path.splitext(filename)
        plugin = ext.lstrip('.')

        dotfile = outprefix + '.dot'
        outfile = outprefix + '.' + plugin

        nx.nx_agraph.write_dot(self.digraph, dotfile)
        cmd = ['dot', '-Grankdir=LR', '-T%s' % plugin, dotfile]
        data = check_output(cmd)
        with open(outfile, 'wb') as fd:
            fd.write(data)



if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    G = Graph.from_names(['bucket-list'])
    # build_graph(['azure'])
    # build_graph(['shade'], buildInputs=set(['openssl']))
    # build_graph(['cloudmesh_client'], buildInputs=set(['openssl libffi']))

    G.graphviz(outprefix='/tmp/test')
