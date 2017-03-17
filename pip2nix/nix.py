from traits.api import HasTraits, Trait, Dict, List, Str, Bool

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


def mkPackageSet(requirements):

    builder = StringIO()

    for pkg in requirements:
        drv = pkg.mkDerivation()
        s = '"{name}" = {drv};\n'.format(name=pkg.package.name, drv=indent(drv))
        builder.write(s)

    reqs = mkRequirements_tmpl.format(packages=indent(builder.getvalue()))
    builder.close()

    return reqs


class Package(HasTraits):

    package = Trait(package.Package)
    pypi = Trait(pypi.Package)
    doCheck = Bool(True)
    setupRequires = Dict(Str, List(Str))

    @property
    def name(self):
        return self.package.name

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

        inputs = self.package.buildInputs.get(self.name, []) + \
                 self.setupRequires.get(self.name, [])
        buildInputs = ' '.join(inputs)


        drv = mkDerivation_tmpl.format(
            name = self.package.name,
            version = self.package.version,
            fetcher = indent(fetcher),
            format = format,
            pythonDependencies = ' '.join(map(lambda pkg: pkg.name, self.package.dependencies)),
            buildInputs = buildInputs,
            doCheck = 'true' if self.doCheck else 'false',
        )

        return drv




def user_package_additions(inputs):
    """Process the user-specified package-specific build inputs

    The inputs are in the form:
    ("python package name", "other_name1,other_name2,other_name_etc")

    :rtype: :class:`dict` from package name -> [other name]
    """

    ret = dict()
    for pkg, deps in inputs:
        names = str(deps).split(',')
        names = map(str.strip, names)
        ret[str(pkg)] = names

    return ret


@click.command()
@click.argument('pkgs', nargs=-1)
@click.option('-i', '--build-inputs', nargs=2, multiple=True)
@click.option('-s', '--setup-requires', nargs=2, multiple=True)
@click.option('-o', '--out-file', default='requirements.nix')
@click.option('-p', '--graphviz-prefix', default='requirements')
@click.option('-T', '--graphviz-type', default='pdf')
def main(pkgs, build_inputs, setup_requires, out_file, graphviz_prefix, graphviz_type):

    pkgs = map(str, pkgs)
    buildInputs = user_package_additions(build_inputs)
    setupRequires = user_package_additions(setup_requires)

    import coloredlogs
    coloredlogs.install()

    logging.basicConfig(level='DEBUG')
    logging.getLogger('requests').setLevel('WARNING')

    G = package.Graph.from_names(pkgs, buildInputs=buildInputs)
    G.graphviz(outprefix=graphviz_prefix, type=graphviz_type)

    packages = dict([(p.name, p) for p in G.nodes()])

    pypi_packages = dict(
        [(p.name, pypi.Package.from_pypi(p.name)) for p in packages.values()]
    )

    logger.info('Pinning packages')
    for pkg in G.nodes():
        logger.debug('Pinning %s to %s', pkg.name, pkg.version)
        pypi_packages[pkg.name].pin(pkg.version)

    logger.info('Creating Nix derivations')
    nix_packages = [Package(package=packages[p.name],
                            pypi=pypi_packages[p.name], doCheck=False,
                            setupRequires=setupRequires[p.name])

                    for p in packages.values()]


    reqs = mkPackageSet(nix_packages)
    print(reqs)

    with open(out_file, 'w') as fd:
        fd.write(reqs)
