
from setuptools import setup, find_packages



setup (

    name = 'pip2nix',
    version = open('pip2nix/VERSION').read().strip(),
    url = 'https://github.com/badi/pip2nix',
    license = 'Apache 2.0',
    packages = find_packages(exclude=['docs', 'test']),
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'pip2nix=pip2nix.main:entrypoint',
        ],
    },
)
