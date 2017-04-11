
from setuptools import setup, find_packages



setup (

    name = 'nixpip',
    version = open('nixpip/VERSION').read().strip(),
    url = 'https://github.com/badi/nixpip',
    license = 'Apache 2.0',
    packages = find_packages(exclude=['docs', 'test']),
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'nix-pip=nixpip.main:entrypoint',
        ],
    },
)
