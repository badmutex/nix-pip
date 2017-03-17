
from munch import Munch, munchify
import requests
from traits.api import HasTraits, Trait, File, Enum, Str, Dict, Int, List

import hashlib
import json
import logging
import os.path
import re
import sys

from collections import defaultdict

logger = logging.getLogger(__name__)


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


def identify_release_kind(release):

    if release.packagetype == 'sdist':
        ptype = 'source'
    elif release.packagetype == 'bdist_wheel' and is_universal_wheel(release.filename):
        ptype = 'universal'
    elif release.packagetype.startswith('bdist_'):
        ptype = 'binary'
    else:
        logger.critical('Could not determine package type for {}: {}'.
                        format(release.filename, release.packagetype))
        raise NotImplementedError(release.filename, release.packagetype)

    logger.debug('Determine package type for {}: {}'.format(release.filename, ptype))
    return ptype




def identify_release_platform(release):
    "Returns the appropriate OS platform (unix, linux, mac, win, any, unknown) from a pypi resonse"

    logger.debug('Looking up platform for %s', release.filename)

    def check_pkg(pkgs):
        return any([release.packagetype == pkg for pkg in pkgs.split()])

    def check_ext(patterns):

        if isinstance(patterns, str):
            patterns = patterns.split()
        elif isinstance(patterns, list):
            patterns = patterns
        else:
            raise NotImplementedError(patterns)

        logger.debug('Checking %s against %s', release.filename, patterns)
        result = [re.search(pat, str(release.filename)) for pat in patterns]
        logger.debug('Matched: %s', result)
        return any(result)

    if check_ext(r'.+-any\.whl'):
        result = 'any'

    elif check_ext(r'.+\.rpm .+linux[a-z_0-9-]+\.(whl|egg|tar\.gz)'):
        result = 'linux'

    elif check_ext(r'.+\.exe .+-win(32|_amd64)\.whl'):
        result = 'win'

    elif check_ext(r'.+macosx-?[a-z_0-9]+\.(whl|egg)'):
        result = 'mac'

    elif check_pkg('sdist'):
        result = 'any'

    elif check_pkg('bdist_wheel') and is_universal_wheel(release.filename):
        result = 'unknown'

    elif check_pkg('bdist_wininst') or check_pkg('bdist_msi'):
        result = 'win'

    elif check_pkg('bdist_rpm'):
        result = 'linux'

    elif check_pkg('bdist_egg'):
        result = 'unknown'

    elif check_pkg('bdist_dumb'):
        result = 'unknown'

    elif is_archive(release.filename):
        result = 'any'

    else:
        logger.critical('Cannot handle %s as %s', release.filename, release.packagetype)
        raise NotImplementedError(release.filename, release.packagetype)

    logger.debug('Platform is %s', result)
    return result


def get_package(package, session=None):
    url = 'https://pypi.python.org/pypi/{}/json'.format(package)
    logger.info('Querying PyPi for %s', package)

    query = session or requests
    response = query.get(url)

    if not response.status_code == 200:
        logger.critical('GET %s failed with %s', url, response.status_code)
        raise NotImplementedError((url, response))

    return munchify(json.loads(response.content))



PyPiResponse = Munch


class Release(HasTraits):

    upload_time = Str
    comment_text = Str
    python_version = Str
    url = Str
    md5 = Str
    sha256 = Str(minlength=64, maxlength=64)  # 64 is the length of the sha256 hexdigest
    kind = Enum('source', 'universal', 'binary')
    packagetype = Enum('sdist', 'bdist_dumb', 'bdist_egg', 'bdist_rpm', 'bdist_wheel', 'bdist_wininst', 'bdist_msi')
    filename = Str
    platform = Enum('unix', 'linux', 'mac', 'win', 'any', 'unknown')
    downloads = Int
    size = Int

    @classmethod
    def from_pypi(cls, pypi_data):
        "Convert a `munchify`-ed response from PyPi"

        return cls(
            upload_time = pypi_data.upload_time,
            comment_text = pypi_data.comment_text,
            python_version = pypi_data.python_version,
            url = pypi_data.url,
            md5 = pypi_data.md5_digest,
            kind = identify_release_kind(pypi_data),
            packagetype = pypi_data.packagetype,
            filename = pypi_data.filename,
            platform = identify_release_platform(pypi_data),
            downloads = pypi_data.downloads,
            size = pypi_data.size,
        )

    def pin(self, session=None):
        query = session or requests
        response = query.get(self.url)
        self.sha256 = hashlib.sha256(response.content).hexdigest()


class Package(HasTraits):

    session = Trait(requests.Session)
    pypi = Trait(PyPiResponse)
    releases = Dict(Str, Dict(Str, List(Release)))  # version str -> kind -> [Release]
    pinned = Trait(Release)

    @classmethod
    def from_pypi(cls, name, session=None):
        pypi = get_package(name, session=session)

        all_releases = defaultdict(lambda: defaultdict(list))
        for version, releases in pypi.releases.items():
            for release in releases:
                rel = Release.from_pypi(release)
                all_releases[version][rel.kind].append(rel)

        return cls(pypi=pypi, releases=all_releases, session=session)

    def pin(self, version):
        releases = self.releases[version]

        prefered_kinds = ['universal', 'source']
        for k in prefered_kinds:
            if k in releases:
                kind_releases = releases[k]
                r = kind_releases[0]
                logger.debug('Pinned %s (%s, %s)', r.kind, r.filename, r.packagetype)
                r.pin(session=self.session)
                self.pinned = r
                return

        import pdb; pdb.set_trace()
        raise Exception('Unable to pin')



if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    logging.getLogger('requests').setLevel('WARNING')
    p = Package.from_pypi('bucket-list')
    p.pin('0.3.8')
