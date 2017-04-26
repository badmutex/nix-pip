from traits.api import HasTraits, Trait, List, Dict, Str, Bool

from nixpip import pypi, package

import pkg_resources
from cStringIO import StringIO



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

    requirements = sorted(requirements, cmp=lambda a, b: cmp(a.name.lower(), b.name.lower()))

    for pkg in requirements:
        drv = pkg.mkDerivation()
        s = '{name} = {drv};\n'.format(name=pkg.name.lower(), drv=indent(drv))
        builder.write(s)

    reqs = mkRequirements_tmpl.format(packages=indent(builder.getvalue()))
    builder.close()

    return reqs


def nixifyName(name):
    return name.replace('.', '-')


class Package(HasTraits):

    package = Trait(package.Package)
    pypi = Trait(pypi.Package)
    doCheck = Bool(True)
    setupRequires = List(Str)
    buildInputs = Dict(Str, List(Str))

    @property
    def name(self):
        return nixifyName(self.package.name)

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

        inputs = self.buildInputs.get(self.package.name, [])
        buildInputs = ' '.join(sorted(inputs))

        propagatedBuildInputs = [nixifyName(p.name) for p in self.package.dependencies] + \
                                self.setupRequires
        propagatedBuildInputs.sort()


        drv = mkDerivation_tmpl.format(
            name = self.package.name,
            version = self.package.version,
            fetcher = indent(fetcher),
            format = format,
            pythonDependencies = ' '.join(propagatedBuildInputs),
            buildInputs = buildInputs,
            doCheck = 'true' if self.doCheck else 'false',
        )

        return drv
