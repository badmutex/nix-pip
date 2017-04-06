
.PHONY: dev install

dev:
	nix-shell

install:
	nix-env -f . -i

