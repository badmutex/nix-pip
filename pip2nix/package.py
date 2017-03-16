from __future__ import print_function

import hashlib
import json
import logging
from pipes import quote

from munch import munchify
import networkx as nx
from traits.api import HasTraits, Str, Set, This, Bool


logger = logging.getLogger(__name__)





def empty_venv_packages():
    logger.info('Determining preinstalled packages in a virtualenv')
    with tmpvenv() as (shell, venvdir, pip):
        frozen = freeze([])
        pkgs = set([p.name for p in frozen])
        return pkgs




class Package(HasTraits):

    name = Str
    version = Str
    dependencies = Set(This)
    preinstalled = Set(Str)
    buildInputs = Set(Str)
    doCheck = Bool(True)

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

    extraPackages = extraPackages or set()
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
        G.add_node(pkg)

        for dep in pkg.dependencies:
            G.add_edge(pkg, dep)

    dotfile = '/tmp/test.dot'
    graphviz_type = 'pdf'
    nx.nx_agraph.write_dot(G, dotfile)
    cmd = ['dot', '-Grankdir=LR', '-T%s' % graphviz_type, dotfile]
    data = check_output(cmd)
    with open('/tmp/test.%s' % graphviz_type, 'wb') as fd:
        fd.write(data)



if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    build_graph(['bucket-list'])
    # build_graph(['azure'])
    # build_graph(['shade'], extraPackages=set(['openssl']))
    # build_graph(['cloudmesh_client'], extraPackages=set(['openssl libffi']))
