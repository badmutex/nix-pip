

let

  pkgs = import <nixpkgs> {};

  # to get the new set of hashes, run
  # nix-prefetch-git git://github.com/NixOS/nixpkgs-channels refs/heads/nixpkgs-unstable
  hashes = {

    "2017-02-17" = {
      rev = "89a036506396dd869474a32e984f5cab5c07992a";
      sha256 = "04fxjh5ca41rlnvc4ggbgh41j4mkqj685inxj2xbm9i8giabncw1";
    };


  };

  origin = hashes."2017-02-17" // {
    owner = "NixOS";
    repo = "nixpkgs-channels";
  };

  src = pkgs.fetchFromGitHub origin;

in

import src {}
