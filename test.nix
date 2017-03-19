{ pkgs ? import ./pip2nix/data/nixpkgs.nix
, name ? "test"
, requirements ? ./requirements.nix
}:

with pkgs;

let

  inherit (lib)
    attrValues
    ;

  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  requirements' = import requirements {
    inherit pkgs;
    inherit (pkgs) fetchurl;
    inherit (pythonPackages) buildPythonPackage;
  };

  python = with pythonPackages; pythonFull.withPackages (_ :
    attrValues requirements'
    # ++ [ virtualenv wheel six packaging setuptools pip pyparsing appdirs ]
  );

  buildInputs = [
  ];

in

pythonPackages.buildPythonPackage {
  name = "${name}";
  buildInputs = [ python ] ++ buildInputs;
}
