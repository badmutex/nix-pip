{ pkgs ? import ./pip2nix/data/nixpkgs.nix
, venvdir ? ".venv"
}:

with pkgs;

let

  inherit (lib)
    getAttr
    hasAttr
    hasPrefix
    fileContents
    filter
    splitString
    stringLength
    ;


  version = builtins.readFile ./VERSION;

  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  packages = import ./requirements.nix {
    inherit pkgs fetchurl;
    inherit (pythonPackages) buildPythonPackage;
  };

  myPythonPackages = pythonPackages // packages;

  readRequirements = file:
    let
      cleaner = line: !(hasPrefix "#" line) && (stringLength line > 0);
      lines = splitString "\n" (fileContents file);
    in filter cleaner lines;

  findPackages = set: packageNames:
    let
      findPkg = name:
        if hasAttr name set
        then getAttr name set
        else throw "Cannot find '${name}'";
    in map findPkg packageNames;

  findPythonPackages = path: findPackages myPythonPackages (readRequirements path);

  requirements      = findPythonPackages ./requirements.open;
  test_requirements = findPythonPackages ./test_requirements.open;

  python = pythonFull.buildEnv.override {
    extraLibs = requirements ++ test_requirements;
    ignoreCollisions = true;
  };


  buildInputs = [
    cacert
    libffi
    openssl
    pkgconfig
    sqlite
    zlib
  ];

in

pythonPackages.buildPythonPackage {
  inherit version;
  name = "pip2nix-${version}";
  buildInputs = [ python ] ++ buildInputs;
  src = ./.;
}
