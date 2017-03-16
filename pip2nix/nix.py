from traits.api import HasTraits, Trait, Bool

from pip2nix import pypi, package

import pkg_resources
from cStringIO import StringIO
from subprocess import check_output, CalledProcessError
import textwrap

import click
import networkx as nx


import logging
logger = logging.getLogger(__name__)


drv_whl = pkg_resources.resource_filename(__name__,
                                               'data/derivation.nix.template')

fetchurl_tmpl = pkg_resources.resource_string(
    __name__,
    'data/fetchurl.nix.template'
)

fetchPypi_tmpl = pkg_resources.resource_string(
    __name__,
    'data/fetchPypi.nix.template'
)

mkDerivation_tmpl = pkg_resources.resource_string(
    __name__,
    'data/mkDerivation.nix.template'
)

mkRequirements_tmpl = pkg_resources.resource_string(
    __name__,
    'data/requirements.nix.template'
)






def indent(s, by=2, using=' '):
    return s.replace('\n', '\n' + by * using)


def fetchurl(url, sha256):
    return fetchurl_tmpl.format(
        url = url,
        sha256 = sha256,
    )


def fetchPypi(name, version, sha256):
    return fetchPypi_tmpl.format(
        name = name,
        version = version,
        sha256 = sha256,
    )




def mkPackageSet(requirements):

    builder = StringIO()

    for entry in requirements:
        drv = mkDerivation(entry)
        s = '{name} = {drv};\n'.format(name=entry.name, drv=indent(drv))
        builder.write(s)

    reqs = mkRequirements_tmpl.format(packages=indent(builder.getvalue()))
    builder.close()

    return reqs


class Package(HasTraits):

    package = Trait(package.Package)
    pypi = Trait(pypi.Package)
    doCheck = Bool(True)

    def mkDerivation(self):
        logger.info('mkDerivation for %s', self.package)

        if self.pypi.pinned.kind == 'source':
            format = 'setuptools'

        elif self.pypi.pinned.kind == 'universal':
            format = 'wheel'

        else:
            raise NotImplementedError(self.pypi.pinned.kind)

        fetcher = fetchurl(url=self.pypi.pinned.url,
                           sha256=self.pypi.pinned.sha256)

        drv = mkDerivation_tmpl.format(
            name = self.package.name,
            version = self.package.version,
            fetcher = indent(fetcher),
            format = format,
            pythonDependencies = ' '.join(map(lambda pkg: pkg.name, self.package.dependencies)),
            buildInputs = ' '.join(self.package.buildInputs),
            doCheck = 'true' if self.doCheck else 'false',
        )

        return drv


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    logging.getLogger('requests').setLevel('WARNING')

    # G = package.build_graph(['bucket-list'])
    G = package.Graph.from_names(['munch', 'cryptography'], extraPackages=set(['openssl']))

    packages = dict([(p.name, p) for p in G.nodes()])

    pypi_packages = dict(
        [(p.name, pypi.Package.from_pypi(p.name)) for p in packages.values()]
    )

    for pkg in G.nodes():
        pypi_packages[pkg.name].pin(version=pkg.version)

    nix_packages = [Package(package = packages[p.name],
                            pypi = pypi_packages[p.name],
                            doCheck = False)
                    for p in packages.values()]

    for p in nix_packages:
        print(p.mkDerivation())


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--gv/--no-gv', default=True)
@click.option('-T', '--graphviz-type', default='pdf')
@click.option('-d', '--dot', type=click.Path())
@click.option('-o', '--out', type=click.Path())
@click.option('-r', '--reqnix', type=click.File('w'), default='requirements.nix')
def main(path, gv, graphviz_type, dot, out, reqnix):

    logging.basicConfig(
        level='INFO',
        format='%(levelname)-9s %(name)-8s %(message)s '
    )
    logging.getLogger('requests').setLevel('WARNING')

    try:
        reqs = pypi.RequirementsSet(path)
        reqs.verify_dependencies()
        reqs.build()
        G = reqs.graph()

        expr = mkPackageSet(reqs)
        print(expr)
        reqnix.write(expr)

        if gv:
            dotfile = dot or path + '.dot'
            logger.info('Writing %s', dotfile)
            nx.nx_agraph.write_dot(G, dotfile)

            outfile = out or path + '.' + graphviz_type
            cmd = ['dot', '-Grankdir=LR', '-T%s' % graphviz_type, dotfile]
            logger.debug('Running cmd %s', ' '.join(cmd))
            data = check_output(cmd)

            logger.info('Writing %s', outfile)
            with open(outfile, 'wb') as fd:
                fd.write(data)

    except CalledProcessError, e:
        print(e.cmd)
        print(e.returncode)
        print(e.output)
