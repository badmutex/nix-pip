
.PHONY: dev install changelog test

default: test

dev:
	nix-shell

install:
	nix-env -f . -i

changelog:
	gitchangelog >CHANGELOG.rst

test:
	nix-shell --command 'py.test tests/test.py'
