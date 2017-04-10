# This file is indended to run in a docker container
# https://hub.docker.com/r/nixos/nix/

set -e
nix-channel --update
nix-env -iA nixpkgs.{gnumake,git,graphviz-nox}
cp -R /data /test
make -C /test
