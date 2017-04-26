{ pkgs ? import ./nixpip/data/nixpkgs.nix
, deployment ? "user"
}:

with pkgs;

let

  nixpip = callPackage ./nixpip.nix {
    requirements_nix = ./requirements.nix;
    runtime = ./requirements.open;
    testing = ./test_requirements.open;
  };

  version = builtins.readFile ./nixpip/VERSION;

  name = {
    user = "runtime";
    dev  = "all";
  }."${deployment}";

  buildInputs = [
    cacert
    libffi
    openssl
    pkgconfig
    sqlite
    zlib
  ];

in

pythonPackages.buildPythonApplication {
  inherit version;
  name = "nixpip-${version}";
  buildInputs = buildInputs;
  propagatedBuildInputs = nixpip.requirements."${name}";
  src = ./.;
}
