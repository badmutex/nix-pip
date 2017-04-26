from traits.api import HasTraits, List, Dict, File, Instance, Set, Str

import copy
import os.path
import pkg_resources

from ruamel import yaml
from munch import munchify


def dictify(obj):
    if isinstance(obj, dict):
        d = obj
    elif hasattr(obj, 'dict'):
        d = obj.dict()
    else:
        return obj

    dd = copy.copy(d)
    for k in dd.keys():
        v = dd[k]
        vv = dictify(v)
        dd[k] = vv

    return dd


class Requirements(HasTraits):

    inputs = List(File(exists=True))
    output = File
    packages = List(Str)
    graphviz = File

    def dict(self):
        return dictify(self.__dict__)


class Config(HasTraits):

    requirements = Instance(Requirements)
    setup_requires = Dict(Str, List(Str))
    build_inputs = Dict(Str, List(Str))

    def add_input(self, *paths):
        for path in paths:
            self.requirements.inputs.append(path)

    def set_output(self, path=None):
        if path:
            self.requirements.output = path

    def set_graphviz(self, path=None):
        if path:
            self.requirements.graphviz = path

    def add_package(self, *pkgs):
        for pkg in pkgs:
            self.requirements.packages.append(pkg)

    def add_setup_requires(self, *pairs):
        for pkg, drv in pairs:
            self.setup_requires[pkg].append(drv)

    def add_build_inputs(self, *pairs):
        for pkg1, pkg2 in pairs:
            self.build_inputs[pkg1].append(pkg2)

    def dict(self):
        return dictify(self.__dict__)

    def __str__(self):
        d = self.dict()
        return yaml.dump(d, default_flow_style=False)


def read(path=None):

    defaults = pkg_resources.resource_string(__name__, 'data/nix-pip.rc')
    default = yaml.safe_load(defaults)

    if path and os.path.exists(path):

        with open(path) as fd:
            cfg = yaml.safe_load(fd)

    else:
        cfg = default

    cfg = munchify(cfg)
    return Config(requirements=Requirements(**cfg.requirements),
                  setup_requires=cfg.setup_requires,
                  build_inputs=cfg.build_inputs)



if __name__ == '__main__':
    import sys

    try:
        c = read(sys.argv[1])
        print str(c)
    except IndexError:
        print read()
