import operator
from pipes import quote
from subprocess import check_output, CalledProcessError

import logging
logger = logging.getLogger(__name__)


class NixShell(object):

    def __init__(self, drv='<nixpkgs>', pkgs=None, pure=True, packages=None):
        self.drv = drv
        self.pkgs = pkgs
        self.pure = pure
        self.packages = packages or []


    def command(self, cmd):
        "Pass cmd to --command"

        cmd = ' '.join(map(quote, cmd))

        monoid = [['nix-shell', self.drv],
                  ['--command', cmd]]

        if self.pkgs:
            monoid.append(['--arg', 'pkgs', self.pkgs])

        if self.pure:
            monoid.append(['--pure'])

        if self.packages:
            inputs = ' '.join(self.packages)
            monoid.append(['--argstr', 'buildInputNames', inputs])


        torun = reduce(operator.add, monoid)
        logger.debug('Executing: %s', ' '.join(map(quote, torun)))

        try:
            output = check_output(torun)
        except CalledProcessError as e:
            logger.error('Output:\n' + e.output)
            raise

        logger.debug(output)
        return output

    def __call__(self, cmd):
        return self.command(cmd)
