{ pkgs ? import ../../nixpip/data/nixpkgs.nix
, deployment ? "user"
}:

with pkgs;

let

  nixpip = callPackage ./nixpip.nix {
    requirements_nix = ./requirements.nix;
    runtime = ./requirements.txt;
  };

  name = {
    user = "runtime";
    dev  = "all";
  }."${deployment}";

in

pythonPackages.buildPythonApplication {
  name = "xeno-nixpip-test";
  propagatedBuildInputs = nixpip.requirements."${name}";
  src = ./.;
}
