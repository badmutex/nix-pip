import operator
from pipes import quote
from subprocess import check_output

import logging
logger = logging.getLogger(__name__)


class NixShell(object):

    def __init__(self, pkgs='<nixpkgs>', pure=True, packages=None):
        self.pkgs = pkgs
        self.pure = pure
        self.packages = packages or []


    def command(self, cmd):
        "Pass cmd to --command"

        cmd = ' '.join(map(quote, cmd))

        monoid = [['nix-shell', self.pkgs],
                  ['--command', cmd]]

        if self.pure:
            monoid.append(['--pure'])

        if self.packages:
            inputs = ' '.join(self.packages)
            monoid.append(['--argstr', 'buildInputNames', inputs])


        torun = reduce(operator.add, monoid)
        logger.debug('Executing: %s', ' '.join(map(quote, torun)))
        output = check_output(torun)
        logger.debug(output)
        return output

    def __call__(self, cmd):
        return self.command(cmd)
