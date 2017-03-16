
from setuptools import setup, find_packages



setup (

    name = 'pip2nix',
    use_scm_version = True,
    setup_requires = ['setuptools_scm'],
    url = 'https://github.com/badi/pip2nix',
    license = 'Apache 2.0',
    packages = find_packages(exclude=['docs', 'test']),
    package_data = {
        'pip2nix': ['data/*'],
    },
    entry_points = {
        'console_scripts': [
            'pip2nix=pip2nix.nix:main',
        ],
    },
)
