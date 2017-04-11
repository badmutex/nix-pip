
.PHONY: dev install changelog test dockertest

default: test

dev:
	nix-shell --argstr deployment dev

install:
	nix-env -f . -i

changelog:
	gitchangelog >CHANGELOG.rst

test:
	nix-shell --argstr deployment dev --command 'py.test -s tests/test.py'

dockertest:
	docker run -v $(PWD):/data --rm nixos/nix:latest bash /data/tests/docker.sh
# this runs the same test as above in a docker container


################################################################

requirements.nix: .nix-pip.rc requirements.open test_requirements.open
	nix-shell --command 'nix-pip -l /dev/null'
