from pkg_resources import get_distribution

__version__ = get_distribution('nixpip').version
version = __version__
