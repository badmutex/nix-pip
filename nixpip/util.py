import warnings
import functools
import itertools
import os
import shelve
import shutil
import tempfile

from contextlib import contextmanager

from nixpip.nixshell import NixShell


def concat(iters):
    return list(itertools.chain(*iters))


def default_config_dir():

    xdg_config_dir = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config_dir:
        prefix = xdg_config_dir
        subdir = 'nixpip'
    else:
        prefix = '~'
        subdir = '.nixpip'

    path = os.path.join(prefix, subdir)
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''

    # https://wiki.python.org/moin/PythonDecoratorLibrary#Smart_deprecation_warnings_.28with_valid_filenames.2C_line_numbers.2C_etc..29

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func


@contextmanager
def tmpdir():
    d = tempfile.mkdtemp()
    try:
        yield d
    finally:
        shutil.rmtree(d)


@contextmanager
def tmpfile():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        yield path
    finally:
        os.unlink(path)


@contextmanager
def tmpvenv(python='python', venvdir=None, buildInputs=None):

    import pkg_resources
    python_bare = pkg_resources.resource_filename(__name__, 'data/python-bare.nix')

    with tmpdir() as venvdir:
        shell = NixShell(python_bare, packages=buildInputs)
        shell.command(['virtualenv', venvdir])
        pip = os.path.join(venvdir, 'bin', 'pip')
        yield (shell, venvdir, pip)


@contextmanager
def shelve_open(*args, **kwargs):
    "Passthrough to :func:`shelve.open`"

    shelf = shelve.open(*args, **kwargs)
    try:
        yield shelf
    finally:
        shelf.sync()
        shelf.close()
