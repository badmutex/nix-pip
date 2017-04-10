
.PHONY: test
test: cloudmesh.core
	cd cloudmesh.core && nix-pip -g requirements.pdf

cloudmesh.core:
	git clone --depth 1 --branch dev "git://github.com/cloudmesh/cloudmesh.core"
