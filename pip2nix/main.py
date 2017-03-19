
import click
import os
import os.path

import nix
import pypi
from requirements import Requirements

from collections import defaultdict

import coloredlogs
import logging
logger = logging.getLogger()
coloredlogs.install(fmt='%(asctime)s %(message)s',
                    datefmt='%H:%M:%S',
                    level_styles={
                        'info': {'color': 'white'},
                        'debug': {'color': 'yellow'},
                        'critical': {'color': 'red', 'bold': True},
                        'error': {'color': 'red'}})



def do_requirements(paths):

    logger.info('Loading requirements from %s', ', '.join(paths))

    if not paths:
        logger.critical('No requirements paths given')

    path0 = paths.pop(0)
    reqs = Requirements.from_file(path0)

    for path in paths:
        r = Requirements.from_file(path)
        reqs = reqs.merge(r)

    return reqs


def user_package_additions(inputs):
    """Process the user-specified package-specific build inputs

    The inputs are in the form:
    ("python package name", "other_name1,other_name2,other_name_etc")

    :rtype: :class:`dict` from package name -> [other name]
    """

    ret = defaultdict(list)
    for pkg, deps in inputs:
        names = str(deps).split(',')
        names = map(str.strip, names)
        ret[str(pkg)] = names

    return ret


def default_config_dir():

    xdg_config_dir = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_dir:
        prefix = xdg_config_dir
        subdir = 'pip2nix'
    else:
        prefix = '~'
        subdir = '.pip2nix'

    path = os.path.join(prefix, subdir)
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


@click.command()
@click.option('-r', '--requirements', multiple=True, help='Paths to the requirments files')
@click.option('-p', '--package', multiple=True, help='Package names')
@click.option('-i', '--build-inputs', nargs=2, multiple=True)
@click.option('-s', '--setup-requires', nargs=2, multiple=True)
@click.option('-C', '--config-dir', default=default_config_dir)
@click.option('-g', '--graphviz', help='Generate a graphviz plot in this file')
@click.option('-o', '--out-file', default='requirements.nix')
def main(requirements, package, build_inputs, setup_requires, config_dir, graphviz, out_file):

    requirements = list(requirements)
    buildInputs = user_package_additions(build_inputs)
    setupRequires = user_package_additions(setup_requires)

    if not os.path.exists(config_dir):
        logger.debug('Creating missing config dir %s', config_dir)
        os.makedirs(config_dir)


    if requirements:
        reqs = do_requirements(requirements)

    else:
        reqs = Requirements()

    for name in package:
        reqs.add(name)

    shelf = os.path.join(config_dir, 'cache.dat')

    ################################################################

    reqs.unpersist(shelf)
    reqs.build_graph(buildInputs=buildInputs)
    reqs.persist(shelf)

    ################################################################

    if graphviz:
        reqs.graphviz(graphviz)

    ################################################################

    packages = dict([(p.name, p) for p in reqs.graph.nodes()])

    session = pypi.requests.Session()
    pypi_packages = dict(
        [(p.name, pypi.Package.from_pypi(p.name, session=session)) for p in packages.values()]
    )

    logger.info('Pinning packages')
    for pkg in reqs.graph.nodes():
        logger.debug('Pinning %s to %s', pkg.name, pkg.version)
        pypi_packages[pkg.name].pin(pkg.version)

    logger.info('Creating Nix derivations')
    nix_packages = [
        nix.Package(package=packages[p.name],
                    pypi=pypi_packages[p.name], doCheck=False,
                    buildInputs=buildInputs,
                    setupRequires=setupRequires[p.name])

        for p in packages.values()]


    reqs_nix = nix.mkPackageSet(nix_packages)

    with open(out_file, 'w') as fd:
        fd.write(reqs_nix)
        logger.info('Wrote %s', fd.name)


def entrypoint():
    main()
