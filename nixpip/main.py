
from nixpip.util import default_config_dir
from nixpip.store import Store
from nixpip import config

import click
import os
import os.path
import pkg_resources

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


def load_requirements(paths=None, packages=None):

    paths = paths or []
    paths = filter(os.path.exists, paths)

    reqs = Requirements()

    if paths:
        reqs = do_requirements(paths)

    if packages:
        for name in packages:
            reqs.add(name)

    return reqs


@click.command()
@click.option('-V', '--version', help='Show version and exit', default=False, is_flag=True)
@click.option('-r', '--requirements', multiple=True, help='Paths to the requirments files')
@click.option('-p', '--package', multiple=True, help='Package names')
@click.option('-i', '--build-inputs', nargs=2, multiple=True)
@click.option('-s', '--setup-requires', nargs=2, multiple=True)
@click.option('-C', '--config-dir', default=default_config_dir)
@click.option('-g', '--graphviz', help='Generate a graphviz plot in this file')
@click.option('-o', '--out-file', default='requirements.nix')
@click.option('-l', '--lib-file', default='nixpip.nix')
@click.option('-f', '--rc-file', default='.nix-pip.rc')
def main(version, requirements, package, build_inputs, setup_requires, config_dir, graphviz, out_file, lib_file, rc_file):

    version_file = pkg_resources.resource_filename(__name__, 'VERSION')
    with open(version_file) as fd:
        my_version = fd.read().strip()

    if version:
        click.echo(my_version)
        return


    requirements = list(requirements)
    buildInputs = user_package_additions(build_inputs)
    setupRequires = user_package_additions(setup_requires)

    cfg = config.read(rc_file)
    cfg.add_input(*requirements)
    cfg.set_output(out_file)
    cfg.add_package(*package)
    cfg.add_setup_requires(*setupRequires.items())
    cfg.add_build_inputs(*buildInputs.items())

    logger.debug('Requirements %s', cfg.requirements.inputs)
    logger.debug('Packages %s', cfg.requirements.packages)
    logger.debug('Build Inputs: %s', cfg.build_inputs)
    logger.debug('Set Requirements: %s', cfg.setup_requires)


    if not os.path.exists(config_dir):
        logger.debug('Creating missing config dir %s', config_dir)
        os.makedirs(config_dir)


    reqs = load_requirements(cfg.requirements.inputs, cfg.requirements.packages)
    store = Store(path=os.path.join(config_dir, 'store.dat'))
    reqs.store = store

    ################################################################

    reqs.build_graph(buildInputs=cfg.build_inputs)

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
                    buildInputs=cfg.build_inputs,
                    setupRequires=cfg.setup_requires.get(p.name, []))

        for p in packages.values()]


    reqs_nix = nix.mkPackageSet(nix_packages)

    with open(out_file, 'w') as fd:
        fd.write(reqs_nix)
        logger.info('Wrote %s', fd.name)

    with open(lib_file, 'w') as fd:
        lib = pkg_resources.resource_string(__name__, 'data/nixpip.nix')
        fd.write(lib)
        logger.info('Wrote %s', fd.name)


def entrypoint():
    main()
