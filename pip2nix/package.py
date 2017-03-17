from __future__ import print_function

import hashlib
import json
import logging
from collections import defaultdict
from pipes import quote
from subprocess import check_output

from munch import munchify
import networkx as nx
from traits.api import HasTraits, Trait, Dict, List, Str, Set, This

from pip2nix.util import tmpvenv


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

        ver = self.version
        for old, new in tx.items():
            ver = ver.replace(old, new)

        logger.debug('%s updating version to %s', self.name, ver)
        self.version = ver

        for dep in self.dependencies:
            dep.apply_version_transformations(transformations=tx)

    def find_requirements(self):
        logger.debug('Finding requirements for %s', self)

        if is_cached(self):
            logger.debug('Using cached %s', self)
            return

        frozen = freeze([self.frozen_name],
                        preinstalled=self.preinstalled.keys(),
                        buildInputs=self.buildInputs.get(self.name))

        for entry in frozen:
            if entry.name == self.name:
                continue

            pkg = Package(name=entry.name, version=entry.version,
                          preinstalled=self.preinstalled,
                          buildInputs=self.buildInputs)

            self.dependencies.add(pkg)


    def prune_dependencies(self):
        logger.debug('Prunning dependencies for %s', self)

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



def freeze(packages, preinstalled=None, buildInputs=None):
    preinstalled = preinstalled or set()

    logger.debug('Freezing packages: %s', ', '.join(packages))
    with tmpvenv(buildInputs=buildInputs) as (shell, venvdir, pip):
        if packages:
            shell([pip, 'install'] + map(quote, packages))

        frozen = shell([pip, 'list', '--format', 'json'])
        frozen_json = json.loads(frozen.strip())
        munched = filter(
            lambda pkg: pkg.name not in preinstalled,
            munchify(frozen_json))
        return munched


class Graph(HasTraits):

    digraph = Trait(nx.DiGraph)

    def __getattr__(self, name):
        return getattr(self.digraph, name)

    @classmethod
    def from_names(cls, names, buildInputs=None):
        logger.info('Building dependency graph for %s', ' '.join(names))

        buildInputs = buildInputs or defaultdict(list)
        preinstalled = empty_venv_packages()
        logger.info('Preinstalled packages: %s', ', '.join(preinstalled))

        frozen = freeze(names, preinstalled=preinstalled)

        packages = preinstalled.values() + \
                   [Package(name=p.name, version=p.version,
                            preinstalled=preinstalled, buildInputs=buildInputs)
                    for p in frozen]
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

        G = nx.DiGraph()
        for pkg in packages:
            G.add_node(pkg)

            for dep in pkg.dependencies:
                G.add_edge(pkg, dep)

        return cls(digraph=G)

    def graphviz(self, outprefix='requirements', type='pdf'):
        logger.info('Creating graphviz depiction')

        dotfile = outprefix + '.dot'
        outfile = outprefix + '.' + type

        nx.nx_agraph.write_dot(self.digraph, dotfile)
        cmd = ['dot', '-Grankdir=LR', '-T%s' % type, dotfile]
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
