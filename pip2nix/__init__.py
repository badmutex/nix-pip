from pkg_resources import get_distribution

__version__ = get_distribution('pip2nix').version
version = __version__
